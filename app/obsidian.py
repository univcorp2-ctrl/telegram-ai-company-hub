from __future__ import annotations

from pathlib import Path

from app.models import GoalPlan


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_vault(plan: GoalPlan, vault_path: Path) -> list[Path]:
    written: list[Path] = []
    master = vault_path / "00_AI_COMPANY" / "00_Master_Goal.md"
    write_text(
        master,
        "# Master Goal\n\n"
        "## 最優先目的\n"
        "- 収益化\n- 回収\n- 不動産仕入れ\n- 融資獲得\n- AI自動化\n- GitHub実装\n\n"
        "## AI社員への基本命令\n"
        "抽象論ではなく、表・コード・ファイル・Issue・Excel化できる成果物へ変換する。\n",
    )
    written.append(master)

    priorities = vault_path / "00_AI_COMPANY" / "04_Current_Priorities.md"
    write_text(
        priorities,
        f"# Current Priorities\n\n## Latest Goal\n{plan.normalized_goal}\n\n"
        + "\n".join(f"- {task.title} ({task.owner})" for task in plan.tasks)
        + "\n",
    )
    written.append(priorities)

    log = vault_path / "90_LOGS" / "daily" / f"{plan.goal_id}.md"
    write_text(
        log,
        f"# Daily Goal Log {plan.goal_id}\n\n"
        f"Created: {plan.created_at.isoformat()}\n\n"
        f"## Goal\n{plan.normalized_goal}\n\n"
        f"## Telegram Reply\n{plan.telegram_reply}\n\n"
        f"## GitHub Issue Draft\n\n{plan.issue_markdown}\n",
    )
    written.append(log)

    criteria = vault_path / "10_REAL_ESTATE" / "00_Investment_Criteria.md"
    write_text(
        criteria,
        "# 不動産投資条件\n\n"
        "## 優先物件\n"
        "- 東京、神奈川、埼玉、千葉の土地または新築アパート候補\n"
        "- 木造9〜18戸\n- 表面利回り8.5%以上、理想9%以上\n- 駅徒歩15分以内\n\n"
        "## 必須チェック\n"
        "- 用途地域\n- 建ぺい率\n- 容積率\n- 前面道路\n- 想定家賃\n- 建築費\n- DSCR\n",
    )
    written.append(criteria)
    return written
