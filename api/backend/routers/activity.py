from fastapi import APIRouter, HTTPException
from typing import List
from database import get_connection, get_cursor
from models import ActivityCreate, ActivityOut

router = APIRouter()


@router.get("/jobs/{job_id}/activity", response_model=List[ActivityOut])
def list_activity(job_id: int):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("SELECT id FROM jobs WHERE id = %s", (job_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")
    cur.execute(
        "SELECT * FROM activity_entries WHERE job_id = %s ORDER BY created_at DESC",
        (job_id,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/jobs/{job_id}/activity", response_model=ActivityOut, status_code=201)
def add_activity(job_id: int, entry: ActivityCreate):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("SELECT id FROM jobs WHERE id = %s", (job_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")
    cur.execute(
        """INSERT INTO activity_entries
               (job_id, source_name, channel, raw_message, parsed_action)
           VALUES (%s, %s, %s, %s, %s)
           RETURNING *""",
        (job_id, entry.source_name, entry.channel, entry.raw_message, entry.parsed_action),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return dict(row)
