import crypto from "node:crypto";

export const DEFAULT_BASE_URL = "https://api.feedmcp.com";

export class FeedMCPError extends Error {
  constructor(message, details = {}) {
    super(message);
    this.name = "FeedMCPError";
    this.status = details.status ?? 0;
    this.code = details.code ?? "unknown_error";
    this.charged = details.charged ?? false;
    this.retry = details.retry ?? null;
    this.retryAfterSeconds = details.retry_after_seconds ?? null;
    this.requestId = details.request_id ?? null;
    this.topUpUrl = details.top_up_url ?? null;
    this.body = details.body ?? {};
  }
}

export class FeedMCPClient {
  constructor(options = {}) {
    this.apiKey = options.apiKey !== undefined ? options.apiKey : process.env.FEEDMCP_API_KEY;
    this.baseUrl = (options.baseUrl || process.env.FEEDMCP_API_URL || DEFAULT_BASE_URL).replace(/\/$/, "");
    this.timeoutMs = options.timeoutMs ?? 30_000;
  }

  async _request(path, { params = {}, auth = false, maxPrice, idempotencyKey } = {}) {
    const url = new URL(this.baseUrl + path);
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== null) url.searchParams.set(k, String(v));
    }

    const headers = {
      Accept: "application/json",
      "User-Agent": "feedmcp-js/0.1.0",
    };

    if (auth) {
      if (!this.apiKey) {
        throw new FeedMCPError(
          "Missing API key. Set FEEDMCP_API_KEY or pass { apiKey } (get $0.10 free trial at https://feedmcp.com/console/keys/).",
          { status: 401, code: "unauthorized", charged: false, retry: "after_fix" },
        );
      }
      headers.Authorization = `Bearer ${this.apiKey}`;
    }
    if (maxPrice !== undefined && maxPrice !== null) headers["X-Max-Price"] = String(maxPrice);
    if (idempotencyKey !== undefined && idempotencyKey !== null) headers["Idempotency-Key"] = String(idempotencyKey);

    const res = await fetch(url, {
      method: "GET",
      headers,
      signal: AbortSignal.timeout(this.timeoutMs),
    });

    const text = await res.text();
    let data = {};
    if (text) {
      try {
        data = JSON.parse(text);
      } catch {
        data = { message: text };
      }
    }

    if (!res.ok) {
      throw new FeedMCPError(data.message || `HTTP ${res.status}`, {
        ...data,
        status: res.status,
        code: data.code || `http_${res.status}`,
        body: data,
      });
    }
    return data;
  }

  // Free discovery endpoints (no API key required)
  catalog() {
    return this._request("/v1/catalog");
  }

  find(query, options = {}) {
    return this._request("/v1/catalog/search", { params: { q: query, platform: options.platform } });
  }

  describe(endpointId) {
    return this._request(`/v1/catalog/endpoints/${encodeURIComponent(endpointId)}`);
  }

  prices() {
    return this._request("/v1/catalog/prices");
  }

  status() {
    return this._request("/v1/catalog/status");
  }

  // Authenticated endpoints
  account() {
    return this._request("/v1/me", { auth: true });
  }

  call(endpointId, params = {}, options = {}) {
    const path = "/v1/" + endpointId.replace(/^\/+/, "").replace(/\./g, "/");
    const merged = { ...params, ...(options.view ? { view: options.view } : {}) };
    return this._request(path, {
      params: merged,
      auth: true,
      maxPrice: options.maxPrice,
      idempotencyKey: options.idempotencyKey,
    });
  }

  async *paginate(endpointId, params = {}, options = {}) {
    const maxPages = options.maxPages ?? 5;
    let cursor;
    for (let i = 0; i < maxPages; i++) {
      const pageParams = { ...params, ...(cursor ? { cursor } : {}) };
      const body = await this.call(endpointId, pageParams, {
        maxPrice: options.maxPrice,
        view: options.view,
        idempotencyKey: crypto.randomUUID(),
      });
      yield body;
      cursor = body?.page?.next_cursor ?? null;
      if (!cursor || body?.page?.has_more === false) break;
    }
  }
}
