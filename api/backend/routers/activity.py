from fastapi import APIRouter, HTTPException
from typing import List
from database import get_connection
from models import ActivityCreate, ActivityOut

router = APIRouter()


@router.get("/jobs/{job_id}/activity", response_model=List[ActivityOut])
def list_activity(job_id: int):
    conn = get_connection()
    if not conn.execute("SELECT id FROM jobs WHERE id = ?", (job_id,)).fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")
    rows = conn.execute(
        "SELECT * FROM activity_entries WHERE job_id = ? ORDER BY created_at DESC",
        (job_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/jobs/{job_id}/activity", response_model=ActivityOut, status_code=201)
def add_activity(job_id: int, entry: ActivityCreate):
    conn = get_connection()
    if not conn.execute("SELECT id FROM jobs WHERE id = ?", (job_id,)).fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")
    c = conn.cursor()
    c.execute(
        """INSERT INTO activity_entries
               (job_id, source_name, channel, raw_message, parsed_action)
           VALUES (?, ?, ?, ?, ?)""",
        (job_id, entry.source_name, entry.channel, entry.raw_message, entry.parsed_action),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM activity_entries WHERE id = ?", (c.lastrowid,)).fetchone()
    conn.close()
    return dict(row)
