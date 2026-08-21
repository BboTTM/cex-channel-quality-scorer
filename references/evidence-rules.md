# Evidence collection rules

## Shared rules

- Record `checked_at` as an ISO date or timestamp and keep the complete canonical source URL.
- Verify that the content author belongs to the claimed profile. Do not merge identities based only on similar names or avatars.
- Use a current profile/page observation for audience size and activity. Treat search-engine snippets as `secondary` evidence.
- Evaluate a representative recent window where accessible: the submitted content plus up to 10 recent posts/videos and the previous 90 days. State when the visible sample is smaller.
- Never infer private metrics, conversions, demographics, or audience authenticity from unavailable data.
- A broken/private/deleted link is evidence of unavailability, not evidence of bad content.

## YouTube

- Accept canonical video, Short, live, channel, or handle URLs.
- For content, verify title, description, publish date, author/channel, visible views and engagement, and transcript/captions when available.
- For channel health, verify current subscribers when public, recent upload cadence, recent comparable views, and recent Crypto/CEX activity.
- Sponsor/referral evidence may appear in spoken content, captions, description, pinned comment, or visible CTA. State exactly where it appears.
- Do not infer claims from visuals or audio that cannot be reliably read.

## X

- Prefer canonical `https://x.com/<author>/status/<id>` links for content and canonical profile URLs for channel review.
- Verify the post/reply/quote text, date, author handle, visible metrics, current followers when visible, and recent Crypto activity.
- Distinguish original commentary from copied threads, automated feeds, and engagement bait.
- A profile/search URL cannot substitute for a post URL when scoring a specific promotion.

## Telegram

- Require public channel/group links and, for content, permanent message URLs such as `t.me/<channel>/<id>` or `t.me/s/<channel>/<id>`.
- Verify public members/subscribers, message date, visible views/reactions, posting cadence, and recent Crypto activity.
- Flag official project channels, automated feeds, private groups, repost-only news, and impersonation. They may be useful media inventory but are not creator-operated KOL channels unless ownership is verified.

## Instagram

- Prefer canonical profile, post, or Reel permalinks.
- Verify author/profile linkage, caption/context, publish date, visible followers and engagement when accessible, and recent Crypto activity.
- Accept collaboration labels, referral links, promo codes, and explicit acquisition CTAs as campaign evidence.
- If public visibility is blocked, do not invent metrics; use lower-confidence corroborated or secondary evidence only when identity is still clear.

## Identity resolution and batches

- A content page that visibly names and links its author can establish the canonical profile.
- Cross-platform profiles may be merged only through explicit links or other strong public identity evidence.
- If a spreadsheet row contains only a name, try one focused public lookup. Accept a match only when region/language, niche, and identity signals are unambiguous; otherwise keep it unresolved and request a canonical link.
- Preserve the original input row and all supplied URLs in batch outputs.
