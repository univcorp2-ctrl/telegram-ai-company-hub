# Setup Guide

## 1. Telegram Botを作る

1. Telegramで `@BotFather` を開く
2. `/newbot` を送る
3. Bot名とusernameを決める
4. Tokenを取得する
5. TokenはGitHubへcommitせず、環境変数 `TELEGRAM_BOT_TOKEN` に保存する

## 2. ローカル起動

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
pytest
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 3. Webhookテスト

```bash
curl -X POST http://localhost:8000/telegram/webhook \
  -H 'Content-Type: application/json' \
  -d @samples/telegram_goal_update.json
```

## 4. HTTPS公開

Telegram webhookにはHTTPS URLが必要です。選択肢は以下です。

- Cloudflare Tunnel
- VPS + Caddy/Nginx
- Cloudflare Workersで受けてFastAPIへ転送
- Render/Fly.io/Railway等

## 5. 本番に必要なSecrets

| Secret | 保存場所 | 用途 |
| --- | --- | --- |
| `TELEGRAM_BOT_TOKEN` | VPS/Cloud host secret | Telegram Bot API |
| `TELEGRAM_WEBHOOK_SECRET` | VPS/Cloud host secret | webhook検証 |
| `GITHUB_TOKEN` | GitHub Actions or server secret | 将来のIssue/PR作成 |

## 6. 最初の運用

1. `/goal` で目的を送る
2. Obsidian Vault出力を見る
3. GitHub Issue Markdownを確認する
4. CSV/Excelを日次ログとして保存する
5. 外部送信や本番反映は人間が確認する
