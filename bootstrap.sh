#!/usr/bin/env bash

test -n "$DEBUG" && set -x

function docker_compose_check(){
    echo "verificando docker-compose..."
    if  ! command -v docker-compose  > /dev/null;
    then
        echo "instalando docker-compose..."
        sudo pip3 install -U docker-compose
    fi
}


function docker_check(){
    echo "verificando docker..."
    if !  command -v docker > /dev/null ; 
    then
        echo "instalando docker..."
        curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
        sh /tmp/get-docker.sh
        sudo usermod -aG docker $USER 
    fi
}

# Instalo algumas dependências
docker_check
docker_compose_check
mkdir -p {modelset,dataset,testset}