BASE_FACE_RECOGNITION_DIR=base_face_recognition
BASE_FACE_RECOGNITION_DOCKERFILE=$(BASE_FACE_RECOGNITION_DIR)/Dockerfile

WEB_FACE_RECOGNITION_IMAGE=web_face_recognition
BASE_FACE_RECOGNITION_IMAGE=base_face_recognition

# Declaro que todos o arquivos YAML têm como dependência
# o Dockerfile da imagem base no diretório base_facerecognition.
%.yml : $(BASE_FACE_RECOGNITION_DOCKERFILE)

# Construo os contêineres
# Isso aqui demora hein... pegue um cafézinho e tenha paciência...
build: Dockerfile $(BASE_FACE_RECOGNITION_DOCKERFILE)
	mkdir -p modelset
	echo "Construindo imagens bases..."
	cd $(BASE_FACE_RECOGNITION_DIR)
	docker build --rm -t $(BASE_FACE_RECOGNITION_IMAGE) .
	cd ..
	docker build --rm -t $(WEB_FACE_RECOGNITION_IMAGE) .
	echo "Imagens bases construídas com sucesso!"

# Removo os contêineres
clean: *.yml
	docker-compose -f docker-compose.dev.yml down
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose.yml rm -sf
	docker-compose -f docker-compose.dev.yml rm -sf

# Executo o contêiner
run: docker-compose.yml modelset/*.clf
	docker-compose -f docker-compose.yml up -d

# Executo o contêiner para desenvolvimento
run_dev: docker-compose.dev.yml modelset dataset
	docker-compose -f docker-compose.dev.yml up -d --build

# Paro a execução dos contêineres
stop: docker-compose.dev.yml docker-compose.yml
	docker-compose -f docker-compose.yml stop
	docker-compose -f docker-compose.dev.yml stop

# Shell script para executar o script python de treinamento de dentro do container.
# É necessário chamar "python3 training.py " dentro do container, então é usado o docker-compose exec
# Obs: só possível fazer treinamento em ambiente de desenvolvimento.
train: dataset modelset docker-compose.dev.yml
	docker-compose -f docker-compose.dev.yml exec web python3 training.py