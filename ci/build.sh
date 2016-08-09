#!/usr/bin/env bash

sirius docker_build_image

# failure with non-zero return code
[ $? -gt 0 ] && exit 1

IMAGE=$(sirius docker_image_name | head -n 1)

docker tag -f ${IMAGE} docker.neg/${IMAGE}

# failure with non-zero return code
[ $? -gt 0 ] && exit 1

docker push docker.neg/${IMAGE}

# failure with non-zero return code
[ $? -gt 0 ] && exit 1

exit 0