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

docker run -it $gpu_arg -p 8080:80 \
    -e STORAGE_API_SERVICE_HOST=10.128.0.31 \
    -e INTERNAL_AUTH_SHARED_SECRET \
    -- restart=always \
    -d vis-{{cookiecutter.package_name}}$tag
