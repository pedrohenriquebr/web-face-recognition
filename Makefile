BASE_FACE_RECOGNITION_DIR=base_face_recognition
WEB_FACE_RECOGNITION_DIR=$(PWD)
BASE_FACE_RECOGNITION_DOCKERFILE=$(BASE_FACE_RECOGNITION_DIR)/Dockerfile
WEB_FACE_RECOGNITION_DOCKERFILE=$(WEB_FACE_RECOGNITION_DIR)/Dockerfile

WEB_FACE_RECOGNITION_IMAGE=web_face_recognition
BASE_FACE_RECOGNITION_IMAGE=base_face_recognition


DOCKER_BUILD_FLAGS=--rm

# Declaro que todos o arquivos YAML têm como dependência
# o Dockerfile da imagem base no diretório base_facerecognition.
%.yml: $(BASE_FACE_RECOGNITION_DOCKERFILE)
# Construo os contêineres
# Isso aqui demora hein... pegue um cafézinho e tenha paciência...

define build_image
	docker build -f $(1) $(DOCKER_BUILD_FLAGS) -t $(2) $(3)
endef

build: $(WEB_FACE_RECOGNITION_DOCKERFILE) $(BASE_FACE_RECOGNITION_DOCKERFILE) src modelset
	$(call build_image,$(BASE_FACE_RECOGNITION_DOCKERFILE),$(BASE_FACE_RECOGNITION_IMAGE),$(BASE_FACE_RECOGNITION_DIR))
	$(call build_image,$(WEB_FACE_RECOGNITION_DOCKERFILE),$(WEB_FACE_RECOGNITION_IMAGE),$(WEB_FACE_RECOGNITION_DIR))

# Executo o contêiner
run: docker-compose.yml modelset/*.clf
	docker-compose -f docker-compose.yml up -d

# Executo o contêiner para desenvolvimento
run-dev: docker-compose.dev.yml modelset dataset
	docker-compose -f docker-compose.dev.yml up -d --build

# Paro a execução dos contêineres
stop: *.yml
	docker-compose stop

status: *.yml
	docker-compose ps

# Removo os contêineres
clean: *.yml
	docker-compose down

# Além de remover os contêineres, remove a imagem base
erase: clean
	rm -f modelset/*.clf
	docker rmi $(WEB_FACE_RECOGNITION_IMAGE)
	#docker rmi $(BASE_FACE_RECOGNITION_IMAGE)

# Shell script para executar o script python de treinamento de dentro do container.
# É necessário chamar "python3 training.py " dentro do container, então é usado o docker-compose exec
# Obs: só possível fazer treinamento em ambiente de desenvolvimento.

train: run_dev
	docker-compose -f docker-compose.dev.yml exec web python3 training.py

terminal:
	docker-compose exec web bash
	#docker exec -it face_recognition_web_1_b123e52ab166 bash