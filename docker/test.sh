#!/usr/bin/env bash

set -eux

TAG="pytest-its-whats-for-testing:test"

docker build -f docker/Dockerfile -t "$TAG" .
docker run -it --rm "$TAG" $@
