#!/usr/bin/env bash
PS3='Does the target machine have a supported NVIDIA GPU?: '
options=("yes" "no")
select option in "${options[@]}"; do
    gpu_support=$option
    break
done

if [ "$gpu_support" == "no" ]; then
    gpu_arg=""
    tag=":osmesa"
else
    gpu_arg="--gpus all"
    tag=":egl"
fi

docker run --name {{cookiecutter.package_name}} $gpu_arg -p {{cookiecutter.port}}:80 \
    -e STORAGE_API_SERVICE_HOST \
    -e INTERNAL_AUTH_SHARED_SECRET \
    -e BUCKET_FOLDER \
    --restart=always \
    -d {{cookiecutter.package_name}}$tag
