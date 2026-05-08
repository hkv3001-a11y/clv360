import sys
import os

# Ensure api/ is on the path so `from backend.main import app` resolves correctly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.main import app  # noqa: F401 — Vercel picks up the `app` ASGI object
