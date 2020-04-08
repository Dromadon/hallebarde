SHELL := /bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:

.DEFAULT_GOAL: help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: deploy ## Deploy dist/ static website content to AWS bucket
deploy: package
	aws s3 sync dist/ s3://hallebarde-dev-website --delete --region eu-west-1

.PHONY: package  ## Produces a production-ready bundle in the dist/ directory
package: clean install-dependencies
	npm run build

.PHONY: clean  ## Remove dist/ bundle and node_modules/ folder
clean:
	rm -rf node_modules/ dist/ --verbose

.PHONY: install-dependencies  ## Install application dependencies
install-dependencies:
	npm install
