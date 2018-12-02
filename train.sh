#!/usr/bin/env bash

# Shell script para executar o script python de treinamento de dentro do container.
# É necessário chamar "python3 training.py " dentro do container, então é usado o docker-compose exec, 
# claro que é preciso especificar qual arquivo de configuração usar (docker-compose.yml) passando como parâmetro '-f'.

docker-compose -f docker-compose.dev.yml exec web python3 training.py





