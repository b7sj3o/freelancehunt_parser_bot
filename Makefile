.PHONY: run

run:
	watchmedo auto-restart --patterns="*.py" --recursive -- .venv/Scripts/python.exe main.py
