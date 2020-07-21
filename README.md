⚔️ Hallebarde ⚔️
===============

![Python application](https://github.com/Dromadon/hallebarde/workflows/hallebarde%20application/badge.svg)

*Token-based file uploader on AWS*

Hallebarde is meant to be a sensitive file-sharing system, with upload/download token creation controled through an OIDC provider. Typically, Google Auth would be plugged on hallebarde in your AWS account, and allow people from your Google Organization to manage upload/download tokens. These tokens can be privately shared with people _outside_ your organization for them to access or upload files.

## Requirements

|                               	| Bash >4.0 	| Python >3.8 	| Pipenv 	| npm 	| Terraform >12.0 	| Terragrunt >0.23 	|
|-------------------------------	|-----------	|-------------	|--------	|-----	|-----------------	|------------------	|
| Build infrastructure          	| x         	|             	|        	|     	| x               	| x                	|
| Package backend code          	| x         	| x           	| x      	|     	|                 	|                  	|
| Run backend unit tests        	| x         	| x           	| x      	|     	|                 	|                  	|
| Run functional tests          	| x         	| x           	| x      	|     	| x               	| x                	|
| Configure frontend            	| x         	|             	|        	|     	| x               	| x                	|
| Start local frontend server   	|           	|             	|        	| x   	|                 	|                  	|
| Build frontend for deployment 	| x         	|             	|        	| x   	|                 	|                  	|
| Deploy frontend               	| x         	|             	|        	|     	| x               	| x                	|

You also need credentials for an AWS IAM account with nearly full-admin rights:
 - IAM : Create/WriteRole, Create/WritePolicy, List*
 - Lambda : Write*
 - S3 : CreateBucket and associated rights on that bucket
 - APIGateway : Write*
 

## General considerations
### Functional capacity
Hallebarde creates simple file exchange between people inside and outside your organization. At the
moment, only file uploading towards people outside the organization is possible. Having external people
upload files for people inside the organization is not yet implemented in the frontend.

Please note that due to UX choices, Hallebarde does not provide any listing of exchanges. This is 
fire & forget.

Hallebarde provides a minimum  of compliance with automated fixed-delay deletion 7 days after the exchanges
are created.

In the future, we are susceptible to add some key features:
- Working upload from the outside workflow
- Email alerting when file is uploaded/downloaded/deleted
- Custom automated deletion delay

### Structure
Hallebarde code is structured around three main subdirectories:
 - `app/` which contains all the backend code, unit tests and functional tests
 - `hallebarde-frontend/` which contains all the frontend code and its unit tests
 - `deploy/` which contains all the infrastructure as code for both backend and frontend, including deployment tasks 
 of backend and frontend code
 
 
### Usage
Each directory is thought to be nearly-independent (you obviously still need a backend package in order to 
_deploy_the backend for exemple)

You will find in each directory:
- A `Readme.md` describing the philosophy, usage, and helpful commands of this part of the code
- A `Makefile` providing all necessary commands for development / packaging / deployment

## How to deploy
Please refer to the detailed [deployment guide](deploy/Readme.md)

## How to develop / test / package the backend
Please refer to the detailed [backend development guide](app/Readme.md)

## How to develop / test / package the frontend
Please refer to the detailed [frontend development guide](hallebarde-frontend/Readme.md)

## Deep-dives
- [General architecture](Docs/Architecture.md)
- [Technical workflow](Docs/Flow.md)
