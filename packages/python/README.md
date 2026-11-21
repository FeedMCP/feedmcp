# feedmcp (Python SDK & CLI)

Official zero-dependency Python client and CLI for [FeedMCP](https://feedmcp.com) — unified public social media, creator marketing, ad library, and e-commerce data across 21 global and Chinese platforms (193 endpoints).

> Note: FeedMCP (`feedmcp.com`) is a social media data MCP server and HTTP API, not an RSS feed reader.

## Install

```bash
pip install feedmcp
```

## Quick Start

```python
from feedmcp import FeedMCPClient

client = FeedMCPClient()  # reads FEEDMCP_API_KEY from environment

# 1. Free discovery (no API key required)
matches = client.find("tiktok comments")
spec = client.describe("tiktok.videos.comments.list")

# 2. Paid call with per-call spend cap (failed calls are free)
res = client.call(
    "tiktok.videos.comments.list",
    {"id": "7700200904678559006"},
    max_price="0.002",
)
print(res["data"]["items"], res["meta"]["billing"])

# 3. Auto-paginate with cursor
for page in client.paginate("douyin.videos.comments.list", {"id": "7372484719365098803"}, max_pages=3, max_price="0.002"):
    print(len(page["data"]["items"]))
```

## CLI

```bash
feedmcp find "xiaohongshu comments"
feedmcp describe douyin.trends.list
feedmcp prices --platform tiktok
feedmcp status
feedmcp call douyin.trends.list --max-price 0.002
feedmcp account
```

Get a free `$0.10` trial API key (no card required): https://feedmcp.com/console/keys/
