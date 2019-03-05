#!/usr/bin/env bash

MAJOR=''
MINOR=''
PATCH=''
VARIANT=''
TAG=''

function build_image(){
    docker build -f $1 --rm -t $2 $3
}

function building(){
    # Base images building
    echo "Building the image $DOCKER_USERNAME/web_face_recognition:$TAG"
    build_image "$PWD/Dockerfile" "$DOCKER_USERNAME/web_face_recognition:latest" "$PWD"
    docker tag "$DOCKER_USERNAME/web_face_recognition:latest" "$DOCKER_USERNAME/web_face_recognition:$TAG"
}

function info(){
    MAJOR=$(echo $TAG | cut -d'.' -f1)
    MINOR=$(echo $TAG | cut -d'.' -f2)
    PATCH=$(echo $TAG | cut -d'.' -f3)
    VARIANT=$(echo $TAG | cut -d'-' -f2)

    MAJOR=${MAJOR%-*}
    MINOR=${MINOR%-*}
    PATCH=${PATCH%-*}

    echo Major: $MAJOR
    test $(echo ${TAG} | tr -cd "." | wc -c ) -ge 1 && echo Minor: $MINOR
    test $(echo ${TAG} | tr -cd "." | wc -c ) -ge 2 && echo Patch: $PATCH
    test $(echo ${TAG} | tr -cd "-" | wc -c ) -ge 1 && echo VARIANT: $VARIANT
}

function main(){

info

building

# Login
echo "$DOCKER_PASSWORD" | docker login --username "$DOCKER_USERNAME" --password-stdin

if [ "$?" -ne "0" ]; then
    exit 1
fi

echo "Sending to Docker Hub..."
docker push ${DOCKER_USERNAME}/web_face_recognition:${TAG}
docker push ${DOCKER_USERNAME}/web_face_recognition:latest

docker logout

}


if [ -z "$DOCKER_USERNAME" ] || [ -z "$DOCKER_PASSWORD" ]; then
    echo "You have to declare \$DOCKER_USERNAME and \$DOCKER_PASSWORD!"
    exit 1
fi

if [ -z "$@" ]; then
    echo "No arguments passed!"
    exit 1
fi

TAG="$1"

main