# FeedMCP — Social Media Data MCP Server, REST API & SDKs

[![FeedMCP MCP connector](https://glama.ai/mcp/connectors/com.feedmcp/mcp/badges/score.svg)](https://glama.ai/mcp/connectors/com.feedmcp/mcp)

[中文文档](./README.zh-CN.md) · [Website](https://feedmcp.com) · [Endpoints & Pricing](https://feedmcp.com/pricing/) · [Docs](https://feedmcp.com/docs/) · [Integrations](https://feedmcp.com/integrations/) · [Glama](https://glama.ai/mcp/connectors/com.feedmcp/mcp) · [`llms.txt`](https://feedmcp.com/llms.txt)

**One API key and one unified JSON schema for public social media, creator marketing, ad library, and e-commerce data across 21 global and Chinese platforms (193 endpoints).** Pay per call starting at **$0.0003**; failed, timed-out, and missing-object calls are **always free**.

> **Note:** FeedMCP (`feedmcp.com`) is a hosted **social media data MCP server and HTTP API**. It is unrelated to open-source `feed-mcp` projects that parse RSS/Atom feeds.

---

## Why FeedMCP

- **21 platforms, 193 endpoints, one schema**: Posts, comments, accounts, trends, transcripts, ads, and products return the same field names across global and Chinese platforms.
- **Global + China coverage behind one key**: TikTok (+ Ads Library & TikTok Shop), YouTube, Instagram, X (Twitter), Threads, Telegram, Reddit, LinkedIn (+ Ads), Facebook, Pinterest, Meta Ad Library, Google Ads Transparency — alongside Xiaohongshu (RedNote + PGY), Douyin (+ Xingtu & Ocean Engine), Kuaishou, WeChat Official Accounts, WeChat Channels, WeChat Search & Index, Weibo, Zhihu, and Bilibili.
- **Pay per call, no subscription**: Starts at **$0.0003** (most global & Douyin/Weibo/Zhihu/Bilibili endpoints are **$0.002/call**; Xiaohongshu & WeChat are **$0.02/call**). Balances never expire. Sign up at [feedmcp.com/console](https://feedmcp.com/console/keys/) for **$0.10 free trial credit** (no card required).
- **Agent-safe guardrails built in**: Per-key spend caps, per-request `X-Max-Price` / `max_price`, 24-hour `Idempotency-Key` replay, and explicit `charged` / `retry` fields on every error.
- **Public data only**: No platform logins, cookies, burner accounts, personal contact details, or video downloads.

---

## Quick Start: Remote MCP (`https://api.feedmcp.com/mcp`)

FeedMCP runs a stateless **Streamable HTTP** MCP server with 4 tools:
- `find` — discover endpoints and live prices in plain words (**free, no key**)
- `describe` — inspect parameters, fields, and pricing (**free, no key**)
- `call` — execute any endpoint with optional `max_price` and `idempotency_key`
- `account` — check remaining balance and key spend against its cap

### Claude Code
```bash
claude mcp add --transport http feedmcp https://api.feedmcp.com/mcp \
  --header "Authorization: Bearer $FEEDMCP_API_KEY"
```

### Cursor (`~/.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "feedmcp": {
      "url": "https://api.feedmcp.com/mcp",
      "headers": {
        "Authorization": "Bearer fmk_live_YOUR_KEY"
      }
    }
  }
}
```

### OpenAI Codex CLI (`~/.codex/config.toml`)
```toml
[mcp_servers.feedmcp]
url = "https://api.feedmcp.com/mcp"
http_headers = { Authorization = "Bearer fmk_live_YOUR_KEY" }
```

More client guides (Claude Desktop, Windsurf, Cherry Studio, ChatGPT Actions, DeepSeek, WorkBuddy, Doubao/Coze, Qwen, Dify & n8n): [docs/mcp-setup.md](./docs/mcp-setup.md) or [feedmcp.com/integrations/](https://feedmcp.com/integrations/).

---

## Python SDK & CLI (`packages/python`)

Zero external runtime dependencies (Python 3.9+ stdlib only).

```bash
pip install feedmcp-sdk
```

```python
from feedmcp import FeedMCPClient

client = FeedMCPClient()  # reads FEEDMCP_API_KEY from env (optional for find/describe/prices/status)

# Free discovery (no key required)
matches = client.find("tiktok comments")

# Paid data call with budget cap
res = client.call(
    "tiktok.videos.comments.list",
    {"id": "7700200904678559006"},
    max_price="0.002",
)
print(len(res["data"]["items"]), res["meta"]["billing"])
```

CLI:
```bash
feedmcp find "xiaohongshu comments"
feedmcp describe douyin.trends.list
feedmcp status
feedmcp call douyin.trends.list --max-price 0.002
```

---

## JavaScript / TypeScript SDK & CLI (`packages/js`)

Zero external runtime dependencies (Node.js 18+ native `fetch`, full TypeScript definitions included).

```bash
npm install feedmcp
# or run CLI directly:
npx feedmcp find "youtube transcript"
```

```js
import { FeedMCPClient } from "feedmcp";

const client = new FeedMCPClient(); // reads process.env.FEEDMCP_API_KEY

const hits = await client.find("meta ads");
const res = await client.call("douyin.trends.list", {}, { maxPrice: "0.002" });
console.log(res.data.items.slice(0, 5));
```

---

## Supported Platforms (21 Platforms · 193 Endpoints)

| Platform | Endpoints | Starting Price | Highlights |
| --- | ---: | ---: | --- |
| [TikTok](https://feedmcp.com/apis/tiktok/) | 15 | $0.002 | Videos, comments & replies, transcripts, profiles, trends, Ads Library, TikTok Shop products & reviews |
| [YouTube](https://feedmcp.com/apis/youtube/) | 8 | $0.002 | Video search, details, timed transcripts, comments & replies, channels |
| [Instagram](https://feedmcp.com/apis/instagram/) | 9 | $0.002 | Profiles, posts, Reels search, hashtags, comments & replies, transcripts |
| [X (Twitter)](https://feedmcp.com/apis/x/) | 21 | $0.0003/item | Search, posts, replies, full threads, X Articles, quotes, mentions, communities, lists, trends, transcripts |
| [Threads](https://feedmcp.com/apis/threads/) | 5 | $0.002 | Post search, posts, replies, profiles, user posts |
| [Telegram](https://feedmcp.com/apis/telegram/) | 3 | $0.002 | Public channels, channel message history, single posts |
| [Reddit](https://feedmcp.com/apis/reddit/) | 6 | $0.002 | Search, subreddit feeds, posts, comment trees, subreddit info, transcripts |
| [LinkedIn](https://feedmcp.com/apis/linkedin/) | 8 | $0.002 | Post search, profiles, company pages & posts, LinkedIn Ad Library, transcripts |
| [Facebook](https://feedmcp.com/apis/facebook/) | 4 | $0.002 | Public pages, page posts, posts, comments |
| [Pinterest](https://feedmcp.com/apis/pinterest/) | 3 | $0.002 | Pin search, pins, boards |
| [Meta Ad Library](https://feedmcp.com/apis/meta/) | 5 | $0.002 | Ad search, advertiser ads, ad details, video ad transcripts |
| [Google Ads Transparency](https://feedmcp.com/apis/google/) | 3 | $0.002 | Advertiser search, advertiser ads, ad details |
| [Xiaohongshu (RedNote)](https://feedmcp.com/apis/xiaohongshu/) | 22 | $0.02 | Notes, search, comments & replies, users + 15 PGY creator & keyword analytics endpoints |
| [Douyin](https://feedmcp.com/apis/douyin/) | 29 | $0.002 | Videos, comments, trends, search + 12 Xingtu creator endpoints + 8 Ocean Engine index endpoints |
| [Kuaishou](https://feedmcp.com/apis/kuaishou/) | 8 | $0.002 | Videos, comments & replies, users, search, trending |
| [WeChat Official Accounts](https://feedmcp.com/apis/wechat_mp/) | 8 | $0.02 | Article full text, reads/likes/shares stats, comments & replies, account history, search, verified owners |
| [WeChat Channels](https://feedmcp.com/apis/wechat_channels/) | 7 | $0.015 | Profiles, videos, search, comments & replies, live replays |
| [WeChat Search](https://feedmcp.com/apis/wechat/) | 3 | $0.02 | Account search (MP/Channels/Mini Programs), WeChat Index, search suggestions |
| [Weibo](https://feedmcp.com/apis/weibo/) | 8 | $0.002 | Hot search trends, posts, comments & replies, users, search |
| [Zhihu](https://feedmcp.com/apis/zhihu/) | 10 | $0.002 | Hot list, search, questions, answers, comments & replies, users |
| [Bilibili](https://feedmcp.com/apis/bilibili/) | 8 | $0.002 | Videos, comments & replies, creators, uploads, search, trending |

Full live price book: [feedmcp.com/prices.json](https://feedmcp.com/prices.json) · OpenAPI 3.1: [feedmcp.com/openapi.json](https://feedmcp.com/openapi.json)

---

## Agent & Protocol Discovery

FeedMCP implements standard agent discovery endpoints:
- `https://feedmcp.com/llms.txt` & `https://feedmcp.com/zh/llms.txt`
- `https://feedmcp.com/agents.md` & `https://feedmcp.com/auth.md`
- `https://feedmcp.com/.well-known/api-catalog` (RFC 9727)
- `https://feedmcp.com/.well-known/ard.json` & `https://feedmcp.com/.well-known/ai-catalog.json` (Agentic Resource Discovery)
- `https://feedmcp.com/.well-known/mcp/server-card.json` (MCP Server Card)
- `https://feedmcp.com/.well-known/agent-skills/index.json` (Agent Skills Discovery v0.2.0)
- `Accept: text/markdown` content negotiation (with YAML frontmatter and `x-markdown-tokens`) supported on every public page
- Browse by capability: [Comments API](https://feedmcp.com/roles/comments/) · [Video Transcripts API](https://feedmcp.com/roles/transcripts/) · [Trending & Index API](https://feedmcp.com/roles/trends/) · [Ad Libraries API](https://feedmcp.com/roles/ads/) · [Creator Rate Cards API](https://feedmcp.com/roles/creators/)
- Side-by-side comparison: [Best Social Media Data APIs & MCP Servers (2026)](https://feedmcp.com/compare/best-social-media-data-apis/) · [TikHub vs FeedMCP](https://feedmcp.com/compare/tikhub-vs-feedmcp/)

---

## License

MIT — see [LICENSE](./LICENSE). Support: [support@feedmcp.com](mailto:support@feedmcp.com).
