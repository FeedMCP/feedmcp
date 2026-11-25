# feedmcp (JavaScript / TypeScript SDK & CLI)

Official zero-dependency Node.js/TypeScript client and CLI for [FeedMCP](https://feedmcp.com/?utm_source=npm) — unified public social media, creator marketing, ad library, and e-commerce data across 21 global and Chinese platforms (193 endpoints).

> Note: FeedMCP (`feedmcp.com`) is a social media data MCP server and HTTP API, not an RSS feed reader.

## Install

```bash
npm install feedmcp
# or run the CLI directly without installing:
npx feedmcp find "tiktok comments"
```

## Quick Start

```js
import { FeedMCPClient } from "feedmcp";

const client = new FeedMCPClient(); // reads process.env.FEEDMCP_API_KEY

// 1. Free discovery (no API key required)
const matches = await client.find("tiktok comments");
const spec = await client.describe("tiktok.videos.comments.list");

// 2. Paid call with per-call spend cap (failed calls are free)
const res = await client.call(
  "tiktok.videos.comments.list",
  { id: "7700200904678559006" },
  { maxPrice: "0.002" },
);
console.log(res.data.items, res.meta.billing);

// 3. Auto-paginate
for await (const page of client.paginate("douyin.videos.comments.list", { id: "7372484719365098803" }, { maxPages: 3, maxPrice: "0.002" })) {
  console.log(page.data.items.length);
}
```

## CLI

```bash
npx feedmcp find "xiaohongshu comments"
npx feedmcp describe douyin.trends.list
npx feedmcp prices --platform tiktok
npx feedmcp status
npx feedmcp call douyin.trends.list --max-price 0.002
npx feedmcp account
```

Get a free `$0.10` trial API key (no card required): https://feedmcp.com/console/keys/?utm_source=npm
