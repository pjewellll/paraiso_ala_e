"""Production entry point for Render/Gunicorn."""

import os

from app import app, init_db


def _auto_init_enabled() -> bool:
    return os.environ.get("AUTO_INIT_DB", "false").strip().lower() in {
        "1",
        "true",
        "yes",
        "y",
        "on",
    }


if _auto_init_enabled():
    init_db()

