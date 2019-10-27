SHELL := /bin/bash

.PHONY: deploy package build_infra tests quality_checks

build_infra:
	cd deploy/; \
	./wrapper.sh apply dev s3; \
	./wrapper.sh apply dev dynamodb; \
	./wrapper.sh apply dev iam; \
	./wrapper.sh apply dev authorizer; \
	./wrapper.sh apply dev lambda; \
	./wrapper.sh apply dev api-gateway; \

package:
	cd app/; \
	find package -type f -name "*.zip" -exec rm {} +; \
	zip -r package/hallebarde.zip hallebarde/; \

deploy: package build_infra

tests:
	pipenv run pytest -vv -p no:warnings ./;

quality_checks:
	pipenv run mypy --ignore-missing-imports app/;
	pipenv run flake8 --ignore=E501 app/;
