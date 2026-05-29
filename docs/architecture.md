# Architecture

## 全体像

このMVPは、Telegramから投げられた `/goal` を、AI会社が実行できる構造化タスクへ変換し、Markdown / SQLite / CSV / Excel / TXT に保存する小さな司令塔です。

```mermaid
flowchart TD
    A[Telegram User] --> B[Telegram Bot]
    B --> C[FastAPI /telegram/webhook]
    C --> D[Goal Parser]
    D --> E[Planner]
    E --> F[Role Templates]
    E --> G[Task List]
    G --> H[SQLite]
    G --> I[Obsidian Vault]
    G --> J[GitHub Issue Markdown]
    G --> K[CSV Excel TXT]
    K --> L[GitHub Actions Artifact]
```

## コンポーネント

| Component | File | Role |
| --- | --- | --- |
| API | `app/main.py` | FastAPI endpoint |
| Planner | `app/planner.py` | goalをroles/tasks/issueへ変換 |
| Telegram | `app/telegram.py` | Telegram Updateから本文を抽出 |
| Storage | `app/storage.py` | SQLite保存 |
| Obsidian | `app/obsidian.py` | Vault互換Markdown生成 |
| Export | `app/export.py` | CSV/Excel/TXT生成 |
| CLI | `app/cli.py` | Actions/ローカルでサンプル実行 |

## データフロー

1. Telegramから `/goal ...` を送る
2. `/telegram/webhook` がUpdateを受け取る
3. `planner.plan_goal()` がAI会社タスクに分解
4. SQLiteへgoal/taskを保存
5. Obsidian Vault互換Markdownを生成
6. GitHub Issue本文とCSV/Excel/TXTを出力
7. Telegram向け返信JSONを返す

## DB

SQLiteを採用しています。最初は単一ファイルで十分です。本番ではCloudflare D1、Supabase、PostgreSQLへ移行可能です。

```mermaid
erDiagram
    GOALS ||--o{ TASKS : contains
    GOALS {
      string id PK
      string source
      string original_text
      string normalized_goal
      string created_at
      string payload_json
    }
    TASKS {
      int id PK
      string goal_id FK
      string title
      string owner
      int priority
      string status
      string checklist_json
    }
```

## Secrets

Secretsはコードに保存しません。

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_SECRET`
- 将来の `GITHUB_TOKEN`
- 将来のCloudflare token

## CI/CD

GitHub Actionsは、push / pull_request / workflow_dispatchで起動します。

- checkout
- setup-python
- install dependencies
- ruff format check
- ruff lint
- pytest
- sample artifact generation
- artifact upload

## 今後の拡張

```mermaid
flowchart LR
    A[Current MVP] --> B[GitHub Issue API]
    A --> C[Paperclip API]
    A --> D[Hermes Gateway]
    A --> E[Cloudflare D1/R2]
    A --> F[Real Estate Research Crawlers]
```
