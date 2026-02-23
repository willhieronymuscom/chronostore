# Makefile — works with uv-managed environment and pytest


# Run tests
.PHONY: test
test:
	uv run pytest -q


# Run tests in verbose mode
.PHONY: test-v
test-quiet:
	uv run pytest -q


# Runs unit test coverage
.PHONY: coverage
coverage:
	uv run pytest --cov=src --cov-report=term-missing


# Runs unit test coverage and builds html report
.PHONY: coverage-report
coverage-report:
	uv run pytest --cov=src --cov-report=html


# Clean Python artifacts
.PHONY: clean
clean:
	find . -name "__pycache__" -type d -exec rm -rf {} +
	find . -name "*.pyc" -type f -delete


# Runs a quick demo from main.py
.PHONY: demo
demo:
	uv run main.py