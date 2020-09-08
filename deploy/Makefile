SHELL := /bin/bash
.SHELLFLAGS = -e -c
.ONESHELL:
env := dev

.DEFAULT_GOAL: help

TERRAFORM_RESOURCES=s3 domain cognito dynamodb iam authorizer lambda api-gateway scheduling

.PHONY: help
help:
	@echo "Please use 'make <target>' where <target> is one of"
	@grep -E '^\.PHONY: [a-zA-Z_-]+ .*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "(: |##)"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$3}'

plan_infra:
	source ../conf.sh
	source ../secret.conf.sh
	cd environments/${env}
	terragrunt plan-all --terragrunt-exclude-dir website

build_infra:
	source ../conf.sh
	source ../secret.conf.sh
	cd environments/${env}
	terragrunt apply-all --terragrunt-non-interactive --terragrunt-exclude-dir website

.PHONY: deploy_website
deploy_website:
	source ../conf.sh
	source ../secret.conf.sh
	cd environments/${env}/website/ 
	terragrunt apply --terragrunt-non-interactive

lint_terraform:
	for resource in modules/*
	do
		$(MAKE) lint_infra_for AWS_RESOURCE=$$resource
	done

lint_infra_for: check_resource
	@echo -e "\033[35m 🚧 Formating TF files in deploy/$(AWS_RESOURCE)... \033[0m"
	cd $$AWS_RESOURCE
	terraform fmt

lint_terragrunt:
	@echo -e "\033[35m 🚧 Validating HCL files in environments... \033[0m"
	cd environments
	terragrunt hclfmt --terragrunt-check

check_resource:
	@[ "${AWS_RESOURCE}" ] || (echo "⚠️ AWS_RESOURCE is not set"; exit 1)
