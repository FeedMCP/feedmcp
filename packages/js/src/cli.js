#!/usr/bin/env node
import { FeedMCPClient, FeedMCPError } from "./index.js";

function usage() {
  console.log(`FeedMCP CLI — query 21 social media & ad library platforms (193 endpoints)

Usage:
  feedmcp find <query> [--platform <slug>]
  feedmcp describe <endpoint_id>
  feedmcp prices [--platform <slug>]
  feedmcp status
  feedmcp account
  feedmcp call <endpoint_id> [-p key=value ...] [--max-price <usd>] [--idempotency-key <key>] [--view standard|full]

Options:
  --api-key <key>      Override FEEDMCP_API_KEY
  --base-url <url>     Override https://api.feedmcp.com
`);
}

function parseArgs(argv) {
  const pos = [];
  const opts = { params: {} };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "-h" || a === "--help") opts.help = true;
    else if (a === "--api-key") opts.apiKey = argv[++i];
    else if (a === "--base-url") opts.baseUrl = argv[++i];
    else if (a === "--platform") opts.platform = argv[++i];
    else if (a === "--max-price") opts.maxPrice = argv[++i];
    else if (a === "--idempotency-key") opts.idempotencyKey = argv[++i];
    else if (a === "--view") opts.view = argv[++i];
    else if (a === "-p" || a === "--param") {
      const kv = argv[++i] || "";
      const idx = kv.indexOf("=");
      if (idx === -1) throw new Error(`Expected key=value, got: ${kv}`);
      opts.params[kv.slice(0, idx)] = kv.slice(idx + 1);
    } else if (a.startsWith("-")) {
      throw new Error(`Unknown flag: ${a}`);
    } else {
      pos.push(a);
    }
  }
  return { pos, opts };
}

async function main() {
  const { pos, opts } = parseArgs(process.argv.slice(2));
  const [cmd, ...rest] = pos;
  if (!cmd || opts.help) {
    usage();
    process.exit(0);
  }

  const client = new FeedMCPClient({ apiKey: opts.apiKey, baseUrl: opts.baseUrl });
  let out;
  if (cmd === "find") {
    if (!rest.length) throw new Error("Missing search query");
    out = await client.find(rest.join(" "), { platform: opts.platform });
  } else if (cmd === "describe") {
    if (!rest[0]) throw new Error("Missing endpoint ID");
    out = await client.describe(rest[0]);
  } else if (cmd === "prices") {
    out = await client.prices();
    if (opts.platform) {
      const prefix = opts.platform + ".";
      out.endpoints = (out.endpoints || []).filter((e) => String(e.id || "").startsWith(prefix));
    }
  } else if (cmd === "status") {
    out = await client.status();
  } else if (cmd === "account") {
    out = await client.account();
  } else if (cmd === "call") {
    if (!rest[0]) throw new Error("Missing endpoint ID");
    out = await client.call(rest[0], opts.params, {
      maxPrice: opts.maxPrice,
      idempotencyKey: opts.idempotencyKey,
      view: opts.view,
    });
  } else {
    throw new Error(`Unknown command: ${cmd}`);
  }
  console.log(JSON.stringify(out, null, 2));
}

main().catch((err) => {
  if (err instanceof FeedMCPError) {
    console.error(JSON.stringify({ error: err.code, message: err.message, charged: err.charged, retry: err.retry, top_up_url: err.topUpUrl }, null, 2));
  } else {
    console.error(err.message || String(err));
  }
  process.exit(1);
});
