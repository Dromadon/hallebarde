SHELL := /bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:

.DEFAULT_GOAL: help
.EXPORT_ALL_VARIABLES:

env := dev

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

.PHONY: package  ## Package the app in zip format
package:
	-rm -rf package/* build/ dist/
	pipenv run pip install --target package/ .
	cd package && zip -r hallebarde.zip *

.PHONY: tests  ## Run unit & functional tests
tests: unit_tests func_tests

.PHONY: unit_tests  ## Run unit tests with pytest + compute coverage
unit_tests:
	AWS_ACCESS_KEY_ID='a_key' AWS_SECRET_ACCESS_KEY='a_secret' AWS_DEFAULT_REGION='eu-west-1' \
	pipenv run pytest -vv -p no:warnings --cov=hallebarde/ tests/;

.PHONY: func_tests  ## Run functional tests with behave
func_tests:
	echo "Getting end2end client secrets from TF output"
	while read -r l; do
	  echo $$l
	  export $$l
	done < <(cd ../deploy/environments/${env}/cognito/ && terragrunt output | grep "end2end" | sed 's/ //g')
	AWS_DEFAULT_REGION=eu-west-1 pipenv run behave tests/functional/features/

.PHONY: lint  ## Run quality and security checks
lint: quality_checks security_checks

.PHONY: quality_checks  ## Run quality checks (mypy, flake8)
quality_checks:
	-pipenv run mypy hallebarde/ tests/
	pipenv run flake8 hallebarde/

.PHONY: security_checks  ## Run security checks on python code and dependencies
security_checks:
	pipenv run bandit --recursive hallebarde/ --exclude tests/
	pipenv run safety check --full-report

