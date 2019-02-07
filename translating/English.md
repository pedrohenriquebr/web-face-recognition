# Web Face Recognition

## Installation

### Requirements

* Docker 18.06+
* Docker Compose 1.23.1+
* Python 3.3+ ou Python 2.7
* Linux (Debian based distro)

### Goals

* [x] Face recognition with HoG
* [x] Face classification with K-NN

## Guide

Clone the repository:

```console
$ git clone https://github.com/pedrohenriquebr/web-face-recognition.git
```

Go to the cloned project directory:

```console
$ cd web-face-recognition
```

Start the bootstrap script:

```console
$ ./bootstrap.sh
```

### Registering people

Inside the dataset directory, create the directory with the name or the label of who you want to recognize with the person's picture. Having the same amount of pictures for each individual is the ideal.

### Starting containers

Build the base images for the containers:

```console
$ make
```

To start the container on development mode, use:

```console
$ make run-dev
```

To start the container on production mode, use:

```console
$ make run
```

To stop the containers:

```console
$ make stop
```


> It will work on both production and development containers.

### Training

Use:

```console
$ make train
```

> Training is only possible on development mode, since on production mode the modelset directory is built in only-reading mode.

### Removing containers

To clean running containers, use:

```console
$ make clean
```

> This script will remove both the network interfaces and the containers.

## Reading suggestions

* [Modern Face Recognition with Deep Learning](https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78)
* [Face Recognition](https://github.com/ageitgey/face_recognition)
* [Face Recognitino API Documentation](https://face-recognition.readthedocs.io/en/latest/face_recognition.html)z