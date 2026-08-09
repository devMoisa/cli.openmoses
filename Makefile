.DEFAULT_GOAL := help

.PHONY: help setup dev test lint format check

help: ## Lista os comandos disponíveis
	@echo "Openmoses"
	@echo ""
	@echo "  make setup   Instala e sincroniza as dependências"
	@echo "  make dev     Abre a TUI do Openmoses"
	@echo "  make test    Executa os testes"
	@echo "  make lint    Verifica a qualidade do código"
	@echo "  make format  Formata o código Python"
	@echo "  make check   Executa lint e testes"

setup: ## Instala e sincroniza as dependências
	uv sync

dev: ## Abre a TUI do Openmoses
	uv run openmoses

test: ## Executa os testes
	uv run pytest

lint: ## Verifica a qualidade do código
	uv run ruff check .
	uv run ruff format --check .

format: ## Formata o código Python
	uv run ruff check --fix .
	uv run ruff format .

check: lint test ## Executa todas as verificações
