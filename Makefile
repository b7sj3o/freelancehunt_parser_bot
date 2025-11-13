include .env
export

# ====== STARTUP ======
.PHONY: run-bot-dev run-bot

run-bot-dev:
	watchmedo auto-restart --patterns="*.py" --recursive -- .venv/Scripts/python.exe -m bot

run-bot:
	.venv/Scripts/python.exe -m bot

# ====== DATABASE ======
.PHONY: migrations migrate downgrade

migrations:
	alembic revision --autogenerate -m "${args}"
	
migrate:
	alembic upgrade head

downgrade:
	alembic gowngrade ${args}


dump-data:
	poetry run python -m bot.scripts.dump_data