#!/usr/bin/env python3
"""Deterministic Crypto/CEX channel quality scorer (standard library only)."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION = "1.0.0"

DIMENSIONS = {
    "audience_fit": {
        "label": "受众匹配",
        "criteria": {"crypto_cex_relevance": 8, "target_market_fit": 6, "acquisition_intent": 6},
    },
    "channel_health": {
        "label": "渠道健康与真实性",
        "criteria": {"identity_authenticity": 8, "activity_consistency": 6, "audience_quality": 6},
    },
    "content_quality": {
        "label": "内容质量",
        "criteria": {"accuracy_depth": 7, "originality_value": 6, "clarity_production": 6, "creator_fit": 6},
    },
    "engagement_effectiveness": {
        "label": "互动有效性",
        "criteria": {"reach_efficiency": 6, "engagement_rate": 5, "comment_quality": 4},
    },
    "campaign_execution": {
        "label": "投放执行",
        "criteria": {"brand_integration": 4, "cta_tracking": 3, "disclosure_completeness": 3},
    },
    "brand_safety": {
        "label": "品牌安全与金融宣传风险",
        "criteria": {"factual_safety": 3, "financial_claims_safety": 3, "reputation_safety": 2, "fraud_spam_safety": 2},
    },
}

EVIDENCE_FACTORS = {"direct": 1.0, "official_meta": 0.85, "corroborated": 0.65, "secondary": 0.4, "none": 0.0}
RISK_CAPS = {
    "malware_phishing": 9,
    "impersonation": 19,
    "fraud_scam": 19,
    "major_financial_misinformation": 29,
    "guaranteed_returns": 39,
    "audience_manipulation": 39,
}

CRITERION_WEIGHTS = {
    criterion: weight
    for dimension in DIMENSIONS.values()
    for criterion, weight in dimension["criteria"].items()
}


class ScoringError(ValueError):
    pass


def _round(value: float) -> float:
    return round(value + 1e-12, 2)


def _risk_cap(risks: list[dict[str, Any]]) -> int | None:
    caps: list[int] = []
    for risk in risks:
        code = str(risk.get("code", "")).strip()
        severity = str(risk.get("severity", "")).strip().lower()
        if code in RISK_CAPS:
            caps.append(RISK_CAPS[code])
        elif severity == "critical":
            caps.append(39)
        elif severity == "high":
            caps.append(59)
    return min(caps) if caps else None


def _base_quality(score: float) -> str:
    if score >= 80:
        return "高质量"
    if score >= 60:
        return "中质量"
    return "低质量"


def _status(identity_verified: bool, confidence: float) -> str:
    if not identity_verified or confidence < 25:
        return "证据不足"
    if confidence < 60:
        return "暂定"
    return "已验证"


def _recommendation(status: str, score: float, cap: int | None) -> str:
    if status == "证据不足":
        return "需补主页或内容链接"
    if cap is not None and cap <= 39:
        return "拒绝合作"
    if status == "暂定":
        return "补充证据后小额测试"
    if score >= 80:
        return "优先合作"
    if score >= 60:
        return "建议小额测试"
    return "暂缓合作"


def score_record(record: dict[str, Any]) -> dict[str, Any]:
    criteria_input = record.get("criteria") or {}
    if not isinstance(criteria_input, dict):
        raise ScoringError("criteria must be an object")
    unknown = sorted(set(criteria_input) - set(CRITERION_WEIGHTS))
    if unknown:
        raise ScoringError(f"unknown criteria: {', '.join(unknown)}")

    normalized: dict[str, dict[str, Any]] = {}
    source_urls: list[str] = []
    dimension_scores: dict[str, float] = {}
    raw_score = 0.0
    confidence_points = 0.0

    for dimension_key, dimension in DIMENSIONS.items():
        dimension_total = 0.0
        for criterion, weight in dimension["criteria"].items():
            item = criteria_input.get(criterion) or {}
            if not isinstance(item, dict):
                raise ScoringError(f"criterion {criterion} must be an object")
            level = str(item.get("evidence_level", "none"))
            if level not in EVIDENCE_FACTORS:
                raise ScoringError(f"invalid evidence_level for {criterion}: {level}")
            try:
                score = float(item.get("score", 0))
            except (TypeError, ValueError) as exc:
                raise ScoringError(f"non-numeric score for {criterion}") from exc
            if not 0 <= score <= 5:
                raise ScoringError(f"score for {criterion} must be between 0 and 5")
            if level == "none" and score != 0:
                raise ScoringError(f"criterion {criterion} with evidence_level none must have score 0")
            urls = item.get("source_urls") or []
            if not isinstance(urls, list) or not all(isinstance(url, str) for url in urls):
                raise ScoringError(f"source_urls for {criterion} must be a list of strings")
            for url in urls:
                if url and url not in source_urls:
                    source_urls.append(url)
            points = weight * score / 5.0
            dimension_total += points
            raw_score += points
            confidence_points += weight * EVIDENCE_FACTORS[level]
            normalized[criterion] = {
                "score": _round(score),
                "weight": weight,
                "points": _round(points),
                "evidence_level": level,
                "source_urls": urls,
                "note": str(item.get("note", "")),
            }
        dimension_scores[dimension_key] = _round(dimension_total)

    risks = record.get("risks") or []
    if not isinstance(risks, list) or not all(isinstance(risk, dict) for risk in risks):
        raise ScoringError("risks must be a list of objects")
    for risk in risks:
        evidence_url = risk.get("evidence_url")
        if isinstance(evidence_url, str) and evidence_url and evidence_url not in source_urls:
            source_urls.append(evidence_url)

    raw_score = _round(raw_score)
    confidence = _round(confidence_points)
    cap = _risk_cap(risks)
    total_score = _round(min(raw_score, cap) if cap is not None else raw_score)
    identity_verified = bool(record.get("identity_verified", False))
    status = _status(identity_verified, confidence)
    base_quality = _base_quality(total_score)
    quality_label = "证据不足" if status == "证据不足" else (f"暂定·{base_quality}" if status == "暂定" else base_quality)

    return {
        "record_id": str(record.get("record_id", "")),
        "channel_name": str(record.get("channel_name", "")),
        "platform": str(record.get("platform", "")),
        "canonical_url": str(record.get("canonical_url", "")),
        "content_url": str(record.get("content_url", "")),
        "identity_verified": identity_verified,
        "checked_at": str(record.get("checked_at", "")),
        "dimension_scores": dimension_scores,
        "raw_score": raw_score,
        "total_score": total_score,
        "quality_label": quality_label,
        "confidence": confidence,
        "status": status,
        "risk_cap": cap,
        "risks": risks,
        "recommendation": _recommendation(status, total_score, cap),
        "evidence_summary": str(record.get("evidence_summary", "")),
        "source_urls": source_urls,
        "criteria": normalized,
        "original": record.get("original") or {},
    }


def score_payload(payload: Any) -> dict[str, Any]:
    records = payload.get("records") if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        raise ScoringError("input must be a list or an object containing records")
    results: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            raise ScoringError(f"record {index} must be an object")
        result = score_record(record)
        record_id = result["record_id"] or f"row-{index:03d}"
        if record_id in seen_ids:
            raise ScoringError(f"duplicate record_id: {record_id}")
        seen_ids.add(record_id)
        result["record_id"] = record_id
        results.append(result)

    summary = {
        "total_records": len(results),
        "by_status": dict(Counter(row["status"] for row in results)),
        "by_quality_label": dict(Counter(row["quality_label"] for row in results)),
        "by_recommendation": dict(Counter(row["recommendation"] for row in results)),
        "by_platform": dict(Counter(row["platform"] or "Unknown" for row in results)),
    }
    return {
        "meta": {
            "scorer_version": VERSION,
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "dimension_weights": {key: sum(value["criteria"].values()) for key, value in DIMENSIONS.items()},
            "evidence_factors": EVIDENCE_FACTORS,
        },
        "summary": summary,
        "records": results,
    }


def write_csv(path: Path, records: list[dict[str, Any]]) -> None:
    fields = [
        "record_id", "channel_name", "platform", "canonical_url", "content_url", "total_score",
        "audience_fit", "channel_health", "content_quality", "engagement_effectiveness",
        "campaign_execution", "brand_safety", "quality_label", "confidence", "status", "risk_cap",
        "recommendation", "evidence_summary", "checked_at", "risks", "source_urls", "original",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in records:
            dims = row["dimension_scores"]
            writer.writerow({
                "record_id": row["record_id"], "channel_name": row["channel_name"], "platform": row["platform"],
                "canonical_url": row["canonical_url"], "content_url": row["content_url"], "total_score": row["total_score"],
                "audience_fit": dims["audience_fit"], "channel_health": dims["channel_health"],
                "content_quality": dims["content_quality"], "engagement_effectiveness": dims["engagement_effectiveness"],
                "campaign_execution": dims["campaign_execution"], "brand_safety": dims["brand_safety"],
                "quality_label": row["quality_label"], "confidence": row["confidence"], "status": row["status"],
                "risk_cap": "" if row["risk_cap"] is None else row["risk_cap"], "recommendation": row["recommendation"],
                "evidence_summary": row["evidence_summary"], "checked_at": row["checked_at"],
                "risks": json.dumps(row["risks"], ensure_ascii=False, sort_keys=True),
                "source_urls": json.dumps(row["source_urls"], ensure_ascii=False),
                "original": json.dumps(row["original"], ensure_ascii=False, sort_keys=True),
            })


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--csv", type=Path)
    args = parser.parse_args()

    with args.input.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    result = score_payload(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        write_csv(args.csv, result["records"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
