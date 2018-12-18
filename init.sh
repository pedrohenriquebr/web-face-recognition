#!/usr/bin/env bash

test -n "$DEBUG" && set -x

docker-compose -f docker-compose.yml up -d