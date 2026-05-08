from fastapi import APIRouter, HTTPException
from database import get_connection, get_cursor
from models import InboundMessage
from services.ai import parse_inbound_message

router = APIRouter()


@router.post("/inbound/test")
async def inbound_test(msg: InboundMessage):
    conn = get_connection()
    cur = get_cursor(conn)
    cur.execute("SELECT * FROM jobs WHERE status != 'cancelled'")
    jobs = [dict(r) for r in cur.fetchall()]

    parsed = await parse_inbound_message(msg.message, msg.sender_name, jobs)

    job_updated = False
    if parsed.get("job_id") and not parsed.get("unrecognized"):
        job_id = parsed["job_id"]
        updates = {}
        if parsed.get("status"):
            updates["status"] = parsed["status"]
        if parsed.get("percent_complete") is not None:
            updates["percent_complete"] = parsed["percent_complete"]

        if updates:
            set_clause = ", ".join(f"{k} = %s" for k in updates)
            values = list(updates.values()) + [job_id]
            cur.execute(
                f"UPDATE jobs SET {set_clause}, updated_at = NOW() WHERE id = %s",
                values,
            )
            cur.execute(
                """INSERT INTO activity_entries
                       (job_id, source_name, channel, raw_message, parsed_action)
                   VALUES (%s, %s, %s, %s, %s)""",
                (job_id, msg.sender_name, msg.channel, msg.message, parsed.get("parsed_action", "")),
            )
            conn.commit()
            job_updated = True

    cur.close()
    conn.close()
    return {
        "job_updated": job_updated,
        "parsed_action": parsed.get("parsed_action", ""),
        "job_id": parsed.get("job_id"),
    }


@router.post("/inbound/sms")
async def inbound_sms():
    raise HTTPException(status_code=501, detail="Twilio SMS not connected yet — use /api/inbound/test")


@router.post("/inbound/whatsapp")
async def inbound_whatsapp():
    raise HTTPException(status_code=501, detail="WhatsApp not connected yet — use /api/inbound/test")


@router.post("/inbound/email")
async def inbound_email():
    raise HTTPException(status_code=501, detail="Email inbound not connected yet — use /api/inbound/test")
