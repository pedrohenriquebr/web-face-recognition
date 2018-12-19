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
* [x] Classificação facial com [K-NN](www.computacaointeligente.com.br/algoritmos/knn-k-vizinhos-mais-proximos/).

### Amostra de base de dados

* [Dataset](https://drive.google.com/drive/folders/1QcVSeMT2tGXO-oMZkyBhuDGqBgmXRBmh?usp=sharing)
  
    baixe, descomprima e coloque as pastas dentro de `dataset`

## Variáveis de ambiente

As variáveis se encontram no arquivo `src/.env` e são carregadas pelo `settings.py`, modifique conforme suas necessidades.

* `DATASET_DIR`
  
   Diretório da base de dados para treinamento

* `MODELSET_DIR`
  
   Diretório de classificadores salvos e treinados

* `KNN_MODEL`
  
  Nome do arquivo do modelo de classificador KNN

* `N_NEIGHBORS`
  
  Particularidade do KNN, se não estiver declarado, `n_neighbors` assumirá
  `int(round(math.sqrt(len(X))))`, onde `X` é número de pessoas a serem treinadas pelo algoritmo (apenas uma conveção);
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

Faça instalação de dependências e a construção de imagens bases de forma automática: 

```bash
./bootstrap.sh
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

Para iniciar o contêiner em modo de desenvolvimento, use:

```bash
./init_dev.sh
```

Para iniciar o contêiner em modo de produção, use:

```bash
./init.sh
```

Parar execução dos contêineres:

```bash
./stop.sh
```

> Funcionará tanto para contêineres de produção quanto para desenvolvimento.

### Treinamento

Utilize:

```bash
./train.sh
```

> O treinamento só é possível no modo de desenvolvimento, visto que em modo de produção
> o diretório `modelset` é montado em modo de somente-leitura. Isso fica evidente, pois é criado um arquivo do classificador KNN, salvo com o nome especificado pela variável `KNN_MODEL`.

### Removendo contêineres

Para limpar os contêineres em execução, use:

```bash
./clean.sh
```

> Esse script removerá tanto as interfaces de rede quanto os contêineres.

## Sugestões de leitura

* [Docker Curriculum](https://docker-curriculum.com/)
* [Compose file version 3 Reference](https://docs.docker.com/compose/compose-file/)
* [Modern Face Recognition with Deep Learning](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78)
* [Face Recognition](https://github.com/ageitgey/face_recognition)
* [Face Recognitino API Documentation](https://face-recognition.readthedocs.io/en/latest/face_recognition.html)
