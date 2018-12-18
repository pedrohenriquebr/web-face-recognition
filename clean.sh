#!/usr/bin/env bash

test -n "$DEBUG" && set -x

echo "Removendo..."
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.yml down
docker-compose -f docker-compose.yml rm -sf
docker-compose -f docker-compose.dev.yml rm -sf