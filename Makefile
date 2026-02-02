
PYTHON=python3
VENV=.venv
VENV_PY=$(VENV)/bin/python
VENV_PIP=$(VENV)/bin/pip

setup:
	$(PYTHON) -m venv $(VENV)
	$(VENV_PIP) install -r requirements.txt

run:
	$(VENV_PY) -m src.main

qa:
	$(VENV_PY) -m black .
	$(VENV_PY) -m ruff check .
	$(VENV_PY) -m pytest -q
	$(VENV_PY) -m mypy src
