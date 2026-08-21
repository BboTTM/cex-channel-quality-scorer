# Crypto/CEX channel quality rubric

## Calculation

Score every atomic criterion from `0` to `5`. The deterministic scorer converts it to weighted points:

`criterion points = criterion weight × score ÷ 5`

Do not renormalize missing criteria. When evidence is unavailable, set `score: 0` and `evidence_level: none`. This intentionally keeps the quality score conservative while confidence explains the coverage gap.

Confidence is the weighted evidence coverage:

- `direct`: 1.00 — canonical platform page, transcript/caption, or directly visible metric.
- `official_meta`: 0.85 — official embed/feed/metadata for the same canonical object.
- `corroborated`: 0.65 — two consistent public sources tied to the same identity.
- `secondary`: 0.40 — one search snippet or secondary index; use only when stronger evidence is unavailable.
- `none`: 0.00 — unavailable, private, deleted, ambiguous, or not checked.

## Dimensions and atomic weights

### 受众匹配 — 20

| Criterion | Weight | 0 anchor | 3 anchor | 5 anchor |
|---|---:|---|---|---|
| `crypto_cex_relevance` | 8 | Unrelated or mostly non-Crypto | Regular Crypto content with some CEX relevance | Consistently serves active Crypto traders/CEX users |
| `target_market_fit` | 6 | Wrong language/market | Partly serves the target language or region | Clear and sustained target-market fit |
| `acquisition_intent` | 6 | Audience shows no trading/product intent | Educational/investment audience with some intent | Strong trading, exchange, campaign, or product-discovery intent |

### 渠道健康与真实性 — 20

| Criterion | Weight | 0 anchor | 3 anchor | 5 anchor |
|---|---:|---|---|---|
| `identity_authenticity` | 8 | Identity mismatch, impersonation, or unverifiable | Canonical identity verified, limited history | Established creator identity with consistent cross-page signals |
| `activity_consistency` | 6 | Inactive over 180 days | Irregular but active within 180 days | Sustained recent publishing cadence |
| `audience_quality` | 6 | Strong manipulation/bot indicators | No clear manipulation; limited evidence | Organic-looking audience and stable cross-content behavior |

### 内容质量 — 25

| Criterion | Weight | 0 anchor | 3 anchor | 5 anchor |
|---|---:|---|---|---|
| `accuracy_depth` | 7 | Materially false or content unavailable | Generally correct but shallow | Accurate, specific, balanced, and useful |
| `originality_value` | 6 | Repost/spam/near-zero value | Standard explanation or commentary | Distinct insight, demonstration, or decision value |
| `clarity_production` | 6 | Unusable or deceptive presentation | Understandable with average execution | Clear structure, strong delivery, and appropriate production |
| `creator_fit` | 6 | Content conflicts with channel identity | Reasonable fit | Natural, credible fit with the creator's established content |

### 互动有效性 — 15

Use recent comparable posts when possible. Do not compare raw counts across platforms without channel context.

| Criterion | Weight | 0 anchor | 3 anchor | 5 anchor |
|---|---:|---|---|---|
| `reach_efficiency` | 6 | No verified reach or extremely weak versus baseline | Typical reach for the channel | Strong, repeatable reach versus recent channel baseline |
| `engagement_rate` | 5 | No verified engagement or implausible pattern | Normal verified interaction | Strong verified interaction without manipulation signals |
| `comment_quality` | 4 | Bot/repetitive/irrelevant comments | Mixed but relevant discussion | Substantive audience questions, intent, and discussion |

### 投放执行 — 10

| Criterion | Weight | 0 anchor | 3 anchor | 5 anchor |
|---|---:|---|---|---|
| `brand_integration` | 4 | Brand absent, misleading, or forced | Brand/product explained adequately | Natural, accurate integration with clear value proposition |
| `cta_tracking` | 3 | No CTA/link or broken destination | Visible CTA or working link | Clear CTA, valid destination, and usable tracking/referral path |
| `disclosure_completeness` | 3 | Hidden sponsorship or deceptive omission | Basic sponsorship/context disclosure | Clear disclosure plus important eligibility/risk context |

### 品牌安全与金融宣传风险 — 10

Higher scores mean safer behavior.

| Criterion | Weight | 0 anchor | 3 anchor | 5 anchor |
|---|---:|---|---|---|
| `factual_safety` | 3 | Major misinformation | Some unsupported or overstated claims | Claims are bounded, accurate, and verifiable |
| `financial_claims_safety` | 3 | Guaranteed profit or concealed material risk | Aggressive claims with partial caveats | No guarantees; material trading risks are treated responsibly |
| `reputation_safety` | 2 | Repeated harmful controversy or hate/abuse | Minor concerns without sustained pattern | No material public brand-safety issue found |
| `fraud_spam_safety` | 2 | Scam, phishing, impersonation, or malicious link | Some spam-like tactics | No fraud, phishing, or deceptive-link signal found |

## Labels and recommendations

- Base quality label: `高质量` for 80–100, `中质量` for 60–79.99, `低质量` below 60.
- `已验证`: identity verified and confidence at least 60.
- `暂定`: identity verified and confidence from 25 to 59.99. Prefix the quality label with `暂定·`.
- `证据不足`: identity unverified or confidence below 25. Do not present the base label as a formal decision.
- Default recommendations: verified 80+ `优先合作`; verified 60–79.99 `建议小额测试`; verified below 60 `暂缓合作`; provisional `补充证据后小额测试`; insufficient `需补主页或内容链接`.

## Deterministic risk caps

- `malware_phishing`: cap total score at 9.
- `impersonation` or `fraud_scam`: cap at 19.
- `major_financial_misinformation`: cap at 29.
- `guaranteed_returns` or `audience_manipulation`: cap at 39.
- Any other `critical` risk: cap at 39.
- Any uncapped `high` risk: cap at 59.

Risk caps never raise a score. A cap of 39 or lower forces recommendation `拒绝合作` when identity is verified; otherwise the outcome remains `证据不足`.
