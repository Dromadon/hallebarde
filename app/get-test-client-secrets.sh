#!/bin/usr/env bash

echo "Getting end2end client secrets from TF output"
while read -r l; do
  export $l
done < <(../deploy/wrapper.sh output dev cognito/ | grep "end2end" | sed 's/ //g')
