import os
import psycopg2
import psycopg2.extras

_url = os.environ.get("DATABASE_URL", "")

# Strip accidental "DATABASE_URL=" prefix if user pasted the full env line
if _url.startswith("DATABASE_URL="):
    _url = _url[len("DATABASE_URL="):]

# Supabase requires SSL — add sslmode=require if not already present
if _url and "sslmode" not in _url:
    _url += "?sslmode=require" if "?" not in _url else "&sslmode=require"

DATABASE_URL = _url


def get_connection():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL environment variable is not set")
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def get_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def init_db() -> None:
    try:
        conn = get_connection()
        cur = get_cursor(conn)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS crew_members (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                phone TEXT DEFAULT '',
                email TEXT DEFAULT '',
                created_at TIMESTAMPTZ DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS jobs (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                address TEXT DEFAULT '',
                status TEXT DEFAULT 'active'
                    CHECK(status IN ('active','on_hold','completed','cancelled')),
                crew_member_id INTEGER REFERENCES crew_members(id) ON DELETE SET NULL,
                percent_complete INTEGER DEFAULT 0
                    CHECK(percent_complete BETWEEN 0 AND 100),
                start_date TEXT,
                target_date TEXT,
                created_at TIMESTAMPTZ DEFAULT NOW(),
                updated_at TIMESTAMPTZ DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS activity_entries (
                id SERIAL PRIMARY KEY,
                job_id INTEGER NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
                source_name TEXT DEFAULT '',
                channel TEXT DEFAULT 'manual'
                    CHECK(channel IN ('sms','whatsapp','email','manual','ai')),
                raw_message TEXT DEFAULT '',
                parsed_action TEXT DEFAULT '',
                created_at TIMESTAMPTZ DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
                body TEXT NOT NULL,
                author TEXT DEFAULT 'Owner',
                created_at TIMESTAMPTZ DEFAULT NOW()
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        # Log but don't crash — tables may already exist or be created via Supabase SQL editor
        print(f"[database] init_db warning: {e}")
