from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import jobs, crew, notes, activity, chat, inbound, weather, alerts

app = FastAPI(title="CLV360 API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
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
