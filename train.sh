#!/usr/bin/env bash

# Shell script para executar o script python de treinamento de dentro do container.
# É necessário chamar "python3 training.py " dentro do container, então é usado o docker-compose exec, 
# claro que é preciso especificar qual arquivo de configuração usar (docker-compose.yml) passando como parâmetro '-f'.
function docker_compose_check(){
    if  ! command -v docker-compose  > /dev/null;
    then
        echo "instalando docker-compose..."

        sudo curl -L https://github.com/docker/compose/releases/download/1.23.1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
}


function docker_check(){
    if !  command -v docker > /dev/null ; 
    then
        echo "instalando docker..."
        curl -fsSL https://get.docker.com -o /tmp/get-docker.sh
        sh /tmp/get-docker.sh
    fi
}


docker_check
docker_compose_check

docker-compose -f docker-compose.dev.yml exec web python3 training.py





