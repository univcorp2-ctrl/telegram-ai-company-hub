from app.planner import normalize_goal, plan_goal


def test_normalize_goal_removes_command():
    assert normalize_goal("/goal  不動産仕入れAI会社を起動") == "不動産仕入れAI会社を起動"


def test_plan_contains_real_estate_and_dev_tasks():
    plan = plan_goal("/goal 不動産仕入れAI会社を起動してGitHub実装もする")
    titles = [task.title for task in plan.tasks]
    assert "不動産候補の調査項目を定義する" in titles
    assert "MVP実装とCI/CDの要件を固める" in titles
    assert plan.issue_markdown.startswith("# AI Company Goal")
