#!/bin/bash
set -e

ARTIFACTS_BUCKET="TODO"

pushd lambda

array=(
  slack_app_immediate_response
  slack_app_async_worker
  slack_app_sync_worker
)

for item in ${array[*]}; do
    zip ${item}.zip ${item}.py
    echo "Created ${item}.zip"

    aws s3 cp ${item}.zip  s3://${ARTIFACTS_BUCKET}/${item}.zip
    echo "Uploaded to s3://${ARTIFACTS_BUCKET}/${item}.zip"

    rm ${item}.zip
    echo "Removed local ${item}.zip"
done

popd
