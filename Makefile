.PHONY: test test-cov lint format

test:
	pytest -v

test-cov:
	pytest --cov=. --cov-report=term-missing -v

lint:
	ruff check .

format:
	ruff format .
	ruff check . --fix