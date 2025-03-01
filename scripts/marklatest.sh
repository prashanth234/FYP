#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Requries version. example ./script.sh d2.0.0"
    exit 1  # Exit the script with a non-zero status code
fi

docker tag prashanth45/fyp:frontendv$1 prashanth45/fyp:frontendvlatest
docker tag prashanth45/fyp:backendv$1 prashanth45/fyp:backendvlatest

docker push prashanth45/fyp:frontendv$1
docker push prashanth45/fyp:backendv$1

docker push prashanth45/fyp:frontendvlatest
docker push prashanth45/fyp:backendvlatest