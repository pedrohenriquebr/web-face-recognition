# Web Face Recognition

## Installation

### Requirements

* Docker 18.06+
* Docker Compose 1.23.1+
* Python 3.3+ ou Python 2.7
* Linux (Debian based distro)

### Dependency installation

* [Installing Docker](https://docs.docker.com/v17.12/install/)
* [Installing Docker Compose](https://docs.docker.com/v17.09/compose/install/)
* [Installing Git](https://git-scm.com/book/pt-br/v1/Primeiros-passos-Instalando-Git)

### Goals

* [ ] Face recognition with HoG
* [ ] Face classification with K-NN

## Environment variables

The variables can be found on the src/.env file and are loaded by the settings.py, modify according to your needs.

* `DATASET_DIR`

    Database directory for training

* `MODELSET_DIR`
  
   Saved and trained classifiers directory

* `KNN_MODEL`
  
  KNN classifier model file name

* `N_NEIGHBORS`
  
  Number of neighbors, the standard is square root of the number of people.

* `FACE_DETECTION_MODEL`
  
  Face detection model that's going to be utilized, can assume the following values:
  * `hog` (default)
  * `cnn` (trained neural network, can be used with KNN, not functional)

* `UNKNOWN_LABEL`
  
  Label for unknown person, only activated when `THRESHOLD` assumes `TRUE`.

* `THRESHOLD`
  
  To activate predifined threshold on K-NN. When it assumes value TRUE, K-NN will return the label for unknown person. When it assumes value FALSE K-NN will return the label for the person that is the most resemblant of the individual from the test picture, even if it's not in the database it's recommended to generate Confusion Matrix.
  