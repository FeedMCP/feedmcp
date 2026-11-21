# Spend Guardrails & Error Handling

FeedMCP is designed so autonomous AI agents and scheduled scripts can never run up runaway bills or get double-charged on network retries.

## 1. Three Layers of Spend Control
1. **Per-Key Spend Cap**: Create a separate key per agent or workflow in `https://feedmcp.com/console/keys/` and set a hard USD cap. Once reached, calls fail cleanly with `key_spend_cap_reached` (`charged: false`).
2. **Per-Call Ceiling (`X-Max-Price` / `max_price`)**: Pass `X-Max-Price: 0.02` in HTTP headers (or `max_price: "0.02"` in MCP `call`). Any endpoint priced above your ceiling is rejected before calling upstream (`price_above_max`, `charged: false`).
3. **24-Hour Idempotency (`Idempotency-Key`)**: Pass a UUID in `Idempotency-Key` when retrying uncertain timeouts. The same key + request within 24 hours replays the original response (`Idempotent-Replayed: true`) with zero extra charge.

## 2. Deterministic Error Handling
Every error response includes:
- `code` — machine-readable error code
- `charged` — always `false` on errors
- `retry` — `no` | `yes` | `once` | `after_fix` | `same_key`
- `retry_after_seconds` — suggested backoff when rate-limited

Never loop on `insufficient_balance` (HTTP 402), `key_spend_cap_reached`, `not_found`, `invalid_params`, or `video_too_long`.

Full error table: https://feedmcp.com/docs/errors/
