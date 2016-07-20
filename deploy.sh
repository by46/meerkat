#!/usr/bin/env bash

docker run --rm -v $1:/home/matrix -v /usr/bin/docker:/usr/bin/docker -v /var/run/docker.sock:/var/run/docker.sock docker.neg/matrix:0.0.2 /usr/local/bin/matrix.sh