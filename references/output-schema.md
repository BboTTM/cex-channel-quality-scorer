# Input and output contract

## Evidence input

The scorer accepts either a JSON object with `records` or a top-level array. Every record uses this shape:

```json
{
  "record_id": "row-001",
  "channel_name": "Example Crypto",
  "platform": "YouTube",
  "canonical_url": "https://www.youtube.com/@example",
  "content_url": "https://www.youtube.com/watch?v=example",
  "identity_verified": true,
  "checked_at": "YYYY-MM-DD",
  "evidence_summary": "Canonical video and channel inspected.",
  "criteria": {
    "crypto_cex_relevance": {
      "score": 4,
      "evidence_level": "direct",
      "source_urls": ["https://www.youtube.com/@example"],
      "note": "Most recent uploads cover trading and exchanges."
    }
  },
  "risks": [
    {
      "code": "guaranteed_returns",
      "severity": "critical",
      "evidence_url": "https://www.youtube.com/watch?v=example",
      "note": "Claims guaranteed daily profit."
    }
  ],
  "original": {}
}
```

All criteria listed in `rubric.md` are optional in input but absent criteria are treated as unknown/zero. Score must be numeric from `0` to `5`. Evidence level must be `direct`, `official_meta`, `corroborated`, `secondary`, or `none`.

## Scored output

The JSON output contains:

```text
meta: scorer version, weights, generation timestamp
summary: counts by status, quality label, recommendation, and platform
records: original identity fields plus dimension scores, raw score, capped score,
         quality label, confidence, status, risk cap, risks, recommendation,
         evidence summary, checked_at, source_urls, criteria details, original
```

Dimension and total scores are rounded to two decimals. Confidence is `0–100`. The CSV flattens result fields and retains the JSON-encoded `original`, `risks`, and `source_urls` fields so no evidence is lost.

## Batch reporting

Keep raw input fields unchanged. Recommended spreadsheet columns are:

```text
Original fields | Platform | Canonical URL | Content URL | Total Score |
Audience Fit | Channel Health | Content Quality | Engagement Effectiveness |
Campaign Execution | Brand Safety | Quality Label | Confidence | Status |
Risk Cap | Risks | Recommendation | Evidence Summary | Checked At | Source URLs
```

For low-confidence rows, the status and missing-evidence request must remain visible even if a numeric conservative score is present.
