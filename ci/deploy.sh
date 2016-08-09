#!/bin/sh

IMAGE=$(sirius docker_image_name | head -n 1)

sirius docker_deploy:meerkat,${IMAGE},server=scmesos06,ports="3141;3141",env="ENV\=prd"
