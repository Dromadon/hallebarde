# Deployment
## Pre-requisites
In order to deploy hallebarde to your organization, you need the following pre-requisites:
 - An AWS account and a user of this account with the following rights (note that these are nearly full-admin rights, 
 so you may want to grant admin rights directly):
   - IAM: Admin (Hallebarde needs to create roles and grant them)
   - S3: CreateBucket, DeleteBucket
   - DynamoDB: ListTables, CreateTable, DeleteTable
   - Lambda: ListLambdas, CreateLambda, DeleteLambda
 - AWS Credentials set in your shell (either with env variables or ~/.aws credentials file)
 - An OIDC provider. At the moment, Hallebarde only support Google
 - A domain name with the ability to set custom NS for the subdomain you will dedicate to Hallebarde

All technical stacks listed in [main Readme.md](../README.md) for packaging backend & frontend and deploy infrastructure

## Steps
### One-shot activities
#### Creating the OIDC application
You need to create an OIDC application in your provider, which will be used by Hallebarde to authenticate calls. 

For this, you can provide to your OIDC application:
 - Authorized javascript origins: 
   - `https://[your app name].auth.eu-west-1.amazoncognito.com` for production environment
   - `https://dev-[your app name].auth.eu-west-1.amazoncognito.com` for dev environment
   - `http://localhost:3000` for local development
 - Redirect URI:
   - `https://[your app name].auth.eu-west-1.amazoncognito.com/oauth2/idpresponse` for production environment
   - `https://dev-[your app name].auth.eu-west-1.amazoncognito.com/oauth2/idpresponse` for dev and local environment

We only support Google OIDC today, so you should end with:
 - an id looking like 
`274210205449-bend56f57m2gcu9an3q6dmv0atj3i7h1.apps.googleusercontent.com` that you will insert in the 
[environments/terragrunt.hcl](environments/terragrunt.hcl)
- a secret that you will insert in a copy of the file `secret.conf.sh.tpl` that shall be named `secret.conf.sh`

#### Creating the AWS Route53 Zone
You need to create a public zone for the base domain of hallebarde in AWS Route53. 
Hallebarde will use 2 subdomains : One for serving the web application, and one for the API.

If `filetransfer.myfirm.com` is the base domain you will dedicate to Hallebarde:
 - Create a Route53 Zone for the domain `filetransfer.myfirm.com`
 - Insert `filetransfer.myfirm.com` in the `route53_zone_name` var in 
 [environments/terragrunt.hcl](environments/terragrunt.hcl)
 
Hallebarde will spontaneously serve the web app on `filetransfer.myfirm.com` and expose the api on 
`api.filetransfer.myfirm.com` <br />
Devlopment environment will be served on `dev.filetransfer.myfirm.com` and `dev.api.filetransfer.myfirm.com`

#### Creating the NS record in your root domain pointing to the Route53 Zone
First gather the AWS nameservers for your zone. They are located in the base `filetransfer.myfirm.com` NS record 
of your zone.

Then in your base domain `myfirm.com` registrar interface, create a new NS record and insert the 
AWS nameservers as hostnames.

#### Setting up the `pipenv` environment
At the root of the hallebarde directory, run ```pipenv install```

This will install the adequate python version and you will be ready for any packaging operation
 

### Actual deployment
#### Sourcing secrets
The only pre-existing secret in Hallebarde is the Google OIDC application secret. All other secrets are dynamically
generated and stored outside the code repository.

In order to make the deployment work, you need to run `source secret.conf.sh` for the Google OIDC application secret
to be available to Terraform during the deployment.

#### Targeting the right environment
All make commands for deploying / testing / getting secrets target real environments, and hence must precise which
environment is targeted by specifying the `env` variable:
```make my_target env=[dev|prod]```

#### First-time deployment specials
The first time you deploy, the backend for the remote state storage for Terraform does not exist. But Terragrunt
will automatically prompt you for creating it on you behalf. You just have to answer `yes` when it happens.

#### Deploying the backend
Still with your AWS credentials sourced, run `make deploy_backend env=dev` at the root directory for deploying to `dev`
environment

This will package the backend application and then create the associated infrastructure by calling the _Makefiles_ in 
`app/` and `deploy` directories

Please note that the first time, Hallebarde will automatically create signed certificates and associated 
CloudFront distributions, and this can take up to 45 minutes until you can effectively use the application 
and run all the end-to-end tests.

#### Deploying the frontend
Still with your AWS credentials sourced, run `make deploy_frontend env=dev` at the root directory. 
      
This will package the frontend application and then create the associated infrastructure by calling the _Makefiles_ in 
`app/` and `deploy` directories