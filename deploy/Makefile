SHELL := /bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:

.DEFAULT_GOAL: help

TERRAFORM_RESOURCES=s3 domain cognito dynamodb iam authorizer lambda api-gateway scheduling

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

plan_infra:
	source ../conf.sh
	source ../secret.conf.sh
	for resource in $(TERRAFORM_RESOURCES)
	do
		./wrapper.sh plan dev $$resource
	done;

build_infra:
	source ../conf.sh
	source ../secret.conf.sh
	for resource in $(TERRAFORM_RESOURCES)
	do
		./wrapper.sh apply dev $$resource
	done;

.PHONY: deploy_website
deploy_website:
	aws s3 cp ../website/index.html s3://hallebarde-dev-website --region eu-west-1

lint:
	for resource in $(TERRAFORM_RESOURCES)
	do
		$(MAKE) lint_infra_for AWS_RESOURCE=$$resource
	done

lint_infra_for: check_resource
	@echo -e "\033[35m 🚧 Validating TF files in deploy/$(AWS_RESOURCE)... \033[0m"
	cd $$AWS_RESOURCE
	TF_IN_AUTOMATION=true terraform init -input=false -backend=false && terraform validate

check_resource:
	@[ "${AWS_RESOURCE}" ] || (echo "⚠️ AWS_RESOURCE is not set"; exit 1)
