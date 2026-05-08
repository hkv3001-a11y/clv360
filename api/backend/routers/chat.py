import re
import json
from fastapi import APIRouter
from database import get_connection, get_cursor
from models import ChatMessage, ChatResponse
from services.ai import chat_completion

router = APIRouter()

SYSTEM_PROMPT = """You are CLV360, an AI project management assistant for a contracting business.
You help the owner and project manager understand job status, crew assignments, and recent activity.

CURRENT DASHBOARD DATA:
{context}

RULES:
- Be concise and professional. Reference specific job names.
- If asked to update a job status or completion, include an action tag at the very start:
  [[ACTION:{{"type":"update_job","job_id":<id>,"updates":{{"status":"<status>","percent_complete":<0-100>}}}}]]
  Then explain in plain language what you did.
- If you cannot find relevant data, say so clearly.
"""


def _build_context(conn) -> str:
    cur = get_cursor(conn)
    cur.execute("SELECT * FROM jobs ORDER BY created_at DESC")
    jobs = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT * FROM crew_members")
    crew = [dict(r) for r in cur.fetchall()]
    cur.execute("SELECT * FROM activity_entries ORDER BY created_at DESC LIMIT 20")
    recent = [dict(r) for r in cur.fetchall()]
    cur.close()
    return json.dumps({"jobs": jobs, "crew": crew, "recent_activity": recent}, default=str)


def _parse_action(response: str) -> tuple[str, dict | None]:
    match = re.match(r"\[\[ACTION:(.*?)\]\](.*)", response, re.DOTALL)
    if not match:
        return response.strip(), None
    try:
        action = json.loads(match.group(1))
        text = match.group(2).strip()
        return text, action
    except json.JSONDecodeError:
        return response.strip(), None


def _apply_action(action: dict, conn) -> None:
    if action.get("type") == "update_job":
        job_id = action.get("job_id")
        updates = action.get("updates", {})
        if job_id and updates:
            cur = get_cursor(conn)
            set_clause = ", ".join(f"{k} = %s" for k in updates)
            values = list(updates.values()) + [job_id]
            cur.execute(
                f"UPDATE jobs SET {set_clause}, updated_at = NOW() WHERE id = %s",
                values,
            )
            conn.commit()
            cur.close()


@router.post("/chat", response_model=ChatResponse)
async def chat(msg: ChatMessage):
    conn = get_connection()
    context = _build_context(conn)
    system = SYSTEM_PROMPT.format(context=context)

    ai_response = await chat_completion(
        [{"role": "user", "content": msg.message}], system
    )

    text, action = _parse_action(ai_response)
    if action:
        _apply_action(action, conn)
    conn.close()

    return ChatResponse(response=text, action_taken=action)
