#!/bin/bash
readonly SCRIPT_DIRECTORY=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

function main() {
  echo "[*] Executing Terraform commands..."

  set -o errexit
  set -o pipefail
  set -o nounset
  set -o errtrace

  export BACKEND_BUCKET="hallebarde"
  export TF_LOG=DEBUG
  export TF_LOG_PATH=/tmp/terraform_log

  readonly COMMAND=$(auto_approve_if_apply "${1}")
  readonly ENV=${2}
  readonly KEY=$(remove_trailing_slash_if_any "${3}")
  readonly BACKEND_BUCKET="hallebarde"
  readonly TOPOLOGY_TF_CLI_ARGS=""

  cd "${SCRIPT_DIRECTORY}/${ENV}"

  if is_tfvars_file_absent_in "${ENV}"; then
    echo "[*] .tfvars file is absent, quitting now..."
    exit 0
  fi

  terraform_init "${BACKEND_BUCKET}" "${KEY}" "${ENV}"
  terraform_do "${COMMAND}" "${TOPOLOGY_TF_CLI_ARGS}" "${ENV}"
}

function auto_approve_if_apply() {
  local -r command=${1}
  if [[ $command == "apply" ]]; then
    echo "${command} --auto-approve"
  fi
}

function remove_trailing_slash_if_any() { echo "${1%/}"; }

function is_tfvars_file_absent_in() {
  local -r env=${1}
  [ ! -f "${SCRIPT_DIRECTORY}/${env}/.tfvars" ]
}

function terraform_init() {
  local -r backend_bucket=${1}
  local -r key=${2}
  local -r env=${3}
  echo "[*] Terraforming in $(pwd) directory..."
  terraform init \
    -backend-config="bucket=${backend_bucket}" \
    -backend-config="key=${key}-${env}" \
    -backend-config="region=eu-west-1"
  echo "[*] Terraform working directory is initialized..."
  terraform get .
  echo "[*] Terraform modules are loaded..."
}

function terraform_do() {
  local -r command=${1}
  local -r tf_cli_args=${2}
  local -r env=${3}
  echo "terraform ${command} ${tf_cli_args} -var-file=\"$env/.tfvars\""
  terraform ${command} ${tf_cli_args} -var-file="$env/.tfvars"
  echo "[*] Terraform command applied successfully..."
}

main "$@"
