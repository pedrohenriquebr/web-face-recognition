#!/usr/bin/env bash

function build_image(){
    docker build -f $1 --rm -t $2 $3
}

function building(){
    # Base images building
    echo "Building the image base_face_recognition:latest"
    build_image "base_face_recognition/Dockerfile" "base_face_recognition:latest" "base_face_recognition"

    echo "Building the image $DOCKER_USERNAME/web_face_recognition:$TAG"
    build_image "$PWD/Dockerfile" "web_face_recognition:latest" "$PWD"
    docker tag "web_face_recognition:latest" "$DOCKER_USERNAME/web_face_recognition:$TAG"
    docker tag "web_face_recognition:latest" "$DOCKER_USERNAME/web_face_recognition:latest"
}

function main(){

MAJOR=$(echo $TAG | cut -d'.' -f1)
MINOR=$(echo $TAG | cut -d'.' -f2)
PATCH=$(echo $TAG | cut -d'.' -f3)


echo Major: $MAJOR
test $(echo ${TAG} | tr -cd "." | wc -c ) -ge 1 && echo Minor: $MINOR
test $(echo ${TAG} | tr -cd "." | wc -c ) -ge 2 && echo Patch: $PATCH

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
    echo "Error!"
    exit
fi

TAG="$1"

main