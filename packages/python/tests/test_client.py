import http.server
import json
import threading
import unittest

from feedmcp import FeedMCPClient, FeedMCPError


class _Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path.startswith("/v1/catalog/search"):
            self._send(200, {"items": [{"id": "douyin.trends.list", "price": "0.002"}]})
        elif self.path.startswith("/v1/douyin/trends/list"):
            if self.headers.get("Authorization") != "Bearer fmk_live_test":
                self._send(401, {"code": "unauthorized", "message": "Invalid key", "charged": False, "retry": "after_fix"})
                return
            if self.headers.get("X-Max-Price") == "0.001":
                self._send(402, {"code": "price_above_max", "message": "Exceeds max", "charged": False, "retry": "after_fix"})
                return
            cursor = "p2" if "cursor=p1" not in self.path else None
            self._send(200, {
                "code": "ok",
                "data": {"items": [{"title": "Trend 1"}]},
                "page": {"next_cursor": "p1" if cursor else None, "has_more": bool(cursor)},
                "meta": {"billing": {"charged": True, "amount": "0.002", "currency": "USD"}},
            })
        else:
            self._send(404, {"code": "unknown_endpoint", "message": "Not found", "charged": False})

    def _send(self, code, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


class FeedMCPClientTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        cls.base_url = f"http://127.0.0.1:{cls.server.server_port}"
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_find_free_without_key(self):
        client = FeedMCPClient(api_key="", base_url=self.base_url)
        res = client.find("douyin")
        self.assertEqual(res["items"][0]["id"], "douyin.trends.list")

    def test_call_and_paginate(self):
        client = FeedMCPClient(api_key="fmk_live_test", base_url=self.base_url)
        pages = list(client.paginate("douyin.trends.list", max_pages=5, max_price="0.002"))
        self.assertEqual(len(pages), 2)
        self.assertEqual(pages[0]["data"]["items"][0]["title"], "Trend 1")

    def test_structured_error(self):
        client = FeedMCPClient(api_key="fmk_live_test", base_url=self.base_url)
        with self.assertRaises(FeedMCPError) as ctx:
            client.call("douyin.trends.list", max_price="0.001")
        self.assertEqual(ctx.exception.code, "price_above_max")
        self.assertFalse(ctx.exception.charged)


if __name__ == "__main__":
    unittest.main()
