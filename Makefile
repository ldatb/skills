# ldatb/skills — deterministic toolchain entrypoints.
# Every target is reproducible: same input, same result. No hidden state.

PYTHON ?= python3
VENV   := .venv
BIN    := $(VENV)/bin

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show this help.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

$(BIN)/activate:
	$(PYTHON) -m venv $(VENV)

.PHONY: install
install: $(BIN)/activate ## Create venv, install tooling + dev deps + pre-commit hooks.
	$(BIN)/pip install --upgrade pip
	$(BIN)/pip install -e ".[dev]"
	$(BIN)/pip install pre-commit
	$(BIN)/pre-commit install

.PHONY: lint
lint: ## Run skill-lint (strict) on every skill. Blocks on any violation.
	$(BIN)/skill-lint --strict skills/

.PHONY: lint-fix
lint-fix: ## Apply skill-lint's deterministic autofixes (frontmatter normalization).
	$(BIN)/skill-lint --fix skills/

.PHONY: docs
docs: ## Check that every Markdown link and file reference resolves.
	$(BIN)/skill-docs .

.PHONY: test
test: ## Run the toolchain test suite.
	$(BIN)/pytest

.PHONY: format
format: ## Format + autofix Python tooling with ruff.
	$(BIN)/ruff check --fix tools/
	$(BIN)/ruff format tools/

.PHONY: sca
sca: ## Static analysis on the toolchain (Semgrep). Blocks on findings.
	$(BIN)/semgrep scan --error --quiet --config semgrep.yml --config p/python --config p/secrets tools/

.PHONY: new-skill
new-skill: ## Scaffold a conformant skill. Usage: make new-skill CATEGORY=engineering NAME=my-skill
	$(BIN)/skill-new --category "$(CATEGORY)" --name "$(NAME)"

.PHONY: ci
ci: lint docs test sca ## Everything CI runs, locally. Green here == green there.
	$(BIN)/ruff check tools/
