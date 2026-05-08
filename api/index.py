import sys
import os

# Add api/backend/ to sys.path so backend modules resolve as expected
# (e.g. `from database import init_db`, `from routers import jobs`)
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "backend"))

from main import app  # noqa: F401 — Vercel picks up the `app` ASGI object
