#!/usr/bin/env python3

import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("score.py")
SPEC = importlib.util.spec_from_file_location("cex_score", MODULE_PATH)
score = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(score)


def complete_record(value=5, level="direct"):
    return {
        "record_id": "one",
        "channel_name": "Test",
        "platform": "YouTube",
        "canonical_url": "https://www.youtube.com/@test",
        "identity_verified": True,
        "criteria": {
            criterion: {"score": value, "evidence_level": level, "source_urls": ["https://example.com/evidence"]}
            for criterion in score.CRITERION_WEIGHTS
        },
    }


class ScoreTests(unittest.TestCase):
    def test_weights_sum_to_100(self):
        self.assertEqual(sum(score.CRITERION_WEIGHTS.values()), 100)

    def test_perfect_record(self):
        result = score.score_record(complete_record())
        self.assertEqual(result["total_score"], 100)
        self.assertEqual(result["confidence"], 100)
        self.assertEqual(result["quality_label"], "高质量")
        self.assertEqual(result["recommendation"], "优先合作")

    def test_missing_evidence_is_conservative(self):
        result = score.score_record({"record_id": "missing", "identity_verified": True})
        self.assertEqual(result["total_score"], 0)
        self.assertEqual(result["confidence"], 0)
        self.assertEqual(result["status"], "证据不足")

    def test_risk_cap(self):
        record = complete_record()
        record["risks"] = [{"code": "guaranteed_returns", "severity": "critical"}]
        result = score.score_record(record)
        self.assertEqual(result["raw_score"], 100)
        self.assertEqual(result["total_score"], 39)
        self.assertEqual(result["recommendation"], "拒绝合作")

    def test_unverified_identity(self):
        record = complete_record()
        record["identity_verified"] = False
        result = score.score_record(record)
        self.assertEqual(result["quality_label"], "证据不足")
        self.assertEqual(result["recommendation"], "需补主页或内容链接")

    def test_none_evidence_cannot_have_points(self):
        record = complete_record()
        first = next(iter(score.CRITERION_WEIGHTS))
        record["criteria"][first] = {"score": 3, "evidence_level": "none"}
        with self.assertRaises(score.ScoringError):
            score.score_record(record)

    def test_duplicate_ids_rejected(self):
        record = complete_record()
        with self.assertRaises(score.ScoringError):
            score.score_payload([record, record])

    def test_four_platform_fixtures(self):
        records = []
        for index, platform in enumerate(["YouTube", "X", "Telegram", "Instagram"], start=1):
            record = complete_record(value=3, level="official_meta")
            record["record_id"] = f"platform-{index}"
            record["platform"] = platform
            records.append(record)
        result = score.score_payload(records)
        self.assertEqual(result["summary"]["by_platform"], {"YouTube": 1, "X": 1, "Telegram": 1, "Instagram": 1})

    def test_secondary_evidence_is_provisional(self):
        result = score.score_record(complete_record(value=4, level="secondary"))
        self.assertEqual(result["confidence"], 40)
        self.assertEqual(result["status"], "暂定")
        self.assertTrue(result["quality_label"].startswith("暂定·"))

    def test_unknown_critical_risk_cap(self):
        record = complete_record()
        record["risks"] = [{"code": "new_critical_risk", "severity": "critical"}]
        result = score.score_record(record)
        self.assertEqual(result["total_score"], 39)
        self.assertEqual(result["recommendation"], "拒绝合作")


if __name__ == "__main__":
    unittest.main()
