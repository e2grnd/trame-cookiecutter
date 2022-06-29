CURRENT_DIR=`dirname "$0"`
PS3='Please select a base image: '
images=("kitware/trame" "kitware/trame:glvnd")
select image in "${images[@]}"; do
    selected_image=$image
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
    $selected_image

if [ "$selected_image" == "kitware/trame" ]; then
    docker_file=Dockerfile
    tag=""
else
    docker_file=Dockerfile.glvnd
    tag=":glvnd"
fi

cd $CURRENT_DIR/..
docker build -f docker_file -t {{cookiecutter.package_name}}$tag .
cd -
