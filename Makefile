SHELL := /bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:

.DEFAULT: help

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: deploy  ## Package the app, build the infrastructure and deploy the app in it as a lambda function
deploy: package build_infra

.PHONY: tests  ## Run unit & functional tests
tests: unit_tests func_tests

.PHONY: package  ## Package the app in zip format
package:
	cd app/
	rm -r package/*
	pipenv run pip install --target package/ .
	cd package/
	zip -r hallebarde.zip *

.PHONY: build_infra  ## Build the infrastructure with Terraform
build_infra:
	source conf.sh
	cd deploy/
	./wrapper.sh apply dev s3
	./wrapper.sh apply dev domain
	./wrapper.sh apply dev cognito
	./wrapper.sh apply dev dynamodb
	./wrapper.sh apply dev iam
	./wrapper.sh apply dev authorizer
	./wrapper.sh apply dev lambda
	./wrapper.sh apply dev api-gateway

.PHONY: unit_tests  ## Run unit tests with pytest + compute coverage
unit_tests:
	AWS_ACCESS_KEY_ID='a_key' AWS_SECRET_ACCESS_KEY='a_secret' AWS_DEFAULT_REGION='eu-west-1' \
	pipenv run pytest -vv -p no:warnings --cov=app/hallebarde/ app/tests/;

.PHONY: func_tests  ## Run functional tests with behave
func_tests:
	source secret.conf.sh && \
	AWS_DEFAULT_REGION=eu-west-1 pipenv run behave app/tests/functional/features/

.PHONY: lint  ## Run quality and security checks
lint: quality_checks security_checks

.PHONY: quality_checks  ## Run quality checks (mypy, flake8)
quality_checks:
	pipenv run mypy --ignore-missing-imports app/ || true
	pipenv run flake8 app/

.PHONY: security_checks  ## Run security checks on python code and dependencies
security_checks:
	pipenv run bandit --recursive app/ --exclude app/tests
	pipenv run safety check --full-report
