from fastapi import APIRouter, HTTPException
from typing import List
from database import get_connection
from models import JobCreate, JobUpdate, JobOut

router = APIRouter()


@router.get("/jobs", response_model=List[JobOut])
def list_jobs():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM jobs ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/jobs", response_model=JobOut, status_code=201)
def create_job(job: JobCreate):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO jobs
               (name, address, status, crew_member_id, percent_complete, start_date, target_date)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (job.name, job.address, job.status, job.crew_member_id,
         job.percent_complete, job.start_date, job.target_date),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM jobs WHERE id = ?", (c.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


@router.put("/jobs/{job_id}", response_model=JobOut)
def update_job(job_id: int, job: JobUpdate):
    conn = get_connection()
    if not conn.execute("SELECT id FROM jobs WHERE id = ?", (job_id,)).fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")

    updates = {k: v for k, v in job.model_dump().items() if v is not None}
    if updates:
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [job_id]
        conn.execute(
            f"UPDATE jobs SET {set_clause}, updated_at = datetime('now') WHERE id = ?",
            values,
        )
        conn.commit()

    row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    conn.close()
    return dict(row)


@router.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int):
    conn = get_connection()
    if not conn.execute("SELECT id FROM jobs WHERE id = ?", (job_id,)).fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Job not found")
    conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
    conn.commit()
    conn.close()
