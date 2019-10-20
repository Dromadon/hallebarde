SHELL := /bin/bash

.PHONY: deploy package build_infra tests quality_checks

build_infra:
	cd deploy/; \
	./wrapper.sh apply dev s3; \
	./wrapper.sh apply dev iam; \
	./wrapper.sh apply dev authorizer; \
	./wrapper.sh apply dev lambda; \
	./wrapper.sh apply dev api-gateway; \
	./wrapper.sh apply dev dynamodb; \

package:
	cd app/; \
	find package -type f -name "*.zip" -exec rm {} +; \
	zip -j package/get_token.zip hallebarde/get_token.py; \
	zip -j package/get_presigned_url.zip hallebarde/get_presigned_url.py; \
	zip -j package/authorizer.zip hallebarde/authorizer.py; \

deploy: package build_infra

tests:
	pipenv run pytest ./;

quality_checks:
	mypy --ignore-missing-imports app/;
	flake8 --ignore=E501 app/;
