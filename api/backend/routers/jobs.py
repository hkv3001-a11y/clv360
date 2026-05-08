from fastapi import APIRouter, HTTPException
from typing import List
from database import get_connection, get_cursor
from models import JobCreate, JobUpdate, JobOut

router = APIRouter()


@router.get("/jobs", response_model=List[JobOut])
def list_jobs():
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("SELECT * FROM jobs ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/jobs", response_model=JobOut, status_code=201)
def create_job(job: JobCreate):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute(
        """INSERT INTO jobs
               (name, address, status, crew_member_id, percent_complete, start_date, target_date)
           VALUES (%s, %s, %s, %s, %s, %s, %s)
           RETURNING *""",
        (job.name, job.address, job.status, job.crew_member_id,
         job.percent_complete, job.start_date, job.target_date),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return dict(row)


@router.put("/jobs/{job_id}", response_model=JobOut)
def update_job(job_id: int, job: JobUpdate):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("SELECT id FROM jobs WHERE id = %s", (job_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")

    updates = {k: v for k, v in job.model_dump().items() if v is not None}
    if updates:
        set_clause = ", ".join(f"{k} = %s" for k in updates)
        values = list(updates.values()) + [job_id]
        cur.execute(
            f"UPDATE jobs SET {set_clause}, updated_at = NOW() WHERE id = %s",
            values,
        )
        conn.commit()

    cur.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return dict(row)


@router.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("SELECT id FROM jobs WHERE id = %s", (job_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")
    cur.execute("DELETE FROM jobs WHERE id = %s", (job_id,))
    conn.commit()
    cur.close()
    conn.close()
