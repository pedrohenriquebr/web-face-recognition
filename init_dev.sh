#!/usr/bin/env bash

test -n "$DEBUG" && set -x

docker-compose -f docker-compose.dev.yml up -d --build

