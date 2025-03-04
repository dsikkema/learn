#!/usr/bin/env bash
CONTAINER_NAME=linux_dev
container_running=$(docker inspect $CONTAINER_NAME | jq -r ".[0].State.Running")
if [[ $container_running == "false" ]]; then
    echo "Starting docker container $CONTAINER_NAME"
    docker start $CONTAINER_NAME
fi
