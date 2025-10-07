.PHONY: help start stop install dev backend frontend db-up db-down logs-backend logs-frontend clean

# Default target
.DEFAULT_GOAL := help

# Colors
GREEN  := \033[0;32m
YELLOW := \033[1;33m
NC     := \033[0m

help: ## Show this help message
	@echo "$(GREEN)Fintech Tracker - Bloomberg for the Everyman$(NC)"
	@echo ""
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

start: ## Start the entire application (database + backend + frontend)
	@./scripts/start.sh

stop: ## Stop the entire application
	@./scripts/stop.sh

install: ## Install all dependencies (backend + frontend)
	@echo "$(YELLOW)Installing backend dependencies...$(NC)"
	@cd backend && python3 -m venv venv && . venv/bin/activate && pip install -r requirements.txt
	@echo "$(GREEN) Backend dependencies installed$(NC)"
	@echo ""
	@echo "$(YELLOW)Installing frontend dependencies...$(NC)"
	@cd frontend && npm install
	@echo "$(GREEN) Frontend dependencies installed$(NC)"

dev: start ## Alias for 'start' - Start development environment

backend: ## Run backend only
	@cd backend && . venv/bin/activate && python -m app.main

frontend: ## Run frontend only
	@cd frontend && npm run dev

db-up: ## Start database services (PostgreSQL + Redis)
	@docker-compose up -d

db-down: ## Stop database services
	@docker-compose down

logs-backend: ## View backend logs
	@tail -f logs/backend.log

logs-frontend: ## View frontend logs
	@tail -f logs/frontend.log

clean: ## Clean up logs and temporary files
	@echo "$(YELLOW)Cleaning up...$(NC)"
	@rm -f logs/*.log logs/*.pid
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN) Cleanup complete$(NC)"

reset: clean db-down ## Full reset (stop everything, clean logs)
	@echo "$(GREEN) Full reset complete$(NC)"
