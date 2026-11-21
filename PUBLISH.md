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
   - **Website**: `https://feedmcp.com`
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
   - [FeedMCP](https://github.com/feedmcp/feedmcp) - Hosted social media data MCP server & API covering 21 global and Chinese platforms (TikTok, YouTube, Instagram, X, Xiaohongshu, Douyin, WeChat, ad libraries, TikTok Shop), pay-per-call with failed calls free.
   ```
