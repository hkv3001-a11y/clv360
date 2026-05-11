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
    try:
        from database import get_connection, get_cursor, DATABASE_URL
        safe = ("***@" + DATABASE_URL.split("@")[-1]) if "@" in DATABASE_URL else DATABASE_URL[:30]
        conn = get_connection()
        cur = get_cursor(conn)
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        cur.close()
        conn.close()
        tables = [r["table_name"] for r in cur.fetchall()]
        return {"db": "connected", "url": safe, "tables": tables}
    except Exception as e:
        return {"db": "error", "error": str(e)}
