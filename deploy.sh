#!/usr/bin/env bash

docker run --rm -v $1:/home/matrix -v /var/run/docker.sock:/var/run/docker.sock matrix:0.0.2 /usr/local/bin/matrix.sh