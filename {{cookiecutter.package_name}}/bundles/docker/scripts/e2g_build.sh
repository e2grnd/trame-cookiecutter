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
    kitware/trame:glvnd

if [ "$gpu_support" == "no" ]; then
    docker_file=Dockerfile
    tag=":osmesa"
else
    docker_file=Dockerfile.egl
    tag=":egl"
fi

cd $CURRENT_DIR/..
docker build -f $docker_file -t vis-{{cookiecutter.package_name}}$tag .
cd -
