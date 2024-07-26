#!/usr/bin/env bash

# Locally, this script should be run as `integration_test.apply.sh``
# from `model-deployment`` directory which is has a distinct python environment
# this directory also contains the docker-compose file needed to start docker containers

if [[ -z "${GITHUB_ACTIONS}" ]]; then
  cd "$(dirname "$0")"
fi

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then 
    LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
    export LOCAL_IMAGE_NAME="webapp:${LOCAL_TAG}"
    echo "Building a new image ${LOCAL_IMAGE_NAME}"
    docker build -t ${LOCAL_IMAGE_NAME} ..
else
    echo "Image ${LOCAL_IMAGE_NAME} already exist"
fi

docker-compose up -d

sleep 5

pipenv run python integration_test/test_pred.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker-compose logs
    docker-compose down
    exit ${ERROR_CODE}
fi

docker-compose down