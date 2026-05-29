from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException

from app.config import Settings, get_settings
from app.export import export_plan
from app.models import GoalRequest, GoalPlan
from app.obsidian import write_vault
from app.planner import plan_goal
from app.storage import GoalStore
from app.telegram import extract_goal_from_update, make_telegram_response

app = FastAPI(title="Telegram AI Company Hub", version="0.1.0")


def get_store(settings: Settings = Depends(get_settings)) -> GoalStore:
    return GoalStore(settings.app_db_path)


def persist_outputs(plan: GoalPlan, source: str, settings: Settings, store: GoalStore) -> None:
    store.save_plan(plan, source=source)
    write_vault(plan, settings.obsidian_vault_path)
    export_plan(plan, settings.obsidian_vault_path.parent / "exports")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "telegram-ai-company-hub"}


@app.post("/goals", response_model=GoalPlan)
def create_goal(
    request: GoalRequest,
    settings: Settings = Depends(get_settings),
    store: GoalStore = Depends(get_store),
) -> GoalPlan:
    plan = plan_goal(request.text, source=request.source, user_name=request.user_name)
    persist_outputs(plan, request.source, settings, store)
    return plan


@app.get("/goals")
def list_goals(store: GoalStore = Depends(get_store)) -> list[dict[str, str]]:
    return store.list_goals()


@app.post("/telegram/webhook")
def telegram_webhook(
    update: dict,
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
    store: GoalStore = Depends(get_store),
) -> dict[str, str]:
    if settings.telegram_webhook_secret and (
        x_telegram_bot_api_secret_token != settings.telegram_webhook_secret
    ):
        raise HTTPException(status_code=401, detail="invalid telegram webhook secret")
    text, user_name = extract_goal_from_update(update)
    plan = plan_goal(text, source="telegram", user_name=user_name)
    persist_outputs(plan, "telegram", settings, store)
    return make_telegram_response(plan.telegram_reply)
