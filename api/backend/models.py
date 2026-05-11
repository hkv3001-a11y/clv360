from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ── Job ──────────────────────────────────────────────────────────────────────

class JobCreate(BaseModel):
    name: str
    address: str = ""
    status: str = "active"
    crew_member_id: Optional[int] = None
    percent_complete: int = 0
    start_date: Optional[str] = None
    target_date: Optional[str] = None


class JobUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None
    crew_member_id: Optional[int] = None
    percent_complete: Optional[int] = None
    start_date: Optional[str] = None
    target_date: Optional[str] = None


class JobOut(BaseModel):
    id: int
    name: str
    address: str
    status: str
    crew_member_id: Optional[int]
    percent_complete: int
    start_date: Optional[str]
    target_date: Optional[str]
    created_at: datetime
    updated_at: datetime


# ── Crew ─────────────────────────────────────────────────────────────────────

class CrewCreate(BaseModel):
    name: str
    phone: str = ""
    email: str = ""


class CrewUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class CrewOut(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    created_at: datetime


# ── Activity ──────────────────────────────────────────────────────────────────

class ActivityCreate(BaseModel):
    source_name: str = ""
    channel: str = "manual"
    raw_message: str = ""
    parsed_action: str = ""


class ActivityOut(BaseModel):
    id: int
    job_id: int
    source_name: str
    channel: str
    raw_message: str
    parsed_action: str
    created_at: datetime


# ── Notes ─────────────────────────────────────────────────────────────────────

class NoteCreate(BaseModel):
    job_id: Optional[int] = None
    body: str
    author: str = "Owner"


class NoteOut(BaseModel):
    id: int
    job_id: Optional[int]
    body: str
    author: str
    created_at: datetime


# ── Chat ──────────────────────────────────────────────────────────────────────

class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    action_taken: Optional[dict] = None


# ── Inbound ───────────────────────────────────────────────────────────────────

class InboundMessage(BaseModel):
    channel: str
    sender_name: str
    message: str
