from __future__ import annotations

from typing import Any


def extract_goal_from_update(update: dict[str, Any]) -> tuple[str, str | None]:
    message = update.get("message") or update.get("edited_message") or {}
    text = message.get("text") or ""
    user = message.get("from") or {}
    user_name = user.get("username") or user.get("first_name")
    if not text.startswith("/goal"):
        text = "/goal " + text
    return text, user_name


def make_telegram_response(text: str) -> dict[str, str]:
    return {"method": "sendMessage", "text": text}
