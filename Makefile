.PHONY: help install test test-unit test-integration test-e2e test-all coverage lint format clean

help:
	@echo "Comandes disponibles:"
	@echo "  make install          - Instal·lar dependències"
	@echo "  make test            - Executar tests unitaris i d'integració"
	@echo "  make test-unit       - Executar només tests unitaris"
	@echo "  make test-integration - Executar només tests d'integració"
	@echo "  make test-e2e        - Executar tests E2E (requereix Chrome)"
	@echo "  make test-all        - Executar tots els tests"
	@echo "  make coverage        - Generar report de cobertura HTML"
	@echo "  make lint            - Executar linters (flake8, pylint)"
	@echo "  make format          - Formatar codi amb black"
	@echo "  make clean           - Netejar fitxers temporals"
	@echo "  make run             - Executar servidor Flask"

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/unit tests/integration -v

test-unit:
	pytest tests/unit -v -m unit

test-integration:
	pytest tests/integration -v -m integration

test-e2e:
	@echo "⚠️  IMPORTANT: Tests E2E requereixen Chrome/Chromium instal·lat"
	@echo "Instal·la Chrome amb: sudo apt install chromium-browser"
	pytest tests/e2e -v -m e2e

test-all:
	pytest tests/unit tests/integration tests/e2e -v

coverage:
	pytest tests/unit tests/integration --cov=api --cov=app --cov-report=html --cov-report=term-missing
	@echo "\n✅ Report de cobertura generat a: htmlcov/index.html"

lint:
	flake8 api app.py tests --max-line-length=100 --exclude=venv
	pylint api app.py --disable=C0111,C0103,R0913

format:
	black api app.py tests --line-length=100

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache htmlcov .coverage
	@echo "✅ Fitxers temporals netejats"

run:
	python app.py

.DEFAULT_GOAL := help
