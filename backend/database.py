import os
import sqlite3
from pathlib import Path

# Vercel serverless functions have a read-only filesystem except /tmp
DB_PATH = Path("/tmp/clv360.db") if os.environ.get("VERCEL") else Path(__file__).parent / "clv360.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS crew_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT DEFAULT '',
            email TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT DEFAULT '',
            status TEXT DEFAULT 'active'
                CHECK(status IN ('active','on_hold','completed','cancelled')),
            crew_member_id INTEGER REFERENCES crew_members(id) ON DELETE SET NULL,
            percent_complete INTEGER DEFAULT 0
                CHECK(percent_complete BETWEEN 0 AND 100),
            start_date TEXT,
            target_date TEXT,
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS activity_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
            source_name TEXT DEFAULT '',
            channel TEXT DEFAULT 'manual'
                CHECK(channel IN ('sms','whatsapp','email','manual','ai')),
            raw_message TEXT DEFAULT '',
            parsed_action TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
            body TEXT NOT NULL,
            author TEXT DEFAULT 'Owner',
            created_at TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()
