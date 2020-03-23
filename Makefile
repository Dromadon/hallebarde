SHELL := /bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:

.DEFAULT_GOAL: help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: deploy  ## Package the app, build the infrastructure and deploy the app in it as a lambda function
deploy: package
	$(MAKE) --directory deploy/ build_infra

.PHONY: package  ## Package the app in zip format
package:
	$(MAKE) --directory app/ package

.PHONY: tests  ## Run unit & functional tests
tests:
	$(MAKE) --directory app/ tests

.PHONY: lint  ## Run quality and security checks
lint:
	$(MAKE) --directory app/ lint
	$(MAKE) --directory deploy/ lint


