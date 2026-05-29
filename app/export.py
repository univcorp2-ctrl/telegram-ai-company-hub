from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook

from app.models import GoalPlan


def export_plan(plan: GoalPlan, output_dir: Path) -> dict[str, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = {
        "txt": output_dir / f"{plan.goal_id}_summary.txt",
        "csv": output_dir / f"{plan.goal_id}_tasks.csv",
        "xlsx": output_dir / f"{plan.goal_id}_tasks.xlsx",
        "issue": output_dir / f"{plan.goal_id}_github_issue.md",
    }
    paths["txt"].write_text(plan.telegram_reply + "\n", encoding="utf-8")
    paths["issue"].write_text(plan.issue_markdown + "\n", encoding="utf-8")

    with paths["csv"].open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["goal_id", "title", "owner", "priority", "status", "checklist"])
        for task in plan.tasks:
            writer.writerow([
                plan.goal_id,
                task.title,
                task.owner,
                task.priority,
                task.status.value,
                " / ".join(task.checklist),
            ])

    wb = Workbook()
    ws = wb.active
    ws.title = "Tasks"
    ws.append(["goal_id", "title", "owner", "priority", "status", "checklist"])
    for task in plan.tasks:
        ws.append([
            plan.goal_id,
            task.title,
            task.owner,
            task.priority,
            task.status.value,
            " / ".join(task.checklist),
        ])
    for column_cells in ws.columns:
        max_length = max(len(str(cell.value or "")) for cell in column_cells)
        ws.column_dimensions[column_cells[0].column_letter].width = min(max_length + 2, 60)
    wb.save(paths["xlsx"])
    return paths
