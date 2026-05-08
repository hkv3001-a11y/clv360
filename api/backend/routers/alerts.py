from fastapi import APIRouter
from database import get_connection, get_cursor
from datetime import datetime, timedelta, timezone

router = APIRouter()

STALE_DAYS = 5


@router.get("/alerts")
def get_alerts():
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("SELECT * FROM jobs WHERE status = 'active'")
    jobs = cur.fetchall()

    alerts = []
    now = datetime.now(timezone.utc)

    for job in jobs:
        cur.execute(
            "SELECT created_at FROM activity_entries WHERE job_id = %s ORDER BY created_at DESC LIMIT 1",
            (job["id"],),
        )
        last = cur.fetchone()

        ref_dt = last["created_at"] if last else job["created_at"]
        if ref_dt and ref_dt.tzinfo is None:
            ref_dt = ref_dt.replace(tzinfo=timezone.utc)

        if ref_dt:
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

    cur.close()
    conn.close()
    return {"alerts": alerts}
