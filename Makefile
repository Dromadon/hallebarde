SHELL := /bin/bash
.PHONY: deploy package build_infra quality_checks

build_infra:
	cd deploy/; \
	./wrapper.sh apply dev s3; \
	./wrapper.sh apply dev iam; \
	./wrapper.sh apply dev authorizer; \
	./wrapper.sh apply dev lambda; \
	./wrapper.sh apply dev api-gateway; \

package:
	cd app/; \
	rm package/*.zip; \
	zip -j package/get_token.zip hallebarde/get_token.py; \
	zip -j package/get_presigned_url.zip hallebarde/get_presigned_url.py; \
	zip -j package/authorizer.zip hallebarde/authorizer.py; \

deploy: package build_infra

quality_checks:
	mypy --ignore-missing-imports app/;
	flake8 --ignore=E501 app/;
