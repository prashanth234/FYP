#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Requries version and servicename. example ./script.sh d2.0.0 servicename"
    exit 1  # Exit the script with a non-zero status code
fi

docker tag prashanth45/fyp:${2}v${1} prashanth45/fyp:${2}vlatest

docker push prashanth45/fyp:${2}v$1

docker push prashanth45/fyp:${2}vlatest