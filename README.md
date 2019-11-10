⚔️ Hallebarde ⚔️
===========

Token-based file uploader on AWS

Hallebarde is meant to be a sensitive file-sharing system, with upload/download token creation controled through an OIDC provider. Typically, Google Auth would be plugged on hallebarde in your AWS account, and allow people from your Google Organization to manage upload/download tokens. These tokens can be privately shared with people _outside_ your organization for them to access or upload files.

## Requirements

You need to have `Terraform >= 1.12.0` and `Pipenv` installed on your computer

You also need credentials for an AWS IAM account with nearly full-admin rights:
 - IAM : Create/WriteRole, Create/WritePolicy, List*
 - Lambda : Write*
 - S3 : CreateBucket and associated rights on that bucket
 - APIGateway : Write*

## How to use

Please refer to the detailed [deployment guide](docs/Deployment.md)

## Run tests

Once you have ran at least once `pip install .`, you can execute every test suites with `make tests`.

* You can find tests about the Hallebarde app in `./app/tests/`
* You can find tests about some makefile recipes in `./tests`
