from fastapi import APIRouter
from database import get_connection
from datetime import datetime, timedelta

router = APIRouter()

STALE_DAYS = 5


@router.get("/alerts")
def get_alerts():
    conn = get_connection()
    jobs = conn.execute(
        "SELECT * FROM jobs WHERE status = 'active'"
    ).fetchall()

    alerts = []
    now = datetime.utcnow()

    for job in jobs:
        last = conn.execute(
            "SELECT created_at FROM activity_entries WHERE job_id = ? ORDER BY created_at DESC LIMIT 1",
            (job["id"],),
        ).fetchone()

        if last:
            try:
                ref_dt = datetime.fromisoformat(last["created_at"])
            except ValueError:
                ref_dt = now
        else:
            try:
                ref_dt = datetime.fromisoformat(job["created_at"])
            except ValueError:
                ref_dt = now

        days_stale = (now - ref_dt).days
        if days_stale >= STALE_DAYS:
            alerts.append({
                "type": "stale_job",
                "job_id": job["id"],
                "job_name": job["name"],
                "days_stale": days_stale,
                "message": f"{job['name']} has had no update in {days_stale} days.",
                "severity": "warning",
            })

    conn.close()
    return {"alerts": alerts}
