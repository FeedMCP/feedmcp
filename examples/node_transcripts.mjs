/**
 * Fetch normalized video transcripts across YouTube, TikTok, Instagram, X, LinkedIn, Reddit, and Meta Ads.
 *
 * Usage:
 *   export FEEDMCP_API_KEY="fmk_live_..."
 *   node examples/node_transcripts.mjs youtube dQw4w9WgXcQ
 */
import { FeedMCPClient, FeedMCPError } from "../packages/js/src/index.js";

const ENDPOINTS = {
  youtube: "youtube.videos.transcript.get",
  tiktok: "tiktok.videos.transcript.get",
  instagram: "instagram.posts.transcript.get",
  x: "x.posts.transcript.get",
  linkedin: "linkedin.posts.transcript.get",
  reddit: "reddit.posts.transcript.get",
  meta: "meta.ads.transcript.get",
};

const [platform, id] = process.argv.slice(2);
if (!platform || !id || !ENDPOINTS[platform]) {
  console.error(`Usage: node node_transcripts.mjs <${Object.keys(ENDPOINTS).join("|")}> <id>`);
  process.exit(1);
}

const client = new FeedMCPClient();
try {
  const res = await client.call(ENDPOINTS[platform], { id }, { maxPrice: "0.002" });
  const item = res.data.item;
  console.log("Source:", item.source, "| Cost: $" + res.meta.billing.amount);
  console.log(item.text);
} catch (err) {
  if (err instanceof FeedMCPError) {
    console.error(`Error [${err.code}] charged=${err.charged} retry=${err.retry}: ${err.message}`);
    process.exit(1);
  }
  throw err;
}
