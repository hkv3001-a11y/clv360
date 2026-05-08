from fastapi import APIRouter
from typing import List
from database import get_connection
from models import NoteCreate, NoteOut

router = APIRouter()


@router.get("/notes", response_model=List[NoteOut])
def list_notes():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM notes ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/notes", response_model=NoteOut, status_code=201)
def create_note(note: NoteCreate):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO notes (job_id, body, author) VALUES (?, ?, ?)",
        (note.job_id, note.body, note.author),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM notes WHERE id = ?", (c.lastrowid,)).fetchone()
    conn.close()
    return dict(row)
