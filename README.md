# Web Face Recognition

## Instalação

### Requisitos

* Docker 18.06+
* Docker Compose 1.23.1+
* Python 3.3+ ou Python 2.7
* Linux

### Instalação de dependências

* [Instalando Docker](https://docs.docker.com/v17.12/install/)
* [Instalando Docker Compose](https://docs.docker.com/v17.09/compose/install/)
* [Instalando Git](https://git-scm.com/book/pt-br/v1/Primeiros-passos-Instalando-Git)

### Metas

* [x] Detecção facial com HoG.
* [ ] Detecção facial com CNN.
* [x] Classificação facial com [K-NN](www.computacaointeligente.com.br/algoritmos/knn-k-vizinhos-mais-proximos/).

### Amostra de base de dados

* [Dataset](https://drive.google.com/drive/folders/1QcVSeMT2tGXO-oMZkyBhuDGqBgmXRBmh?usp=sharing)
  
    baixe, descomprima e coloque as pastas dentro de `dataset`

## Variáveis de ambiente

* `DATASET_DIR`
  
  Diretório da base de dados para treinamento

* `MODELSET_DIR`
  
  Diretório de classificadores salvos e treinados

* `KNN_MODEL`
  
  Nome do arquivo do modelo de classificador KNN

* `N_NEIGHBORS`
  
  Particularidade do KNN, se não estiver declarado, `n_neighbors` assumirá 
  `int(round(math.sqrt(len(X))))`, onde `X` é número de pessoas a serem treinadas pelo algoritmo;
se não for um valor válido, `n_neighbors` assumirá
o valor `1`.

* `FACE_DETECTION_MODEL`
  
  Modelo de detecção de faces a ser utilizado, pode assumir os seguintes valores:
  * `hog` (valor padrão)
  * `cnn` (rede neural treinada, pode ser usado com KNN, não funcional)

* `UNKNOWN_LABEL`
  
  Rótulo para pessoa desconhecida, só é ativada quando `THRESHOLD` é assume `TRUE`.

* `THRESHOLD`
  
  Para ativar limiar pré-definido no K-NN. Quando assume valor `TRUE`, K-NN retornará o rótulo para pessoa desconhecida. Quando assume valor `FALSE` K-NN retornará rótulo da pessoa mais parecida com o indivíduo da foto de teste, mesmo que não esteja na base de dados, é recomendado para gerar Matriz de Confusão].

## Guia

Clone o repositório:

```bash
git clone https://bitbucket.org/nupemteam/face_recognition.git
```

Entre no diretório do projeto clonado:

```bash
cd face_recognition
```

Construa a imagem base do face_recognition:

```bash
cd base_face_recognition
docker build -t base_face_recognition .
```

Construa a imagem base para web de face_recognition:

```bash
cd ../
docker build -t web_face_recognition . 
```

Utilize o Compose para rodar os contêineres:

Para ambiente de produção:

```bash
docker-compose -f docker-compose.yml up -d --build 
```

Para ambiente de desenvolvimento ou de testes:

```bash
docker-compose -f docker-compose.dev.yml up -d --build 
```

Caso queira a instalação de dependências e a construção de imagens bases de forma automática, utilize o script `bootstrap.sh`.

```bash
bash bootstrap.sh
```

## Cadastrando pessoas

Dentro do diretório `dataset` crie o diretório com nome ou rótulo de quem deseja reconhecer 
com as fotos da pessoa.  

## Sugestões de leitura

* [Docker Curriculum](https://docker-curriculum.com/)
* [Compose file version 3 Reference](https://docs.docker.com/compose/compose-file/)
* [Modern Face Recognition with Deep Learning](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78)
* [Face Recognition](https://github.com/ageitgey/face_recognition)
* [Face Recognitino API Documentation](https://face-recognition.readthedocs.io/en/latest/face_recognition.html)