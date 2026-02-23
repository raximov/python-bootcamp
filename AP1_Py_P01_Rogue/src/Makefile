export PYGAME_HIDE_SUPPORT_PROMPT=hide

# Detect OS and set Python command
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Linux)
    PYTHON := python3
else ifeq ($(UNAME_S),Darwin)
    PYTHON := python3
else
    PYTHON := python
endif

# Use venv python if it exists
VENV_PYTHON := .venv/bin/python
ifneq ($(wildcard $(VENV_PYTHON)),)
    PYTHON := $(VENV_PYTHON)
endif

.PHONY: run install uninstall lint format clean

run:
	rm -rf log/*
	$(PYTHON) main.py

install:
	$(PYTHON) -m pip install -e .[dev] -U

uninstall:
	$(PYTHON) -m pip uninstall -y -e .
	$(PYTHON) -m pip freeze | grep -v '^-e' | xargs $(PYTHON) -m pip uninstall -y
	$(PYTHON) -m pip cache purge

lint:
	ruff check .
	ruff format . --check

format:
	ruff check . --fix
	ruff format .

clean:
	rm -rf __pycache__ build/ log/*
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "🧹"
