import sys
import os

# Add backend to path so Vercel can find the FastAPI app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from main import app  # noqa: F401 — Vercel picks up the `app` ASGI object
