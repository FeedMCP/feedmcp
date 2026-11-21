"""Export paginated comments from any FeedMCP comment endpoint to CSV.

Usage:
  export FEEDMCP_API_KEY="fmk_live_..."
  python examples/python_comments_csv.py tiktok.videos.comments.list 7700200904678559006 out.csv 3 0.002
"""

import csv
import sys
from feedmcp import FeedMCPClient


def main() -> None:
    if len(sys.argv) < 3:
        print("Usage: python python_comments_csv.py <endpoint_id> <post_id> [out.csv] [max_pages] [max_price]")
        sys.exit(1)

    endpoint_id = sys.argv[1]
    post_id = sys.argv[2]
    out_csv = sys.argv[3] if len(sys.argv) > 3 else "comments.csv"
    max_pages = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    max_price = sys.argv[5] if len(sys.argv) > 5 else "0.02"

    client = FeedMCPClient()
    rows = []
    for page in client.paginate(endpoint_id, {"id": post_id}, max_pages=max_pages, max_price=max_price):
        rows.extend(page.get("data", {}).get("items", []))

    with open(out_csv, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "author", "likes", "reply_count", "created_at", "text"])
        for c in rows:
            writer.writerow([
                c.get("id"),
                (c.get("author") or {}).get("name"),
                c.get("likes"),
                c.get("reply_count"),
                c.get("created_at"),
                c.get("text"),
            ])

    print(f"Saved {len(rows)} comments to {out_csv}")


if __name__ == "__main__":
    main()
