# CEX Channel Quality Scorer

A reusable Codex skill for evidence-backed scoring of Crypto/CEX KOLs, channels, and sponsored content across YouTube, X, Telegram, and Instagram.

## Install

Copy or clone this repository as a folder named `cex-channel-quality-scorer` inside the receiving agent's skills directory. The agent can then invoke it explicitly:

```text
Use $cex-channel-quality-scorer to score these KOL links for the specified target market: <links>
```

The agent should read `SKILL.md`, collect current public evidence, apply the rubric, and run the deterministic scorer in `scripts/score.py`.

## What the result includes

- 100-point score and six weighted dimensions
- evidence confidence separate from quality
- verified, provisional, or insufficient-evidence status
- deterministic financial-promotion risk caps
- source URLs, evidence notes, risks, and cooperation recommendation

## Privacy

This repository contains no case history, real campaign records, creator list, exchange-specific data, credentials, cookies, tracking links, or previous scoring output. Keep all case-specific evidence and generated files outside the installed skill directory.

## Validate

```bash
python3 scripts/test_score.py
```
