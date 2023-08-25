#!/usr/bin/env bash

CURRENT_DIR=`dirname "$0"`
PS3='Does the target machine have an NVIDIA GPU?: '
options=("yes" "no")
select option in "${options[@]}"; do
    gpu_support=$option
    break
done

pushd .
cd $CURRENT_DIR/..
DEPLOY_DIR=$PWD
cd $CURRENT_DIR/../../..
ROOT_DIR=$PWD
popd

docker run --rm          \
    -e TRAME_BUILD_ONLY=1 \
    -v "$DEPLOY_DIR:/deploy" \
    -v "$ROOT_DIR:/local-app"  \
    gcr.io/sandbox-225221/trame:builder build

if [ "$gpu_support" == "no" ]; then
    docker_file=Dockerfile.osmesa
    name="{{cookiecutter.entry_point}}-osmesa"
else
    docker_file=Dockerfile.egl
    name="{{cookiecutter.entry_point}}-egl"
fi

hash=$(git rev-parse release/dev)
cd $CURRENT_DIR/..
docker build -f $docker_file -t gcr.io/sandbox-225221/trame/$name:$hash -t gcr.io/sandbox-225221/trame/$name:latest .
docker push gcr.io/sandbox-225221/trame/$name -a
cd -
