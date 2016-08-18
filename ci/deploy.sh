#!/bin/sh

IMAGE=$(sirius docker_image_name | head -n 1)

# build release image

RELEASE_IMAGE=$(sirius docker_image_name:release=true | head -n 1)

docker tag -f ${IMAGE} docker.neg/${RELEASE_IMAGE}

docker push docker.neg/${RELEASE_IMAGE}

[ $? -gt 0 ] && exit 2

exit 0