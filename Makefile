.PHONY: install format lint test run dev clean

install:
	uv pip install -e .

format:
	ruff format app tests

lint:
	ruff check app tests

test:
	uv run pytest tests/ -v

run:
	docker compose up --build

dev: format lint test

clean:
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

