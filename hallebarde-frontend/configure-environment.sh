#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset
set -o errtrace

function get_env () {
  if [ $1 == "local" ]; then
    echo "dev"
  else
    echo $1
  fi
}

function get_web_client () {
  if [ $1 == "local" ]; then
    echo "local"
  else
    echo "web"
  fi
}

env="$(get_env $1)"

declare -A fields
fields=([user_pool_id]="REACT_APP_USER_POOL_ID"
[$(get_web_client $1)_client_id]="REACT_APP_USER_POOL_WEB_CLIENT_ID"
[oauth_domain]="REACT_APP_OAUTH_DOMAIN"
[$(get_web_client $1)_client_callback_url]="REACT_APP_OAUTH_CALLBACK_URL"
[$(get_web_client $1)_client_signout_url]="REACT_APP_OAUTH_SIGNOUT_URL"
[api_domain_name]="REACT_APP_BACKEND_URL")

function replace_env_with_tf_output () {
  while read -r l; do
    echo "Working on output line ${l}"
    for i in "${!fields[@]}"; do
      # echo "Working on var ${i}"
      tf_output_name=$i
      if grep -q "$tf_output_name" <<< "$l"; then
        echo "Found output $tf_output_name"
        tf_output_value=$(echo $l | awk -F "${tf_output_name} = " '{print $2}')
        echo "Output value is $tf_output_value"

        react_var_name=${fields[$i]}
        echo "React var name is $react_var_name"
        # Note the "" after -i, needed in OS X
        echo "Substituting…"
        sed -r -i "s~(${react_var_name}=\").+~\1${tf_output_value}\"~" .env
      fi
    done
  done < <(cd ../deploy/environments/${env}/$1/ && terragrunt output)
}

replace_env_with_tf_output api-gateway
replace_env_with_tf_output cognito

