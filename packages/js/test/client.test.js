import assert from "node:assert/strict";
import http from "node:http";
import test from "node:test";
import { FeedMCPClient, FeedMCPError } from "../src/index.js";

function startMockServer() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const url = new URL(req.url, "http://127.0.0.1");
      const send = (status, payload) => {
        res.writeHead(status, { "Content-Type": "application/json" });
        res.end(JSON.stringify(payload));
      };
      if (url.pathname === "/v1/catalog/search") {
        send(200, { items: [{ id: "tiktok.videos.comments.list", price: "0.002" }] });
      } else if (url.pathname === "/v1/tiktok/videos/comments/list") {
        if (req.headers.authorization !== "Bearer fmk_live_test") {
          send(401, { code: "unauthorized", message: "Bad key", charged: false, retry: "after_fix" });
          return;
        }
        if (req.headers["x-max-price"] === "0.001") {
          send(402, { code: "price_above_max", message: "Too expensive", charged: false, retry: "after_fix" });
          return;
        }
        const hasCursor = url.searchParams.get("cursor") === "c1";
        send(200, {
          code: "ok",
          data: { items: [{ id: hasCursor ? "2" : "1", text: "Hello" }] },
          page: { next_cursor: hasCursor ? null : "c1", has_more: !hasCursor },
          meta: { billing: { charged: true, amount: "0.002", currency: "USD" } },
        });
      } else {
        send(404, { code: "unknown_endpoint", message: "Not found", charged: false });
      }
    });
    server.listen(0, "127.0.0.1", () => {
      const addr = server.address();
      resolve({ server, baseUrl: `http://127.0.0.1:${addr.port}` });
    });
  });
}

test("FeedMCPClient discovery, pagination, and structured errors", async () => {
  const { server, baseUrl } = await startMockServer();
  try {
    const free = new FeedMCPClient({ apiKey: "", baseUrl });
    const hits = await free.find("tiktok");
    assert.equal(hits.items[0].id, "tiktok.videos.comments.list");

    const authed = new FeedMCPClient({ apiKey: "fmk_live_test", baseUrl });
    const pages = [];
    for await (const p of authed.paginate("tiktok.videos.comments.list", { id: "123" }, { maxPages: 5, maxPrice: "0.002" })) {
      pages.push(p);
    }
    assert.equal(pages.length, 2);
    assert.equal(pages[1].data.items[0].id, "2");

    await assert.rejects(
      () => authed.call("tiktok.videos.comments.list", { id: "123" }, { maxPrice: "0.001" }),
      (err) => err instanceof FeedMCPError && err.code === "price_above_max" && err.charged === false,
    );
  } finally {
    server.close();
  }
});
