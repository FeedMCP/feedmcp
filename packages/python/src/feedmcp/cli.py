"""Minimal CLI for FeedMCP: find, describe, prices, status, call, account."""

from __future__ import annotations

import argparse
import json
import sys
from typing import Dict, List, Optional

from .client import FeedMCPClient, FeedMCPError


def _parse_kv(pairs: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for item in pairs:
        if "=" not in item:
            raise ValueError(f"Expected key=value parameter, got: {item}")
        k, v = item.split("=", 1)
        out[k] = v
    return out


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="feedmcp",
        description="FeedMCP CLI — query 21 social media & ad library platforms (193 endpoints).",
    )
    parser.add_argument("--api-key", help="API key (defaults to FEEDMCP_API_KEY)")
    parser.add_argument("--base-url", help="Override API base URL (defaults to https://api.feedmcp.com)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_find = sub.add_parser("find", help="Search endpoints in plain words (free, no key)")
    p_find.add_argument("query", help="Search query, e.g. 'tiktok comments'")
    p_find.add_argument("--platform", help="Limit to one platform slug")

    p_desc = sub.add_parser("describe", help="Show parameters, fields and price for one endpoint (free)")
    p_desc.add_argument("endpoint", help="Endpoint ID, e.g. douyin.trends.list")

    p_prices = sub.add_parser("prices", help="Show live USD price book (free)")
    p_prices.add_argument("--platform", help="Filter by platform prefix, e.g. tiktok")

    sub.add_parser("status", help="Show live health status for all 21 platforms (free)")
    sub.add_parser("account", help="Show balance for FEEDMCP_API_KEY")

    p_call = sub.add_parser("call", help="Call a data endpoint by ID (requires FEEDMCP_API_KEY)")
    p_call.add_argument("endpoint", help="Endpoint ID, e.g. douyin.trends.list")
    p_call.add_argument("-p", "--param", action="append", default=[], help="Query parameter as key=value (repeatable)")
    p_call.add_argument("--max-price", help="Maximum USD allowed for this call (X-Max-Price)")
    p_call.add_argument("--idempotency-key", help="Idempotency-Key for safe retries")
    p_call.add_argument("--view", choices=["standard", "full"], help="Optional response view")

    args = parser.parse_args(argv)
    client = FeedMCPClient(api_key=args.api_key, base_url=args.base_url)

    try:
        if args.cmd == "find":
            out = client.find(args.query, platform=args.platform)
        elif args.cmd == "describe":
            out = client.describe(args.endpoint)
        elif args.cmd == "prices":
            out = client.prices()
            if args.platform:
                prefix = args.platform + "."
                out["endpoints"] = [e for e in out.get("endpoints", []) if e.get("id", "").startswith(prefix)]
        elif args.cmd == "status":
            out = client.status()
        elif args.cmd == "account":
            out = client.account()
        elif args.cmd == "call":
            params = _parse_kv(args.param)
            out = client.call(
                args.endpoint,
                params,
                max_price=args.max_price,
                idempotency_key=args.idempotency_key,
                view=args.view,
            )
        else:
            parser.print_help()
            return 2
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except (FeedMCPError, ValueError) as exc:
        if isinstance(exc, FeedMCPError):
            print(json.dumps({"error": exc.code, "message": str(exc), "charged": exc.charged, "retry": exc.retry, "top_up_url": exc.top_up_url}, ensure_ascii=False, indent=2), file=sys.stderr)
        else:
            print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
