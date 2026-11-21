export declare const DEFAULT_BASE_URL: string;

export interface FeedMCPClientOptions {
  apiKey?: string;
  baseUrl?: string;
  timeoutMs?: number;
}

export interface CallOptions {
  maxPrice?: string | number;
  idempotencyKey?: string;
  view?: "standard" | "full";
}

export interface PaginateOptions extends Omit<CallOptions, "idempotencyKey"> {
  maxPages?: number;
}

export class FeedMCPError extends Error {
  readonly status: number;
  readonly code: string;
  readonly charged: boolean | null;
  readonly retry: string | null;
  readonly retryAfterSeconds: number | null;
  readonly requestId: string | null;
  readonly topUpUrl: string | null;
  readonly body: Record<string, unknown>;
}

export class FeedMCPClient {
  constructor(options?: FeedMCPClientOptions);
  catalog(): Promise<Record<string, unknown>>;
  find(query: string, options?: { platform?: string }): Promise<{ items: Record<string, unknown>[] }>;
  describe(endpointId: string): Promise<Record<string, unknown>>;
  prices(): Promise<{ revision: string; currency: string; endpoints: Record<string, unknown>[] }>;
  status(): Promise<{ platforms: Array<{ platform: string; state: string; checked_at?: string }> }>;
  account(): Promise<Record<string, unknown>>;
  call(endpointId: string, params?: Record<string, unknown>, options?: CallOptions): Promise<Record<string, any>>;
  paginate(endpointId: string, params?: Record<string, unknown>, options?: PaginateOptions): AsyncGenerator<Record<string, any>>;
}
