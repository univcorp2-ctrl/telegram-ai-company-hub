# CODEX Instructions

- Do not commit secrets or `.env` files.
- Keep the MVP runnable with `pytest` and `python -m app.cli run-sample --output-dir outputs`.
- Update README and docs when behavior changes.
- Prefer small, explicit functions over hidden agent magic.
- External actions such as sending emails to banks/brokers/customers must remain draft-only unless production approval rules are added.
