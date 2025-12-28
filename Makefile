# Makefile for shconfparser

.PHONY: help install dev-install test lint format type-check clean build publish

help:
	@echo "Available commands:"
	@echo "  install       - Install the package"
	@echo "  dev-install   - Install package with development dependencies"
	@echo "  test          - Run tests with coverage"
	@echo "  lint          - Run ruff linter"
	@echo "  format        - Format code with black and ruff"
	@echo "  type-check    - Run mypy type checking"
	@echo "  clean         - Remove build artifacts"
	@echo "  build         - Build distribution packages"
	@echo "  publish       - Publish to PyPI (requires credentials)"

install:
	uv pip install -e .

dev-install:
	uv pip install -e . --dev

test:
	pytest

lint:
	ruff check .

format:
	black .
	ruff check --fix .

type-check:
	mypy shconfparser

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	uv build

publish: build
	uv publish

check-all: format type-check test
	@echo "All checks passed!"
