#!/bin/bash
set -eu

# wait until light node comes up
until [ "$(curl -s -w '%{http_code}' -o /dev/null "http://da:26659/header/1")" -eq 200 ]; do
  echo "waiting for light node to be ready"
  sleep 5
done


local_head=$(curl "http://da:26659/head" -s | jq -r '.header.height')
remote_head=$(curl "${CELESTIA_API}/header" -s | jq -r '.result.header.height')

until [ "$local_head" -eq "$remote_head" ]; do
    echo "Waiting for celestia light node to be synced..."
    echo "local_head: $local_head"
    echo "remote_head: $remote_head"
    sleep 5
    local_head=$(curl "http://da:26659/head" -s | jq -r '.header.height')
    remote_head=$(curl "${CELESTIA_API}/header" -s | jq -r '.result.header.height')
done

exec ./op-node-entrypoint