SHELL := /bin/bash
.SHELLFLAGS = -ec
.ONESHELL:

.DEFAULT_GOAL: help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | \
	sort | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: install-dependencies  ## ⏬ Install all dependencies. You can install prod-only dependencies with NODE_ENV=production.
install-dependencies:
	npm install

.PHONY: test ## ✅ Run the unit tests
tests:
	CI=true npm test

.PHONY: tests-with-coverage  ## ✅ 📏 Run the unit tests and measure code coverage
tests-with-coverage:
	CI=true npm test -- --coverage

