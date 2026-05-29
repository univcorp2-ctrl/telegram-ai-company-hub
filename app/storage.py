from __future__ import annotations

import json
import sqlite3
from pathlib import Path

from app.models import GoalPlan


SCHEMA = """
CREATE TABLE IF NOT EXISTS goals (
  id TEXT PRIMARY KEY,
  source TEXT NOT NULL,
  original_text TEXT NOT NULL,
  normalized_goal TEXT NOT NULL,
  created_at TEXT NOT NULL,
  payload_json TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  goal_id TEXT NOT NULL,
  title TEXT NOT NULL,
  owner TEXT NOT NULL,
  priority INTEGER NOT NULL,
  status TEXT NOT NULL,
  checklist_json TEXT NOT NULL,
  FOREIGN KEY(goal_id) REFERENCES goals(id)
);
"""


class GoalStore:
    def __init__(self, path: Path):
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._init()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.path)

    def _init(self) -> None:
        with self._connect() as conn:
            conn.executescript(SCHEMA)

    def save_plan(self, plan: GoalPlan, source: str) -> None:
        payload = plan.model_dump_json(indent=2)
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO goals
                (id, source, original_text, normalized_goal, created_at, payload_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    plan.goal_id,
                    source,
                    plan.original_text,
                    plan.normalized_goal,
                    plan.created_at.isoformat(),
                    payload,
                ),
            )
            conn.execute("DELETE FROM tasks WHERE goal_id = ?", (plan.goal_id,))
            conn.executemany(
                """
                INSERT INTO tasks (goal_id, title, owner, priority, status, checklist_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                [
                    (
                        plan.goal_id,
                        task.title,
                        task.owner,
                        task.priority,
                        task.status.value,
                        json.dumps(task.checklist, ensure_ascii=False),
                    )
                    for task in plan.tasks
                ],
            )

    def list_goals(self) -> list[dict[str, str]]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, source, normalized_goal, created_at FROM goals ORDER BY created_at DESC"
            ).fetchall()
        return [
            {"id": row[0], "source": row[1], "normalized_goal": row[2], "created_at": row[3]}
            for row in rows
        ]
