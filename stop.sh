#!/usr/bin/env bash

test -n "$DEBUG" && set -x

docker-compose -f docker-compose.yml stop
docker-compose -f docker-compose.dev.yml stop