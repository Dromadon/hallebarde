#!/bin/bash
set -o errexit


export BACKEND_BUCKET="hallebarde"

BASE_DIR=$(dirname $(realpath $0))
export TF_LOG=DEBUG;
export TF_LOG_PATH=/tmp/terraform_log;

# Sets auto yes for apply command
COMMAND=$1
if [[ $COMMAND = "apply" ]]; then
  COMMAND="apply --auto-approve"
fi

ENV=$2

# remove potential trailing slash in topology name
KEY=${3%/}

cd $BASE_DIR/$KEY

if [ ! -f $ENV.tfvars ]; then
  echo "tfvars file is absent, skipping"
  exit 0
fi

rm -rf .terraform/

terraform init \
    -backend-config="bucket=$BACKEND_BUCKET" \
    -backend-config="key=$KEY-$ENV" \
    -backend-config="region=eu-west-1"
echo "Terraform init has finished";
terraform get .

terraform $COMMAND $TOPOLOGY_TF_CLI_ARGS -var-file="$ENV.tfvars"

rm -rf .terraform/

