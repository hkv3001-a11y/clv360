from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import jobs, crew, notes, activity, chat, inbound, weather, alerts

app = FastAPI(title="CLV360 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://clv360.com", "https://*.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(jobs.router, prefix="/api")
app.include_router(crew.router, prefix="/api")
app.include_router(notes.router, prefix="/api")
app.include_router(activity.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(inbound.router, prefix="/api")
app.include_router(weather.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/debug-db")
def debug_db():
    import os
    url = os.environ.get("DATABASE_URL", "NOT SET")
    # Only show non-sensitive parts
    if url != "NOT SET" and "@" in url:
        parts = url.split("@")
        safe_url = "***@" + parts[-1]
    else:
        safe_url = url[:20] + "..." if len(url) > 20 else url
    try:
        from database import get_connection, get_cursor
        conn = get_connection()
        cur = get_cursor(conn)
        cur.execute("SELECT COUNT(*) as n FROM jobs")
        count = cur.fetchone()["n"]
        cur.close()
        conn.close()
        return {"db": "connected", "jobs_count": count, "url_hint": safe_url}
    except Exception as e:
        return {"db": "error", "error": str(e), "url_hint": safe_url}
