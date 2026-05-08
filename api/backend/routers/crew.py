from fastapi import APIRouter, HTTPException
from typing import List
from database import get_connection
from models import CrewCreate, CrewUpdate, CrewOut

router = APIRouter()


@router.get("/crew", response_model=List[CrewOut])
def list_crew():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM crew_members ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]


@router.post("/crew", response_model=CrewOut, status_code=201)
def create_crew_member(member: CrewCreate):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO crew_members (name, phone, email) VALUES (?, ?, ?)",
        (member.name, member.phone, member.email),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM crew_members WHERE id = ?", (c.lastrowid,)).fetchone()
    conn.close()
    return dict(row)


@router.put("/crew/{member_id}", response_model=CrewOut)
def update_crew_member(member_id: int, member: CrewUpdate):
    conn = get_connection()
    if not conn.execute("SELECT id FROM crew_members WHERE id = ?", (member_id,)).fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Crew member not found")

    updates = {k: v for k, v in member.model_dump().items() if v is not None}
    if updates:
        set_clause = ", ".join(f"{k} = ?" for k in updates)
        values = list(updates.values()) + [member_id]
        conn.execute(f"UPDATE crew_members SET {set_clause} WHERE id = ?", values)
        conn.commit()

    row = conn.execute("SELECT * FROM crew_members WHERE id = ?", (member_id,)).fetchone()
    conn.close()
    return dict(row)


@router.delete("/crew/{member_id}", status_code=204)
def delete_crew_member(member_id: int):
    conn = get_connection()
    if not conn.execute("SELECT id FROM crew_members WHERE id = ?", (member_id,)).fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Crew member not found")
    conn.execute("DELETE FROM crew_members WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()
