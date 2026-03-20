.PHONY: dev.install db.migration.new db.migrate db.rollback db.up db.down

# Load .env if exists
-include .env
export

# Database URL from .env
DB_URL ?= postgresql://$(DB_USER):$(DB_PASSWORD)@$(DB_HOST):$(DB_PORT)/$(DB_NAME)
MIGRATIONS_DIR = ./migrations

dev.install:
	python3 -m venv .venv
	.venv/bin/pip install yoyo-migrations[postgres]
	@echo "Dependencies installed. Activate with: source .venv/bin/activate"

db.migration.new:
	@if [ -z "$(name)" ]; then echo "Usage: make db.migration.new name=\"migration description\""; exit 1; fi
	.venv/bin/yoyo new $(MIGRATIONS_DIR) -m "$(name)"

db.migrate:
	.venv/bin/yoyo apply --database "$(DB_URL)" $(MIGRATIONS_DIR) --batch

db.rollback:
	.venv/bin/yoyo rollback --database "$(DB_URL)" $(MIGRATIONS_DIR) --batch

db.up:
	docker compose up -d

db.down:
	docker compose down
