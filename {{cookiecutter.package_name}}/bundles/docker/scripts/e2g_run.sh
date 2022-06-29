#!/usr/bin/env bash
PS3='Does the target machine have a supported NVIDIA GPU?: '
options=("yes" "no")
select option in "${options[@]}"; do
    gpu_support=$option
    break
done

if [ "$gpu_support" == "no" ]; then
    gpu_arg=""
else
    gpu_arg="--gpus all"
fi

docker run -it --rm $gpu_arg -p 8080:80 -d {{cookiecutter.package_name}}