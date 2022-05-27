#!/usr/bin/env bash
CURRENT_DIR=`dirname "$0"`

# Since Mac doesn't come with realpath by default, let's set the full
# paths using PWD.
pushd .
cd $CURRENT_DIR/..
DEPLOY_DIR=$PWD
popd

docker run -it --rm --gpus all \
    -p {{cookiecutter.port}}:80 \
    -v "$DEPLOY_DIR:/deploy" \
    -d \
    e2grnd/trame:glvnd
