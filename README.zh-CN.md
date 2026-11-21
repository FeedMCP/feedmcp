# FeedMCP — 社媒数据 MCP 服务器、REST API 与官方 SDK

[English README](./README.md) · [官网](https://feedmcp.com/zh/) · [接口与定价](https://feedmcp.com/zh/pricing/) · [文档](https://feedmcp.com/zh/docs/) · [AI 客户端接入](https://feedmcp.com/zh/integrations/) · [中文 `llms.txt`](https://feedmcp.com/zh/llms.txt)

**一把 API Key、一套统一返回格式，覆盖海内外 21 个社交媒体与广告平台（193 个公开数据接口）。** 纯按次付费（每次 **$0.0003** 起，无月费、余额永不过期），失败、超时和对象不存在的调用**全部免费**。

> **说明**：FeedMCP（`feedmcp.com`）是托管式**社媒数据 MCP 服务器和 HTTP API**，与 GitHub 上用于解析 RSS 订阅源的开源项目 `feed-mcp` 无关。

---

## 核心特性

- **21 个平台、193 个接口统一 Schema**：海外平台（TikTok、YouTube、Instagram、X、Threads、Telegram、Reddit、LinkedIn、Facebook、Pinterest、Meta/Google 广告库、TikTok Shop）与中国平台（小红书 + 蒲公英、抖音 + 星图 + 巨量算数、快手、微信公众号、视频号、微信搜一搜/微信指数、微博、知乎、B 站）全部统一字段格式。
- **按次付费，失败不收费**：大部分平台接口 **$0.002/次**，小红书与微信 **$0.02/次**，X 引用/提及/对话串按条 **$0.0003/条**。新用户邮箱注册即送 **$0.10 试用额度**（无需绑卡）。
- **专为 AI Agent 设计的三层预算护栏**：单把 Key 可设总花费上限 + 单次请求 `X-Max-Price`/`max_price` + 24 小时 `Idempotency-Key` 幂等防重扣。
- **零账号风险**：只提供公开数据，不需要你的平台账号、Cookie 或本地代理池。

---

## 快速接入远程 MCP（`https://api.feedmcp.com/mcp`）

提供 4 个工具：`find`（免费找接口）、`describe`（免费看参数和价格）、`call`（调用取数）、`account`（查余额与 Key 上限）。

### Claude Code
```bash
claude mcp add --transport http feedmcp https://api.feedmcp.com/mcp \
  --header "Authorization: Bearer $FEEDMCP_API_KEY"
```

### Cursor（`~/.cursor/mcp.json`）
```json
{
  "mcpServers": {
    "feedmcp": {
      "url": "https://api.feedmcp.com/mcp",
      "headers": {
        "Authorization": "Bearer fmk_live_你的Key"
      }
    }
  }
}
```

更多客户端（Claude Desktop、Codex、Windsurf、Cherry Studio、ChatGPT Actions、DeepSeek、WorkBuddy、豆包/扣子、通义千问、Dify & n8n）见 [docs/mcp-setup.md](./docs/mcp-setup.md) 或 [feedmcp.com/zh/integrations/](https://feedmcp.com/zh/integrations/)。

---

## Python SDK 与 CLI（零依赖）

```bash
pip install feedmcp-sdk
```

```python
from feedmcp import FeedMCPClient

client = FeedMCPClient()  # 自动读取环境变量 FEEDMCP_API_KEY

# 免费搜索接口（无需 Key）
print(client.find("小红书评论"))

# 带单次限价调用
res = client.call("douyin.trends.list", max_price="0.002")
print(res["data"]["items"][:5])
```

命令行：
```bash
feedmcp find "小红书 评论"
feedmcp describe xiaohongshu.notes.comments.list
feedmcp status
feedmcp call douyin.trends.list --max-price 0.002
```

---

## JavaScript / TypeScript SDK 与 CLI（零依赖）

```bash
npm install feedmcp
# 或直接免安装运行 CLI：
npx feedmcp find "抖音 热榜"
```

```js
import { FeedMCPClient } from "feedmcp";

const client = new FeedMCPClient();
const res = await client.call("tiktok.videos.comments.list", { id: "7700200904678559006" }, { maxPrice: "0.002" });
console.log(res.data.items, res.meta.billing);
```

---

## 开源协议与联系

MIT License — 见 [LICENSE](./LICENSE)。问题与需求反馈：[support@feedmcp.com](mailto:support@feedmcp.com)。
