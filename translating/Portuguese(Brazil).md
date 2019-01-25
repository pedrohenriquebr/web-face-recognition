# Web Face Recognition

## Instalação

### Requisitos

* Docker 18.06+
* Docker Compose 1.23.1+
* Python 3.3+ ou Python 2.7
* Linux (distro baseada no Debian)

### Instalação de dependências

* [Instalando Docker](https://docs.docker.com/v17.12/install/)
* [Instalando Docker Compose](https://docs.docker.com/v17.09/compose/install/)
* [Instalando Git](https://git-scm.com/book/pt-br/v1/Primeiros-passos-Instalando-Git)

### Metas

* [x] Detecção facial com HoG.
* [x] Classificação facial com K-NN

## Variáveis de ambiente

As variáveis se encontram no arquivo `src/.env` e são carregadas pelo `settings.py`, modifique conforme suas necessidades.

* `DATASET_DIR`
  
    Diretório da base de dados para treinamento

* `MODELSET_DIR`
  
   Diretório de classificadores salvos e treinados

* `KNN_MODEL`
  
  Nome do arquivo do modelo de classificador KNN

* `N_NEIGHBORS`
  
  Número de vizinhos, o padrão é raiz quadrada do número de pessoas.

* `FACE_DETECTION_MODEL`
  
  Modelo de detecção de faces a ser utilizado, pode assumir os seguintes valores:
  * `hog` (padrão)
  * `cnn` (rede neural treinada, pode ser usado com KNN, não funcional)

* `UNKNOWN_LABEL`
  
  Rótulo para pessoa desconhecida, só é ativada quando `THRESHOLD` é assume `TRUE`.

* `THRESHOLD`
  
  Para ativar limiar pré-definido no K-NN. Quando assume valor `TRUE`, K-NN retornará o rótulo para pessoa desconhecida. Quando assume valor `FALSE` K-NN retornará rótulo da pessoa mais parecida com o indivíduo da foto de teste, mesmo que não esteja na base de dados, é recomendado para gerar Matriz de Confusão.

## Guia

Clone o repositório:

```console
$ git clone https://bitbucket.org/nupemteam/face_recognition.git
```

Entre no diretório do projeto clonado:

```console
$ cd face_recognition
```

Faça instalação de dependências:

```console
$ ./bootstrap.sh
```

### Reconhecimento Facial

O servidor web ouve requisições GET na porta 5000, acesse `http://ip_do_servidor:5000/` para ver uma
demonstração do reconhecimento.

Para o reconhecimento em si, o servidor recebe requisiçõe do tipo POST contendo as fotos, pelo endereço `http://ip_do_servidor:5000/api/recognition` e retorna o nome da pessoa reconhecida.

Trecho de código para fazer reconhecimento:

```python
def send_image(image_path):
   url = 'http://{RECOGNITION_HOST}:5000/api/recognition'.format(
      RECOGNITION_HOST=RECOGNITION_HOST)
   files = {'file': open(image_path, 'rb')}
   r = requests.post(url, files=files)
   return json.loads(r.text)
```

### Cadastrando pessoas

Dentro do diretório `dataset` crie o diretório com nome ou rótulo de quem deseja reconhecer
com as fotos da pessoa. O ideal é ter a mesma quantidade de fotos para cada indivíduo.

### Iniciando contêineres

Construa as imagens para os contêineres:

```console
$ make
```

Para iniciar o contêiner em modo de desenvolvimento, use:

```console
$ make run-dev
```

Para iniciar o contêiner em modo de produção, use:

```console
$ make run
```

Parar execução dos contêineres:

```console
$ make stop
```

> Funcionará tanto para contêineres de produção quanto para desenvolvimento.

### Treinamento

Utilize:

```console
$ make train
```

> O treinamento só é possível no modo de desenvolvimento, visto que em modo de produção
> o diretório `modelset` é montado em modo de somente-leitura. Isso fica evidente, pois é criado um arquivo do classificador KNN, salvo com o nome especificado pela variável `KNN_MODEL`.

### Removendo contêineres

Para limpar os contêineres em execução, use:

```console
$ make clean
```

> Esse script removerá tanto as interfaces de rede quanto os contêineres.

## Sugestões de leitura

* [Docker Curriculum](https://docker-curriculum.com/)
* [Compose file version 3 Reference](https://docs.docker.com/compose/compose-file/)
* [Modern Face Recognition with Deep Learning](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78)
* [Face Recognition](https://github.com/ageitgey/face_recognition)
* [Face Recognitino API Documentation](https://face-recognition.readthedocs.io/en/latest/face_recognition.html)
