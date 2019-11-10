# Deployment
## Pre-requisites
In order to deploy hallebarde to your organization, you need the following pre-requisites:
 - An AWS account and a user of this account with the following rights:
   - IAM: Admin (Hallebarde needs to create roles and grant them)
   - S3: CreateBucket, DeleteBucket
   - DynamoDB: ListTables, CreateTable, DeleteTable
   - Lambda: ListLambdas, CreateLambda, DeleteLambda
 - `terraform >= 0.12` installed on your computer
 - AWS Credentials set in your shell (either with env variables or ~/.aws credentials file)
 - An OIDC provider. At the moment, Hallebarde only support Google
 - A domain name with the ability to set custom NS for the subdomain you will dedicate to Hallebarde

You don't need anything related to `python` for pure deployment as you do not need to modify the code. 
Deployment is based on `Makefile` and `terraform`

## Steps
### One-shot activities
#### Creating the OIDC application
You need to create an OIDC application in your provider, which will be used by Hallebarde to authenticate calls. We only support Google OIDC today, so you should end with an id looking like `274210205449-bend56f57m2gcu9an3q6dmv0atj3i7h1.apps.googleusercontent.com` that you will insert in the `TF_VAR_google_oidc_application` variable in `conf.sh`

#### Creating the AWS Route53 Zone
You need to create a zone for the base domain of hallebarde in AWS Route53. 
Hallebarde will use 2 domains : One for serving the web application, and one for the API.

If `filetransfer.myfirm.com` is the base domain you will dedicate to Hallebarde:
 - Create a Route53 Zone for the domain `filetransfer.myfirm.com`
 - Insert `filetransfer.myfirm.com` in the `TF_VAR_route53_zone_name` var in `conf.sh`
Hallebarde will spontaneously serve the web app on `filetransfer.myfirm.com` and expose the api on `api.filetransfer.myfirm.com`

#### Creating the NS record in your root domain pointing to the Route53 Zone
First gather the AWS nameservers for your zone. They are located in the base `filetransfer.myfirm.com` NS record of your zone.

Then in your base domain `myfirm.com` registrar interface, create a new NS record and insert the AWS nameservers as hostnames.
 
### Actual deployment
Still with your AWS credentials sourced, run `make deploy` at the root directory. Please note that the first time, Hallebarde will automatically create signed certificates and associated CloudFront distributions, and this can take up to 45 minutes until you can effectively use the application and run all the end-to-end tests.