SHELL := /bin/bash

.PHONY: deploy package build_infra tests func_tests quality_checks
.ONESHELL:

deploy: package build_infra

tests: unit_tests func_tests

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

package:
	cd app/
	rm -r package/*
	pipenv run pip install --target package/ .
	cd package/
	zip -r hallebarde.zip *

unit_tests:
	AWS_DEFAULT_REGION='eu-west-1' pipenv run pytest -vv -p no:warnings ./;

func_tests:
	source secret.conf.sh && \
	AWS_DEFAULT_REGION=eu-west-1 pipenv run behave app/tests/functional/features/

quality_checks:
	pipenv run mypy --ignore-missing-imports app/ || true
	pipenv run flake8 app/
