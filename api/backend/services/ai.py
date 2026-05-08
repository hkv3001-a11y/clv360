import os
import json
import re
import httpx
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.environ.get("OPENROUTER_MODEL", "anthropic/claude-sonnet-4-6")
OPENROUTER_BASE = "https://openrouter.ai/api/v1"


async def chat_completion(messages: list[dict], system_prompt: str) -> str:
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "system", "content": system_prompt}] + messages,
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{OPENROUTER_BASE}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30.0,
        )
        resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


async def parse_inbound_message(message: str, sender_name: str, jobs: list[dict]) -> dict:
    jobs_context = json.dumps(
        [{"id": j["id"], "name": j["name"], "status": j["status"]} for j in jobs]
    )
    system = (
        "You are a job update parser for a contractor management system.\n"
        "Given a field worker message and a list of active jobs, identify which job is "
        "being updated and what action to take.\n\n"
        "Respond ONLY with valid JSON in this exact format:\n"
        '{"job_id": <int or null>, "status": <"active"|"on_hold"|"completed"|"cancelled"|null>, '
        '"percent_complete": <0-100 or null>, "parsed_action": "<brief description>", '
        '"unrecognized": <true if no job match>}'
    )
    user_msg = f"Field worker '{sender_name}' sent: '{message}'\n\nCurrent jobs:\n{jobs_context}"
    raw = await chat_completion([{"role": "user", "content": user_msg}], system)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {"job_id": None, "unrecognized": True, "parsed_action": "Could not parse message"}
