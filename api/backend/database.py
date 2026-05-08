import os
import psycopg2
import psycopg2.extras

DATABASE_URL = os.environ["DATABASE_URL"]


def get_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def get_cursor(conn):
    return conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def init_db() -> None:
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
