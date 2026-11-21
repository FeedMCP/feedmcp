# FeedMCP Platforms & Pricing Overview

All 193 endpoints return one unified JSON envelope (`code`, `request_id`, `data`, `page`, `warnings`, `meta.billing`). Every price below is pay-per-call in USD; failed, timed-out, and not-found calls are free.

- Live machine-readable prices: `GET https://api.feedmcp.com/v1/catalog/prices` (free, no key) or `https://feedmcp.com/prices.json`
- Free natural-language search: `GET https://api.feedmcp.com/v1/catalog/search?q=tiktok+comments`
- Live platform status: `GET https://api.feedmcp.com/v1/catalog/status`

## Global Platforms
- **TikTok** (15 endpoints, `$0.002`): video search/get/comments/replies/transcript, users, trends, TikTok Ads Library, TikTok Shop products & reviews.
- **YouTube** (8 endpoints, `$0.002`): video search/get/comments/replies/transcript, channels & channel videos.
- **Instagram** (9 endpoints, `$0.002–$0.003`): profiles, posts, Reels search, hashtags, comments/replies, transcripts.
- **X (Twitter)** (21 endpoints, `$0.0003/item–$0.002/call`): search, posts, replies, followers/following, retweeters, communities, lists, trends, full threads (`$0.0003/item`), quotes (`$0.0003/item`), mentions (`$0.0003/item`), user search (`$0.0004/item`), full X Articles (`$0.002`), transcripts (`$0.002`).
- **Threads** (5 endpoints, `$0.002–$0.003`): search, posts, replies, profiles, user posts.
- **Telegram** (3 endpoints, `$0.002`): public channels, channel message history, single posts.
- **Reddit** (6 endpoints, `$0.002`): post search, subreddit feeds, posts, comments, subreddit info, transcripts.
- **LinkedIn** (8 endpoints, `$0.002`): post search, posts, profiles, company pages & posts, LinkedIn Ad Library, transcripts.
- **Facebook** (4 endpoints, `$0.002`): public pages, page posts, posts, comments.
- **Pinterest** (3 endpoints, `$0.002`): pin search, pin details, board pins.
- **Meta Ad Library** (5 endpoints, `$0.002`): ad search, advertiser search, advertiser ads, ad details, video ad transcripts.
- **Google Ads Transparency** (3 endpoints, `$0.002`): advertiser search, advertiser ads, ad details.

## Chinese Platforms
- **Xiaohongshu / RedNote** (22 endpoints, `$0.02–$0.04`): notes, search, comments/replies, users (`$0.02`) + 15 PGY creator & keyword analytics endpoints (`$0.04`).
- **Douyin** (29 endpoints, `$0.002–$0.04`): videos, comments/replies, trends (`$0.002`), search (`$0.02`), 12 Xingtu creator endpoints (`$0.002–$0.04`), 8 Ocean Engine index endpoints (`$0.002–$0.006`).
- **Kuaishou** (8 endpoints, `$0.002–$0.02`): videos, comments/replies, trends (`$0.002`), search & users (`$0.02`).
- **WeChat Official Accounts** (8 endpoints, `$0.02–$0.10`): articles, reads/likes/shares stats, comments/replies, account article lists, search (`$0.02`), verified corporate owners (`$0.10`).
- **WeChat Channels** (7 endpoints, `$0.015–$0.05`): profiles, videos, search, comments (`$0.02`), comment replies (`$0.015`), live replays (`$0.05`).
- **WeChat Search** (3 endpoints, `$0.02–$0.10`): account search (`$0.02`), WeChat Index (`$0.10`), search suggestions (`$0.10`).
- **Weibo** (8 endpoints, `$0.002–$0.003`): trends, posts, comments/replies, users (`$0.002`), search (`$0.003`).
- **Zhihu** (10 endpoints, `$0.002`): hot list, search, questions, answers, comments/replies, users.
- **Bilibili** (8 endpoints, `$0.002–$0.003`): videos, comments/replies, creators, uploads, trends (`$0.002`), search (`$0.003`).
