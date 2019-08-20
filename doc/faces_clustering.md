# Clusterização de faces

## Guia

Baixe ao mínimo 5 imagens para cada pessoa, coloque todas as fotos no diretório `dataset-raw`. 
Obs: não precisa separar as imagens em pastas diferentes.

```console
$ ls dataset-raw/
$ barackObama_foto_perfil.jpeg Donald_trump.jpeg Rihanna_UOL_imagem.JPEG ...
```

### Workflow

(opcional,recomendado) Faça a *standardização* dos nomes dos arquivos.

```console
$ bash standard.sh
$ ls dataset-raw/
$ 0001.jpeg 0002.jpeg ... 0042.jpeg
```

> O intuito de usar esse script, é para facilitar a identificação das imagens durante os testes.
> Ex: O arquivo que se chama `Donald_web1234568.jpeg` fica mais fácil de se localizar renomeado como `0034.jpeg`.

Treine DBSCAN.

```console
$ make build run encoding-raw train-dbscan
```

Será criado um arquivo `clusters.csv` no diretório `dataset-clusters`, contendo as classes ou *clusters* associados para cada arquivo.

```csv
clusters.csv

0,0043.jpeg
1,0033.jpeg
2,0013.jpeg
1,0036.jpeg
3,0003.jpeg
...
```

Crie um arquivo chamado `labels.csv` dentro do diretório `dataset-raw`, contendo o nome de 
uma imagem e o nome da pessoa contida, semelhante a seguir:

```csv
labels.csv

0001.jpeg,barack obama
0015.jpeg,donal trump
0022.jpeg,keanu reeves
0036.jpeg,rihanna
0043.jpeg,robin williams
...
```

Faça a *clusterização*.

```console
$ make clustering
```

`clustering` irá ler `clusters.csv` e colocar as imagens nos devidos diretórios, criando para *cluster*.

```console
./dataset-clusters/
├── 0
│   ├── 0042.jpeg
│   ├── 0043.jpeg
│   ├── 0044.jpeg
│   ├── 0045.jpeg
│   └── 0046.jpeg
├── 1
│   ├── 0032.jpeg
│   ├── 0033.jpeg
│   ├── 0034.jpeg
...
├── 2
│   ├── 0011.jpeg
│   ├── 0012.jpeg
│   ├── 0013.jpeg
...
├── 3
│   ├── 0001.jpeg
│   ├── 0002.jpeg
│   ├── 0003.jpeg
...
├── 4
│   ├── 0021.jpeg
│   ├── 0022.jpeg
│   ├── 0023.jpeg
...
└── clusters.csv

5 directories, 47 files
```

Rode dbscan para poder associar o nome correto das pessoas com o identificardor dos clusters.

```console
$ make pred-dbscan
```

Será criado um arquivo `names.csv` em `dataset-clusters`, contendo os nomes e seus devidos *clusters*.

```csv
names.csv

0,robin williams
1,rihanna
4,keanu reeves
2,donal trump
3,barack obama
```

(opcional,recomendado) Gere um cache dos atributos das faces.

```console
$ make encoding-clusters
$ ls dataset-clusters
./dataset-clusters/
├── 0
├── 1
├── 2
├── 3
├── 4
└── __cache__
    ├── 0
    ├── 1
    ├── 2
    ├── 3
    └── 4
```

> O sistema de cache de atributos é importante pois facilita o processo de treino de qualquer classificador, pois uma vez que tenha o atributo já salvo, não há a necessidade de usar *detecção* de faces e *extração de atributos*, que é bem lento.


