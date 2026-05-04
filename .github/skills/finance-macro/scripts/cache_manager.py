#!/usr/bin/env python3
"""SQLite-based data cache for macro-finance skills.

Prevents redundant API calls and respects rate limits. Each data source
gets its own table. Cache TTL is configurable per source.

Usage:
    python3 cache_manager.py get fred GDP 2024-01-01 2024-12-31
    python3 cache_manager.py set fred GDP '{"data": [...]}'
    python3 cache_manager.py purge fred --older-than 7d
    python3 cache_manager.py stats
"""

import json
import sqlite3
import time
import sys
from datetime import datetime, timedelta
from pathlib import Path

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache"
CACHE_DB = CACHE_DIR / "macro_cache.db"

DEFAULT_TTL = {
    "fred": 3600,
    "worldbank": 86400,
    "imf": 86400,
    "bis": 43200,
    "stats": 3600,
    "ecb": 3600,
    "news": 1800,
}


def _ensure_db():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(CACHE_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cache (
            source TEXT NOT NULL,
            series_id TEXT NOT NULL,
            params TEXT NOT NULL DEFAULT '',
            data TEXT NOT NULL,
            fetched_at REAL NOT NULL,
            PRIMARY KEY (source, series_id, params)
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_cache_fetched
        ON cache(source, fetched_at)
    """)
    conn.commit()
    return conn


def get(source, series_id, params=""):
    conn = _ensure_db()
    row = conn.execute(
        "SELECT data, fetched_at FROM cache WHERE source=? AND series_id=? AND params=?",
        (source, series_id, params),
    ).fetchone()
    conn.close()

    if not row:
        return None

    data_str, fetched_at = row
    ttl = DEFAULT_TTL.get(source, 3600)
    age = time.time() - fetched_at

    if age > ttl:
        return None

    try:
        return json.loads(data_str)
    except (json.JSONDecodeError, TypeError):
        return None


def set(source, series_id, data, params=""):
    conn = _ensure_db()
    data_str = json.dumps(data, ensure_ascii=False, default=str)
    conn.execute(
        "INSERT OR REPLACE INTO cache (source, series_id, params, data, fetched_at) VALUES (?,?,?,?,?)",
        (source, series_id, params, data_str, time.time()),
    )
    conn.commit()
    conn.close()


def purge(source=None, older_than_days=7):
    conn = _ensure_db()
    cutoff = time.time() - (older_than_days * 86400)
    if source:
        conn.execute(
            "DELETE FROM cache WHERE source=? AND fetched_at < ?", (source, cutoff)
        )
    else:
        conn.execute("DELETE FROM cache WHERE fetched_at < ?", (cutoff,))
    deleted = conn.total_changes
    conn.commit()
    conn.close()
    return deleted


def stats():
    conn = _ensure_db()
    rows = conn.execute(
        "SELECT source, COUNT(*) as cnt, MIN(fetched_at) as oldest, MAX(fetched_at) as newest FROM cache GROUP BY source"
    ).fetchall()
    conn.close()

    print(f"{'Source':<15} {'Entries':<8} {'Oldest':<20} {'Newest':<20}")
    print("-" * 63)
    for source, cnt, oldest, newest in rows:
        oldest_str = datetime.fromtimestamp(oldest).strftime("%Y-%m-%d %H:%M")
        newest_str = datetime.fromtimestamp(newest).strftime("%Y-%m-%d %H:%M")
        print(f"{source:<15} {cnt:<8} {oldest_str:<20} {newest_str:<20}")

    total = sum(r[1] for r in rows)
    print(f"\nTotal entries: {total}")
    print(f"Cache DB: {CACHE_DB}")
    db_size = CACHE_DB.stat().st_size if CACHE_DB.exists() else 0
    print(f"Size: {db_size / 1024:.1f} KB")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cache_manager.py <get|set|purge|stats> [...]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "get":
        if len(sys.argv) < 4:
            print("Usage: cache_manager.py get <source> <series_id> [params]")
            sys.exit(1)
        source = sys.argv[2]
        series_id = sys.argv[3]
        params = sys.argv[4] if len(sys.argv) > 4 else ""
        result = get(source, series_id, params)
        if result is None:
            print("CACHE_MISS")
            sys.exit(1)
        else:
            print(json.dumps(result, ensure_ascii=False, default=str))

    elif cmd == "set":
        if len(sys.argv) < 4:
            print("Usage: cache_manager.py set <source> <series_id> <json_data> [params]")
            sys.exit(1)
        source = sys.argv[2]
        series_id = sys.argv[3]
        data = json.loads(sys.argv[4]) if len(sys.argv) > 4 else {}
        params = sys.argv[5] if len(sys.argv) > 5 else ""
        set(source, series_id, data, params)
        print(f"Cached {source}/{series_id}")

    elif cmd == "purge":
        source = sys.argv[2] if len(sys.argv) > 2 else None
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        deleted = purge(source, days)
        print(f"Purged {deleted} entries")

    elif cmd == "stats":
        stats()

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
