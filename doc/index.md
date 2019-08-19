## Makefile

> Pré-requisitos: você precisa rodar colocar as imagens nas pas

Constroi a imagem base docker, levanta o container, extrai os atributos das imagens e treina todos os classificadores disponíveis.

```console
$ make all
```

Idem o de cima, porém coloca em modo de desenvolvimento.

```console
$ make all-dev
```

Idem o de cima, porém treina apenas o classificador SVM

```console
$ make all-svm
```

Idem o de cima, porém treina apenas o classificador SVM em modo de desenvolvimento

```console
$ make all-svm-dev
```

Constrói a imagem docker.

```console
$ make build
```

Levanta o container em modo de produção.

```console
$ make run
```

Levanta o container em modo de desenvolvimento.

```console
$ make run-dev
```

Para todos os contêineres em execução.

```console
$ make stop
```

Exibe saída de `docker-compose ps`, ou seja, exibe quais conteineres estão rodando.

```console
$ make status
```

Remove os conteineres em execução.

```console
$ make clean
```

Remove arquivos das pastas: dataset, testset, modelset

```console
$ make clean-data
```

Gera um backup em formato zip.

```console
$ make backup
```

Deleta imagem base do web-face-recognition.

```console
$ make rmi
```

Extrai atributos das faces nas imagens e gera arquivo a partir deles.

```console
$ make encoding
```

Treina todos os classificadores.

```console
$ make train
```

Treina algum classificador específico, por enquanto há apenas para SVM e KNN.

```console
$ make train-knn
$ make train-svm
```

Acessar o terminal do container.

```console
$ make terminal
```

Clusterização de faces, ainda em testes.

```console
$ make test-clusters
```


### Workflow

O workflow do makefile precisa seguir essa ordem:

standard => encoding-raw => train-dbscan => clustering => encoding-clusters
