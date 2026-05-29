from pathlib import Path
from fastapi.testclient import TestClient

from app.config import get_settings
from app.main import app


def test_health():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_goal(tmp_path: Path):
    settings = get_settings()
    settings.app_db_path = tmp_path / "app.db"
    settings.obsidian_vault_path = tmp_path / "vault"
    client = TestClient(app)
    response = client.post("/goals", json={"text": "/goal GitHub実装を進める"})
    assert response.status_code == 200
    data = response.json()
    assert data["goal_id"]
    assert len(data["tasks"]) >= 4


def test_telegram_webhook(tmp_path: Path):
    settings = get_settings()
    settings.app_db_path = tmp_path / "telegram.db"
    settings.obsidian_vault_path = tmp_path / "vault2"
    client = TestClient(app)
    response = client.post(
        "/telegram/webhook",
        json={"message": {"text": "/goal 不動産仕入れタスク化", "from": {"username": "irene"}}},
    )
    assert response.status_code == 200
    assert response.json()["method"] == "sendMessage"
