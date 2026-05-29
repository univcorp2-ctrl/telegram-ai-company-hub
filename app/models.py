from datetime import UTC, datetime
from enum import Enum
from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"
    BLOCKED = "blocked"


class AgentRole(BaseModel):
    name: str
    mission: str
    outputs: list[str]


class CompanyTask(BaseModel):
    title: str
    owner: str
    priority: int = Field(ge=1, le=5)
    status: TaskStatus = TaskStatus.TODO
    checklist: list[str]


class GoalRequest(BaseModel):
    text: str
    source: str = "api"
    user_name: str | None = None


class GoalPlan(BaseModel):
    goal_id: str
    original_text: str
    normalized_goal: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    company_name: str
    roles: list[AgentRole]
    tasks: list[CompanyTask]
    obsidian_files: list[str]
    issue_markdown: str
    telegram_reply: str
