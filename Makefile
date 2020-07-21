SHELL := /bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:
env := dev

.DEFAULT_GOAL: help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: deploy_backend  ## Package the app, build the infrastructure and deploy the app in it as a lambda function
deploy_backend: package_backend
	$(MAKE) --directory deploy/ build_infra env=${env}

.PHONY: package_backend  ## Package the app in zip format
package_backend:
	$(MAKE) --directory app/ package

.PHONY: deploy_frontend
deploy_frontend:
	$(MAKE) --directory deploy/ deploy_website

.PHONY: tests  ## Run unit & functional tests
tests:
	$(MAKE) --directory app/ tests

.PHONY: lint  ## Run quality and security checks
lint:
	$(MAKE) --directory app/ lint
	$(MAKE) --directory deploy/ lint


