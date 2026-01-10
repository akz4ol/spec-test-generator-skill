.PHONY: help install dev test lint format typecheck coverage clean build publish docker-build docker-run validate-policy

PYTHON := python3
PIP := pip3

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

install: ## Install package in development mode
	$(PIP) install -e .

dev: ## Install package with development dependencies
	$(PIP) install -e ".[dev]"

test: ## Run tests
	pytest tests/ -v

lint: ## Run linters
	ruff check src/ tests/
	ruff format --check src/ tests/

format: ## Format code
	ruff format src/ tests/
	ruff check --fix src/ tests/

typecheck: ## Run type checking
	mypy src/

coverage: ## Run tests with coverage
	pytest tests/ -v --cov=src/spec_test_generator --cov-report=html --cov-report=term

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf spec/
	find . -type d -name __pycache__ -exec rm -rf {} +

build: clean ## Build package
	$(PYTHON) -m build

publish: build ## Publish to PyPI (requires credentials)
	twine upload dist/*

docker-build: ## Build Docker image
	docker build -t spec-test-generator:latest .

docker-run: ## Run Docker container with example
	docker run --rm -v $(PWD)/skills/spec-test-generator/resources/examples:/prds spec-test-generator:latest /prds/prd_input.md

validate-policy: ## Validate policy files against schema
	$(PYTHON) scripts/validate_policies.py

# Example targets
example: ## Run generator on example PRD
	$(PYTHON) -m spec_test_generator skills/spec-test-generator/resources/examples/prd_input.md

example-strict: ## Run generator with strict policy
	$(PYTHON) -m spec_test_generator skills/spec-test-generator/resources/examples/prd_input.md --strict

example-json: ## Run generator with JSON output
	$(PYTHON) -m spec_test_generator skills/spec-test-generator/resources/examples/prd_input.md --json

all: lint typecheck test ## Run all checks
