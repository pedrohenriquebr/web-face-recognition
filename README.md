# Web Face Recognition

## Instalação

### Requisitos
  * Docker 18.06+
  * Docker Compose 1.23.0-rc3+
  * Python 3.3+ ou Python 2.7
  * Linux
  * Git

### Instalação de dependências
  * [Instalando Docker e Compose](https://gist.github.com/pedrohenriquebr/5c0676e74ade52d1e8ae676835dccb08)
  * [Instalando Git](https://git-scm.com/book/pt-br/v1/Primeiros-passos-Instalando-Git)


### Amostra de base de dados
  * [Dataset](https://drive.google.com/drive/folders/1QcVSeMT2tGXO-oMZkyBhuDGqBgmXRBmh?usp=sharing)
  
    baixe, descomprima e coloque as pastas dentro de `dataset`

## Variáveis de ambiente 
  
  * `DATASET_DIR` 
  
    diretório da base de dados para treinamento

  * `MODELSET_DIR` 
  
    diretório de classificadores salvos e treinados

  * `KNN_MODEL` 
  
    nome do arquivo do modelo de classificador KNN 
    
  * `N_NEIGHBORS`
  
    particularidade do KNN se não estiver declarado, n_neighbors assumirá o 
    valor da raíz quadrada do número de indivíduos no dataset
se não for um valor válido, n_neighbors assumirá
o valor `1` 

  * `CNN_MODEL`
    
    nome do arquivo do modelo de classificador CNN, não implementado

  * `FACE_DETECTION_MODEL`
  
    modelo de detecção de faces a ser utilizado, pode assumir os seguintes valores:
    - `hog` (valor padrão)
    - `cnn` (rede neural treinada, pode ser usado com KNN)

  * `UNKNOWN_LABEL`
  
    rótulo para pessoa desconhecida

  * `THRESHOLD`

    flag para usar limiar no algoritmo K-NN (não funcional

### Guia
Clone o repositório: 
```bash 
$ git clone https://bitbucket.org/nupemteam/face_recognition.git
```
ou clone já com seu usuário:
```bash
$ git clone https://<usuario>@bitbucket.org/nupemteam/face_recognition.git
```
Construa a imagem base do face_recognition:
```bash
$ cd base_face_recognition
$ docker build -t base_face_recognition .
```

Construa a imagem base para web de face_recognition:
```bash
$ cd ../
$ docker build -t web_face_recognition . 
```

Utilize o Compose para rodar os contêineres:
* Para ambiente de produção:
```bash
$ docker-compose up -d --build -f docker-compose.prod.yml
```
* Para ambiente de desenvolvimento:
```bash
$ docker-compose up -d --build -f docker-compose.dev.yml
```

#### Sugestões de leitura
* [Docker Curriculum](https://docker-curriculum.com/)
* [Face Recognition](https://github.com/ageitgey/face_recognition)
* [Modern Face Recognition with Deep Learning](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78)
  

