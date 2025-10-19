# Facebook Pages dbt Transformation Models Makefile

.PHONY: help install deps run test docs clean

help:  ## Show this help message
	@echo "Facebook Pages dbt Transformation Models Commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install Python dependencies
	pip install -r requirements.txt

deps:  ## Install dbt dependencies
	dbt deps

run:  ## Run all dbt models
	dbt run

run-staging:  ## Run only staging models
	dbt run --select staging

run-marts:  ## Run only mart models
	dbt run --select facebook_pages__pages_report facebook_pages__posts_report

test:  ## Run dbt tests
	dbt test

compile:  ## Compile dbt models without running
	dbt compile

docs:  ## Generate and serve dbt documentation
	dbt docs generate
	dbt docs serve

docs-generate:  ## Generate dbt documentation only
	dbt docs generate

seed:  ## Load seed data (if any)
	dbt seed

snapshot:  ## Run dbt snapshots (if any)
	dbt snapshot

build:  ## Run models, tests, and snapshots
	dbt build

clean:  ## Remove dbt artifacts
	rm -rf target/
	rm -rf logs/
	rm -rf dbt_packages/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

dev-setup:  ## Setup development environment
	python -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	dbt deps
	@echo "Development environment ready! Activate with: source venv/bin/activate"
	@echo "Configure your database connection in .dbt/profiles.yml"

check-connection:  ## Test database connection
	dbt debug

pipeline:  ## Run the complete dbt pipeline
	dbt deps
	dbt run
	dbt test

deploy:  ## Deploy to production (run with production profile)
	dbt run --target prod
	dbt test --target prod

lint:  ## Format SQL files (requires sqlfluff)
	@if command -v sqlfluff >/dev/null 2>&1; then \
		sqlfluff format models/; \
	else \
		echo "sqlfluff not installed. Install with: pip install sqlfluff"; \
	fi