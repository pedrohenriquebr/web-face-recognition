#!/usr/bin/env bash

test -n "$DEBUG" && set -x

function docker_compose_check(){
    echo "Verifying docker-compose..."
    if  ! command -v docker-compose  > /dev/null;
    then
        echo "installing docker-compose..."
        sudo pip3 install -U docker-compose
    fi
}


function docker_check(){
    echo "Verifying docker..."
    if !  command -v docker > /dev/null ; 
    then
        echo "installing docker..."
        curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
        sh /tmp/get-docker.sh
        sudo usermod -aG docker $USER 
    fi
}

# Instalo algumas dependências
docker_check
docker_compose_check

op=""
while   [ "$op"  != 'y' ] && [ "$op" !=  'n' ] && [ "$op" != 'Y'  ] && [ "$op" != 'N' ] ; do 
    read -p 'Do you want install dlib?' op
done

if [ "$op" = 'N' ] || [ "$op" = 'n' ]; then
    exit 1
fi

sudo su << EOF
apt-get -y update
apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    python3-pip \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

cd ~ && mkdir -p dlib && \
    git clone -b 'master' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python3 setup.py install

EOF