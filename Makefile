include .env
export

# ====== STARTUP ======
.PHONY: run run-bot run-admin run-bot-dev run-admin-dev run-dev

run-bot-dev:
	watchmedo auto-restart --patterns="*.py" --recursive -- .venv/Scripts/python.exe -m bot

run-bot:
	.venv/Scripts/python.exe -m bot

run-admin-dev:
	.venv/Scripts/python.exe -m admin.app --reload

run-admin:
	.venv/Scripts/python.exe -m admin.app

run-dev: run-bot-dev run-admin-dev
run: run-bot run-admin

# ====== DATABASE ======
.PHONY: mm migrate downgrade

mm:
	alembic revision --autogenerate -m "${args}"
	
migrate:
	alembic upgrade head

downgrade:
	alembic gowngrade ${args}