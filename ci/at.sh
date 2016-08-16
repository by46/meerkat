#!/bin/sh

IMAGE=$(sirius docker_image_name | head -n 1)

sirius docker_deploy:meerkat,${IMAGE},server=scdfis01,ports="3141;8080",env="ENV\=gqc"