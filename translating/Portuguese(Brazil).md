# Web Face Recognition

## Instalação

### Requisitos

* Docker 18.06+
* Docker Compose 1.23.1+
* Python 3.3+ ou Python 2.7
* Linux (distro baseada no Debian)

### Metas

* [x] Detecção facial com HoG.
* [x] Classificação facial com K-NN

## Guia

Clone o repositório:

```console
$ git clone https://github.com/pedrohenriquebr/web-face-recognition.git
```

Entre no diretório do projeto clonado:

```console
$ cd web-face-recognition
```

Inicie o script de boostrap:

```console
$ ./bootstrap.sh
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

> O treinamento só é possível no modo de desenvolvimento, mas em modo de produção
> o diretório `modelset` é montado em modo de somente-leitura.

### Removendo contêineres

Para limpar os contêineres em execução, use:

```console
$ make clean
```

> Esse script removerá tanto as interfaces de rede quanto os contêineres.

## Sugestões de leitura

* [Modern Face Recognition with Deep Learning](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78)
* [Face Recognition](https://github.com/ageitgey/face_recognition)
* [Face Recognitino API Documentation](https://face-recognition.readthedocs.io/en/latest/face_recognition.html)
