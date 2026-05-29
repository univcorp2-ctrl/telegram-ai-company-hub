from __future__ import annotations

import argparse
import json
from pathlib import Path

from app.export import export_plan
from app.obsidian import write_vault
from app.planner import plan_goal
from app.telegram import extract_goal_from_update


def run_sample(output_dir: Path) -> None:
    sample = Path("samples/telegram_goal_update.json")
    update = json.loads(sample.read_text(encoding="utf-8"))
    text, user_name = extract_goal_from_update(update)
    plan = plan_goal(text, source="cli", user_name=user_name)
    vault = output_dir / "ObsidianVault"
    write_vault(plan, vault)
    export_plan(plan, output_dir / "exports")
    print(plan.telegram_reply)


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sample = sub.add_parser("run-sample")
    sample.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()
    if args.command == "run-sample":
        run_sample(args.output_dir)


if __name__ == "__main__":
    main()
