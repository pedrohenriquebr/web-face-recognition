# Web Face Recognition

## Instalação

### Requisitos
  * Docker 18.06+
  * Docker Compose 1.23.0-rc3+
  * Python 3.3+ ou Python 2.7
  * Linux 

### Instalação de dependências
  * [Instalando Docker e Compose](https://gist.github.com/pedrohenriquebr/5c0676e74ade52d1e8ae676835dccb08)

### Amostra de base de dados
  * [Dataset](https://drive.google.com/drive/folders/1QcVSeMT2tGXO-oMZkyBhuDGqBgmXRBmh?usp=sharing)
  
    baixe, descomprima e coloque as pastas dentro de dataset

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
    - `hog`
    - `cnn` (rede neural treinada, pode ser usado com KNN)

  * `UNKNOWN_LABEL`
  
    rótulo para pessoa desconhecida

  * `THRESHOLD`

    flag para usar limiar no algoritmo K-NN (não funcional)



#### Referências bibliográficas
  * [Face Recognition](https://github.com/ageitgey/face_recognition)
  

