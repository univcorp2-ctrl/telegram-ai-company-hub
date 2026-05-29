from __future__ import annotations

import hashlib
import re
from textwrap import dedent

from app.models import AgentRole, CompanyTask, GoalPlan


def normalize_goal(text: str) -> str:
    cleaned = re.sub(r"^/goal\s*", "", text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "AI会社の初期設定と日次タスクを作成する"


def make_goal_id(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]


def default_roles() -> list[AgentRole]:
    return [
        AgentRole(
            name="CEO Agent",
            mission="目的を分解し、収益化・融資・仕入れ・開発の優先順位を決める",
            outputs=["今日の方針", "優先度", "人間承認が必要な判断"],
        ),
        AgentRole(
            name="Research Agent",
            mission="根拠URLと一次情報を集め、調査結果を構造化する",
            outputs=["調査メモ", "候補リスト", "根拠URL"],
        ),
        AgentRole(
            name="Underwriter Agent",
            mission="利回り、融資可能性、収支、出口を定量評価する",
            outputs=["Excel向け表", "投資判定", "リスク一覧"],
        ),
        AgentRole(
            name="Engineer Agent",
            mission="GitHub実装、CI、Cloudflare、DB、成果物生成を担当する",
            outputs=["コード", "PR/Issue本文", "CI結果"],
        ),
        AgentRole(
            name="QA Agent",
            mission="計算・根拠・安全性・Secrets混入・テスト結果を確認する",
            outputs=["レビュー", "修正指示", "テスト結果"],
        ),
        AgentRole(
            name="Memory Librarian",
            mission="Obsidian Vaultへ判断基準、成功例、失敗例、日次ログを保存する",
            outputs=["Markdownナレッジ", "日次ログ", "再利用プロンプト"],
        ),
    ]


def build_tasks(goal: str) -> list[CompanyTask]:
    lower = goal.lower()
    is_real_estate = any(k in goal for k in ["不動産", "物件", "融資", "土地", "アパート"])
    is_dev = any(k in lower for k in ["github", "repo", "web", "app", "cloudflare", "実装"])

    tasks = [
        CompanyTask(
            title="ゴールを事業成果物へ分解する",
            owner="CEO Agent",
            priority=5,
            checklist=["目的を1文にする", "成果物を決める", "人間承認が必要な操作を分離する"],
        ),
        CompanyTask(
            title="Obsidian原液ナレッジを更新する",
            owner="Memory Librarian",
            priority=4,
            checklist=["Master Goalへ反映", "判断ルールへ追記", "日次ログを作成"],
        ),
        CompanyTask(
            title="GitHub Issue用の実行仕様を作る",
            owner="Engineer Agent",
            priority=4,
            checklist=["背景を書く", "タスクをチェックリスト化", "完了条件を書く"],
        ),
        CompanyTask(
            title="QA観点でリスクとSecrets混入を確認する",
            owner="QA Agent",
            priority=3,
            checklist=["外部送信なし", "秘密情報なし", "テスト可能な形になっている"],
        ),
    ]
    if is_real_estate:
        tasks.insert(
            1,
            CompanyTask(
                title="不動産候補の調査項目を定義する",
                owner="Research Agent",
                priority=5,
                checklist=["価格/面積/駅距離", "用途地域/建ぺい率/容積率", "想定家賃/表面利回り"],
            ),
        )
        tasks.insert(
            2,
            CompanyTask(
                title="融資・出口・利回りの簡易判定表を作る",
                owner="Underwriter Agent",
                priority=5,
                checklist=["総事業費", "DSCR", "出口利回り", "銀行打診メモ"],
            ),
        )
    if is_dev:
        tasks.append(
            CompanyTask(
                title="MVP実装とCI/CDの要件を固める",
                owner="Engineer Agent",
                priority=5,
                checklist=["README", "テスト", "GitHub Actions", "devcontainer", "architecture docs"],
            )
        )
    return tasks


def build_issue_markdown(goal: str, tasks: list[CompanyTask]) -> str:
    checklist = "\n".join(
        f"- [ ] **{task.title}** — owner: {task.owner}, priority: {task.priority}\n"
        + "\n".join(f"  - [ ] {item}" for item in task.checklist)
        for task in tasks
    )
    return dedent(
        f"""
        # AI Company Goal

        ## Goal
        {goal}

        ## Execution Checklist
        {checklist}

        ## Safety Rules
        - Do not commit secrets, API keys, bot tokens, or personal information.
        - External messages to banks, brokers, or customers must be drafted only.
        - Main branch deployment requires human approval until production rules are explicit.

        ## Done Definition
        - Tasks are saved to SQLite or Markdown.
        - Obsidian-compatible notes are generated.
        - CSV/Excel/TXT exports are available.
        - QA review notes are included.
        """
    ).strip()


def plan_goal(text: str, source: str = "api", user_name: str | None = None) -> GoalPlan:
    goal = normalize_goal(text)
    tasks = build_tasks(goal)
    gid = make_goal_id(f"{source}:{user_name}:{goal}")
    obsidian_files = [
        "00_AI_COMPANY/00_Master_Goal.md",
        "00_AI_COMPANY/04_Current_Priorities.md",
        f"90_LOGS/daily/{gid}.md",
    ]
    if any("不動産" in task.title for task in tasks):
        obsidian_files.append("10_REAL_ESTATE/00_Investment_Criteria.md")
    reply = f"AI会社に登録しました。goal_id={gid} / tasks={len(tasks)} / GitHub Issue用MarkdownとObsidianログを生成済みです。"
    return GoalPlan(
        goal_id=gid,
        original_text=text,
        normalized_goal=goal,
        company_name="UNIV AI Company Hub",
        roles=default_roles(),
        tasks=tasks,
        obsidian_files=obsidian_files,
        issue_markdown=build_issue_markdown(goal, tasks),
        telegram_reply=reply,
    )
