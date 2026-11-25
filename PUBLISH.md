# FeedMCP 站外高权重信源发布清单（GitHub / PyPI / npm / Context7 / MCP 目录）

这个目录（`feedmcp-public`）完全独立于你的私有后端仓库，不含任何上游信息或密钥，可直接整仓开源发布。

---

## 1. 发布到 GitHub（创建组织 `feedmcp` + 仓库 `feedmcp/feedmcp`）

1. 在 GitHub 新建组织 `feedmcp`（若已被占，可用 `feedmcp-hq` 或你的个人账号并同步替换 `README.md`、`server.json`、`pyproject.toml`、`package.json` 中的仓库 URL）。
2. 创建公开仓库 `feedmcp`，推送本目录：
   ```bash
   cd /Users/fuhaikui/Downloads/大数据项目/创业项目/feedmcp-public
   git init -b main
   git add .
   git commit -m "Initial public release: FeedMCP docs, MCP manifest, Python & JS SDKs v0.1.0"
   git remote add origin https://github.com/feedmcp/feedmcp.git
   git push -u origin main
   ```
3. 在 GitHub 仓库右上角 **About** 填好：
   - **Website**: `https://feedmcp.com/?utm_source=github`
   - **Description**: `Social media data MCP server & pay-per-call API for 21 global and Chinese platforms (TikTok, YouTube, Instagram, X, Xiaohongshu, Douyin, WeChat).`
   - **Topics**: `mcp`, `mcp-server`, `social-media-api`, `tiktok`, `youtube`, `instagram`, `twitter`, `xiaohongshu`, `douyin`, `wechat`, `ai-agent`

---

## 2. 发布 Python SDK 到 PyPI（`pip install feedmcp`）

```bash
cd /Users/fuhaikui/Downloads/大数据项目/创业项目/feedmcp-public/packages/python
python3 -m pip install --upgrade build twine
python3 -m build
python3 -m twine upload dist/*
```
*(若 `feedmcp` 包名已被占用，把 `pyproject.toml` 中的 `name` 改为 `feedmcp-sdk` 或 `feedmcp-client` 即可。)*

---

## 3. 发布 JS/TS SDK & CLI 到 npm（`npm install feedmcp` / `npx feedmcp`）

```bash
cd /Users/fuhaikui/Downloads/大数据项目/创业项目/feedmcp-public/packages/js
npm login
npm publish --access public
```
*(若 `feedmcp` 包名已被占用，改为 `@feedmcp/sdk` 或 `feedmcp-cli` 即可。)*

---

## 4. 提交到 Context7（让 Cursor / Claude Code 写代码时自动检索 FeedMCP）

1. 打开 https://context7.com/add-library
2. 填入你的 GitHub 仓库地址：`https://github.com/feedmcp/feedmcp`
3. 本仓库根目录已放好 `context7.json`，Context7 会自动索引 `docs/`、`examples/`、`packages/python/` 和 `packages/js/`。

---

## 5. 登记到 Official MCP Registry & 5 大 MCP 导航站

1. **Official MCP Registry**（`registry.modelcontextprotocol.io`）：本仓库根目录已按官方 schema 准备好 `server.json`（名称 `com.feedmcp/mcp`，远程 `streamable-http` 地址 `https://api.feedmcp.com/mcp`）。按官方文档使用 `mcp-publisher` 工具完成域名 DNS/HTTP 验证后一键发布：
   ```bash
   mcp-publisher login dns --domain feedmcp.com
   mcp-publisher publish
   ```
2. **Smithery**（https://smithery.ai/new）— 提交 `https://github.com/feedmcp/feedmcp` 和远程端点 `https://api.feedmcp.com/mcp`。
3. **Glama**（https://glama.ai/mcp/servers）— 提交 GitHub 仓库与 `https://api.feedmcp.com/mcp`。
4. **PulseMCP**（https://www.pulsemcp.com/submit）— 提交官网与 GitHub 仓库。
5. **mcp.so**（https://mcp.so/submit）— 提交中文 + 英文介绍。
6. **awesome-mcp-servers（GitHub PR）**— 在 *Social Media / Data / Marketing* 分类提交一行 PR：
   ```markdown
   - [FeedMCP](https://github.com/FeedMCP/feedmcp) - Hosted social media data MCP server & API covering 21 global and Chinese platforms (TikTok, YouTube, Instagram, X, Xiaohongshu, Douyin, WeChat, ad libraries, TikTok Shop), pay-per-call with failed calls free.
   ```

---

## 6. P2 高权重 Awesome 榜单与 AI 目录 PR 矩阵（对标 DataXAPI / Qovia / AIsa）

以下 10 个高星仓库是大模型（ChatGPT Search、Perplexity、Claude、DeepSeek）交叉验证 MCP 和 API 权威度的核心信源，建议依次提交 PR：

