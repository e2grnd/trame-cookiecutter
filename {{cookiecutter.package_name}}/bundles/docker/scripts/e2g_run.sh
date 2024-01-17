#!/usr/bin/env bash

PS3='Does the target machine have a supported NVIDIA GPU?: '
options=("yes" "no")
select option in "${options[@]}"; do
    gpu_support=$option
    break
done

if [ "$gpu_support" == "no" ]; then
    gpu_arg=""
    name="{{cookiecutter.entry_point}}-osmesa"
else
    gpu_arg="--gpus all"
    name="{{cookiecutter.entry_point}}-egl"
fi

docker run --name {{cookiecutter.entry_point}} $gpu_arg -p {{cookiecutter.port}}:80 \
    -e STORAGE_API_SERVICE_HOST \
    -e INTERNAL_AUTH_SHARED_SECRET \
    -e BUCKET_FOLDER \
    --restart=always \
    -d gcr.io/sandbox-225221/$name/trame:latest
