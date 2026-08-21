---
name: cex-channel-quality-scorer
description: Score Crypto/CEX creators, channels, and sponsored content on YouTube, X, Telegram, or Instagram using cited public evidence, conservative missing-data handling, confidence, and financial-promotion risk controls. Use for single links, link batches, or channel spreadsheets; do not use as an ROI or conversion measurement tool without internal performance data.
---

# CEX Channel Quality Scorer

Produce repeatable, evidence-backed channel and content quality scores for Crypto/CEX marketing decisions.

## Workflow

1. Normalize each input into a channel/profile link, a content link, or an unresolved name. Never assume identity from a name alone.
2. Collect only public evidence. Prefer an available platform connector or official API, then the canonical public page, then a logged-in browser when the user authorizes it, then public search snippets as a low-confidence fallback.
3. Read [references/evidence-rules.md](references/evidence-rules.md) for the relevant platform. Record the observation date and complete source URLs; do not store credentials, cookies, tokens, or browser state.
4. Read [references/rubric.md](references/rubric.md). Assign every atomic criterion a `0–5` score and an evidence level. Unknown criteria receive score `0`; do not redistribute their weight.
5. Create the input JSON defined in [references/output-schema.md](references/output-schema.md), then run:

   ```bash
   python3 scripts/score.py --input evidence.json --output scored.json --csv scored.csv
   ```

6. Report the deterministic result. Separate quality from confidence, surface risk caps, and distinguish verified, provisional, and insufficient-evidence outcomes.

## Decisions and boundaries

- The score represents public-evidence Crypto/CEX advertising quality, not ROI, registrations, first deposits, or trading volume.
- Use canonical content/profile URLs. A search result or UTM link is supporting context, not proof of channel identity.
- If `identity_verified` is false, keep the row but label it `证据不足`; do not make a formal cooperation recommendation.
- Severe risks such as impersonation, scams, phishing, fabricated audience, guaranteed returns, or major financial misinformation trigger deterministic caps in the scorer.
- When a content link exists but the profile link is missing, resolve the content author from the canonical platform page before scoring the channel.
- For a batch, preserve every original row and add result fields. Never delete low-confidence rows.
- If a spreadsheet is requested, keep raw inputs separate from the scored output and include full source URLs and the verification date.

## Privacy and reusable packaging

- Treat every scoring request as an independent run. Do not reuse, cache, or infer evidence, identities, scores, or recommendations from earlier cases.
- Do not store account credentials, cookies, browser state, private analytics exports, or hidden identifiers in the skill directory.
- Keep case-specific inputs and outputs outside the skill directory. The installed skill must contain only generic instructions, schemas, and deterministic code.
- Examples and tests must use fictional names, placeholder URLs, and synthetic values. Never add a real exchange, campaign, creator, channel, referral code, UTM, or prior result to the package.
- Before sharing or publishing the skill, exclude generated JSON, CSV, spreadsheets, screenshots, logs, caches, archives, and local-path metadata.

## Standard response

For each channel, show total score, six dimension scores, quality label, confidence, status, important evidence, risks, and recommendation. For batches, also summarize counts for `优先合作`, `建议小额测试`, `暂缓合作`, and `证据不足`.