| # | 目标仓库 | 分类位置 | 提交文案（直接复制） |
|---|---|---|---|
| 1 | `punkpeye/awesome-remote-mcp-servers` | Social Media / Data | `- [FeedMCP](https://feedmcp.com/mcp/?utm_source=github&utm_campaign=awesome-remote-mcp) ([`https://api.feedmcp.com/mcp`](https://api.feedmcp.com/mcp)) - Public social media, creator marketing & ad library data across 21 global and Chinese platforms (TikTok, YouTube, Instagram, X, Xiaohongshu, Douyin, WeChat). Streamable HTTP, pay-per-call, failed calls free.` |
| 2 | `jaw9c/awesome-remote-mcp-servers` | Data & Marketing | 同上 |
| 3 | `TensorBlock/awesome-mcp-servers` | Social Media | `- [FeedMCP](https://github.com/FeedMCP/feedmcp) - Unified social media data MCP server and REST API for 21 platforms (193 endpoints: TikTok, YouTube, X, Instagram, Reddit, Meta/Google Ads, Xiaohongshu, Douyin, WeChat).` |
| 4 | `YinTokey/Awesome-MCP-ZH`（或同类中文 MCP 榜） | 社交媒体与数据 | `- [FeedMCP 社媒数据 MCP](https://feedmcp.com/zh/mcp/?utm_source=github&utm_campaign=awesome-mcp-zh)（[GitHub](https://github.com/FeedMCP/feedmcp)）- 远程 Streamable HTTP MCP 服务器，一把 Key 读取小红书（含蒲公英）、抖音（含星图与巨量算数）、微信公众号/视频号/微信指数、微博、B 站、知乎、TikTok、YouTube、X 及四大广告库（21 平台 193 接口，按次计费，失败不收费）。` |
| 5 | `zackchewa/awesome-china-mcp` | Social Media & Content | `- [FeedMCP](https://github.com/FeedMCP/feedmcp) - Hosted remote MCP server for Chinese & global social media data: Xiaohongshu (RedNote + PGY), Douyin (Xingtu + Ocean Engine), WeChat Official Accounts/Channels/Index, Weibo, Bilibili, Zhihu, Kuaishou ($0.002/call, no login or cookies required).` |
| 6 | `thedaviddias/llms-txt-hub` | Developer Tools / APIs | 提交站点 `https://feedmcp.com`、`https://feedmcp.com/llms.txt` 与 `https://feedmcp.com/llms-full.txt` |
| 7 | `karanb192/awesome-claude-skills` | Data & Research Skills | `- [feedmcp](https://feedmcp.com/.well-known/agent-skills/feedmcp/SKILL.md) ([Repo](https://github.com/FeedMCP/feedmcp)) - Query live public social media, influencer rate cards, ad libraries, and video transcripts across 21 global and Chinese platforms with spend guardrails.` |
| 8 | `UnderleveledBuilder/awesome-social-media-skills` | 数据采集与分析 | `- [FeedMCP 社媒数据 Skill](https://github.com/FeedMCP/feedmcp/blob/main/SKILL.md) - 免登录读取小红书、抖音、公众号、视频号、B 站、TikTok、YouTube、X 的帖子、评论、热搜榜、字幕与达人报价，支持 Claude Code、Cursor、WorkBuddy、OpenClaw。` |
| 9 | `public-apis/public-apis` & `marcelscruz/public-apis` | Social | `| [FeedMCP](https://feedmcp.com/docs/?utm_source=github&utm_campaign=public-apis) | Unified public social media, creator & ad library data across 21 global and Chinese platforms | `apiKey` | Yes | Yes |` |
| 10 | `1c7/chinese-independent-developer` | 开发工具 / 数据接口 | `- [FeedMCP 社媒数据 MCP & API](https://feedmcp.com/zh/?utm_source=github&utm_campaign=chinese-indie)：让 AI（Claude、Cursor、WorkBuddy、DeepSeek、豆包）直接读取小红书、抖音、微信公众号、视频号、微博、B 站、TikTok、YouTube、X 等 21 个平台公开数据，按次计费，失败不收费。` |

---

## 7. 站外渠道 UTM 归因规范（与 `/admin` 后台归因规则对齐）

所有**面向人点击的网页链接**按渠道统一加 `?utm_source=...`（`llms.txt`、`agents.md`、`openapi.json`、`prices.json`、`/.well-known/*` 和 `https://api.feedmcp.com/*` 等机器接口保持干净不加参数）：

| 发布渠道 | 推荐链接后缀 | `/admin` 归类结果 |
| --- | --- | --- |
| GitHub README / About / Awesome PR | `?utm_source=github`（可附加 `&utm_campaign=xxx`） | `github` (`dev`) |
| npm 包页面 (`feedmcp`) | `?utm_source=npm` | `npm` (`dev`) |
| PyPI 包页面 (`feedmcp-sdk`) | `?utm_source=pypi` | `pypi` (`dev`) |
| Glama 目录 | `?utm_source=glama` | `glama` (`directory`) |
| Smithery 目录 | `?utm_source=smithery` | `smithery` (`directory`) |
| PulseMCP / mcp.so / Context7 | `?utm_source=pulsemcp` / `mcp.so` / `context7` | `directory` |
| 知乎 / 掘金 / CSDN / V2EX | `?utm_source=zhihu` / `juejin` / `csdn` / `v2ex` | 对应独立渠道行 |
| Dev.to / Medium / Hashnode / Reddit / X | `?utm_source=devto` / `medium` / `hashnode` / `reddit` / `x` | 对应独立渠道行 |
| 小红书 / 微信公众号 / 微信群 | `?utm_source=xiaohongshu` / `wechat` | `social` |
