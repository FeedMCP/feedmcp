"""Zero-dependency HTTP client for the FeedMCP API (https://feedmcp.com)."""

from __future__ import annotations

import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any, Dict, Iterator, Optional

DEFAULT_BASE_URL = "https://api.feedmcp.com"


def _ssl_context() -> ssl.SSLContext:
    try:
        import certifi  # type: ignore

        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


class FeedMCPError(Exception):
    """Structured error returned by the FeedMCP API."""

    def __init__(
        self,
        message: str,
        *,
        status: int = 0,
        code: str = "unknown_error",
        charged: Optional[bool] = False,
        retry: Optional[str] = None,
        retry_after_seconds: Optional[int] = None,
        request_id: Optional[str] = None,
        top_up_url: Optional[str] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.charged = charged
        self.retry = retry
        self.retry_after_seconds = retry_after_seconds
        self.request_id = request_id
        self.top_up_url = top_up_url
        self.body = body or {}


class FeedMCPClient:
    """Thin client for FeedMCP discovery and pay-per-call data endpoints."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ) -> None:
        self.api_key = api_key if api_key is not None else os.environ.get("FEEDMCP_API_KEY")
        self.base_url = (base_url or os.environ.get("FEEDMCP_API_URL") or DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout

    def _request(
        self,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        auth: bool = False,
        max_price: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        query_items = [(k, str(v)) for k, v in (params or {}).items() if v is not None]
        qs = urllib.parse.urlencode(query_items)
        url = f"{self.base_url}{path}" + (f"?{qs}" if qs else "")

        headers = {
            "Accept": "application/json",
            "User-Agent": "feedmcp-python/0.1.0",
        }
        if auth:
            if not self.api_key:
                raise FeedMCPError(
                    "Missing API key. Set FEEDMCP_API_KEY or pass api_key=... (get $0.10 free trial at https://feedmcp.com/console/keys/).",
                    status=401,
                    code="unauthorized",
                    charged=False,
                    retry="after_fix",
                )
            headers["Authorization"] = f"Bearer {self.api_key}"
        if max_price is not None:
            headers["X-Max-Price"] = str(max_price)
        if idempotency_key is not None:
            headers["Idempotency-Key"] = str(idempotency_key)

        req = urllib.request.Request(url, headers=headers, method="GET")
        try:
            ctx = _ssl_context() if url.startswith("https://") else None
            with urllib.request.urlopen(req, timeout=self.timeout, context=ctx) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                data = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                data = {"message": raw or str(exc)}
            raise FeedMCPError(
                data.get("message") or f"HTTP {exc.code}",
                status=exc.code,
                code=data.get("code") or f"http_{exc.code}",
                charged=data.get("charged", False),
                retry=data.get("retry"),
                retry_after_seconds=data.get("retry_after_seconds"),
                request_id=data.get("request_id"),
                top_up_url=data.get("top_up_url"),
                body=data,
            ) from exc

    # ---------------- Free discovery (no API key required) ----------------

    def catalog(self) -> Dict[str, Any]:
        """Return the full catalog of platforms, endpoints, parameters and prices (free)."""
        return self._request("/v1/catalog")

    def find(self, query: str, *, platform: Optional[str] = None) -> Dict[str, Any]:
        """Search endpoints in plain words (free, no key required)."""
        return self._request("/v1/catalog/search", params={"q": query, "platform": platform})

    def describe(self, endpoint_id: str) -> Dict[str, Any]:
        """Inspect parameters, response shape and price for one endpoint ID (free)."""
        safe = urllib.parse.quote(endpoint_id, safe="")
        return self._request(f"/v1/catalog/endpoints/{safe}")

    def prices(self) -> Dict[str, Any]:
        """Return the live USD price book for all endpoints (free)."""
        return self._request("/v1/catalog/prices")

    def status(self) -> Dict[str, Any]:
        """Return current health status for all 21 platforms (free)."""
        return self._request("/v1/catalog/status")

    # ---------------- Authenticated endpoints ----------------

    def account(self) -> Dict[str, Any]:
        """Check remaining account balance and email (requires API key)."""
        return self._request("/v1/me", auth=True)

    def call(
        self,
        endpoint_id: str,
        params: Optional[Dict[str, Any]] = None,
        *,
        max_price: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        view: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Call any FeedMCP data endpoint by ID (e.g. 'tiktok.videos.comments.list')."""
        path = "/v1/" + endpoint_id.lstrip("/").replace(".", "/")
        merged = dict(params or {})
        if view is not None:
            merged["view"] = view
        return self._request(
            path,
            params=merged,
            auth=True,
            max_price=max_price,
            idempotency_key=idempotency_key,
        )

    def paginate(
        self,
        endpoint_id: str,
        params: Optional[Dict[str, Any]] = None,
        *,
        max_pages: int = 5,
        max_price: Optional[str] = None,
        view: Optional[str] = None,
    ) -> Iterator[Dict[str, Any]]:
        """Yield up to max_pages pages from a list endpoint using page.next_cursor."""
        cursor: Optional[str] = None
        for _ in range(max_pages):
            page_params = dict(params or {})
            if cursor is not None:
                page_params["cursor"] = cursor
            body = self.call(
                endpoint_id,
                page_params,
                max_price=max_price,
                idempotency_key=str(uuid.uuid4()),
                view=view,
            )
            yield body
            page = body.get("page") or {}
            cursor = page.get("next_cursor")
            if not cursor or not page.get("has_more", True):
                break
