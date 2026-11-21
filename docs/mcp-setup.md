# FeedMCP Setup Guides for AI Clients & Workflows

- **Remote MCP URL**: `https://api.feedmcp.com/mcp` (`Streamable HTTP`)
- **HTTP Base URL**: `https://api.feedmcp.com`
- **OpenAPI 3.1**: `https://feedmcp.com/openapi.json`
- **Get a free `$0.10` trial API key (no card)**: `https://feedmcp.com/console/keys/`

---

## 1. Claude Code
```bash
export FEEDMCP_API_KEY="fmk_live_YOUR_KEY"
claude mcp add --transport http feedmcp https://api.feedmcp.com/mcp \
  --header "Authorization: Bearer $FEEDMCP_API_KEY"
```

## 2. Claude Desktop
Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):
```json
{
  "mcpServers": {
    "feedmcp": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://api.feedmcp.com/mcp",
        "--header",
        "Authorization: Bearer fmk_live_YOUR_KEY"
      ]
    }
  }
}
```

## 3. Cursor
Add to `~/.cursor/mcp.json`:
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

## 4. OpenAI Codex CLI
Add to `~/.codex/config.toml`:
```toml
[mcp_servers.feedmcp]
url = "https://api.feedmcp.com/mcp"
http_headers = { Authorization = "Bearer fmk_live_YOUR_KEY" }
```

## 5. Windsurf
Add to `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "feedmcp": {
      "serverUrl": "https://api.feedmcp.com/mcp",
      "headers": {
        "Authorization": "Bearer fmk_live_YOUR_KEY"
      }
    }
  }
}
```

## 6. Cherry Studio / WorkBuddy / Qwen-Agent
- **Transport**: Streamable HTTP
- **URL**: `https://api.feedmcp.com/mcp`
- **Header**: `Authorization: Bearer fmk_live_YOUR_KEY`

## 7. ChatGPT (Custom GPT Actions), Coze, Dify & n8n
- Import `https://feedmcp.com/openapi.json` (or select the subset of endpoints you need).
- Set authentication to **Bearer API Key** (`Authorization: Bearer fmk_live_YOUR_KEY`).
- Always pass `X-Max-Price` and `Idempotency-Key` in automated workflow nodes.

Full client-by-client guides: https://feedmcp.com/integrations/
