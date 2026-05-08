from fastapi import APIRouter
from typing import List
from database import get_connection, get_cursor
from models import NoteCreate, NoteOut

router = APIRouter()


@router.get("/notes", response_model=List[NoteOut])
def list_notes():
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("SELECT * FROM notes ORDER BY created_at DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/notes", response_model=NoteOut, status_code=201)
def create_note(note: NoteCreate):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute(
        "INSERT INTO notes (job_id, body, author) VALUES (%s, %s, %s) RETURNING *",
        (note.job_id, note.body, note.author),
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return dict(row)
