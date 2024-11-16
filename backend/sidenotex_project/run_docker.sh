#!/bin/zsh
docker run -p 8001:8001 \
  -e DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD \
  -e EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD \
  -v /Users/piotrek/docker_data_folders/sidenotex:/externaldata sidenotex