BASE_FACE_RECOGNITION_DIR=base_face_recognition
WEB_FACE_RECOGNITION_DIR=$(PWD)
BASE_FACE_RECOGNITION_DOCKERFILE=$(BASE_FACE_RECOGNITION_DIR)/Dockerfile
WEB_FACE_RECOGNITION_DOCKERFILE=$(WEB_FACE_RECOGNITION_DIR)/Dockerfile

WEB_FACE_RECOGNITION_IMAGE=web_face_recognition
BASE_FACE_RECOGNITION_IMAGE=base_face_recognition

DOCKER_BUILD_FLAGS=--rm

DATASETDIR := $(PWD)/dataset
TESTSET := $(PWD)/testset

.PHONY: build run run-dev stop status stop clean rmi rmi-all train terminal

all:
	@make build

$(WEB_FACE_RECOGNITION_DOCKERFILE) : $(BASE_FACE_RECOGNITION_DOCKERFILE)

%.yml: $(WEB_FACE_RECOGNITION_DOCKERFILE)

# Base image building
define build_image
	docker build -f $(1) $(DOCKER_BUILD_FLAGS) -t $(2) $(3)
endef

build: $(WEB_FACE_RECOGNITION_DOCKERFILE) $(BASE_FACE_RECOGNITION_DOCKERFILE) src modelset
	@$(call build_image,$(BASE_FACE_RECOGNITION_DOCKERFILE),$(BASE_FACE_RECOGNITION_IMAGE),$(BASE_FACE_RECOGNITION_DIR))
	@$(call build_image,$(WEB_FACE_RECOGNITION_DOCKERFILE),$(WEB_FACE_RECOGNITION_IMAGE),$(WEB_FACE_RECOGNITION_DIR))

# Run production environment
run: production.yml modelset/*.clf
	@export ENV_APP=release;\
	docker-compose -f $< up -d

# Run  development environment
run-dev: docker-compose.yml modelset dataset
	@export ENV_APP=devel;\
	docker-compose -f $< up -d

# Stop containers
stop: docker-compose.yml
	@docker-compose stop

# Get running containers status
status: docker-compose.yml
	@docker-compose ps

# Remove the containers
clean: docker-compose.yml
	@docker-compose down

# Remove web face base image only
rmi:
	@docker rmi $(WEB_FACE_RECOGNITION_IMAGE)

# Remove base face base image too
rmi-all: rmi
	@docker rmi $(BASE_FACE_RECOGNITION_IMAGE)

# Train the face recognition model
train:
	@docker-compose exec web python3 training.py

# Enter the terminal
terminal:
	@docker-compose exec web bash

standard-dataset: standard.sh
	@for i in $(DATASETDIR)/* ; do \
		bash standard.sh "$$i" ;\
	done

standard-testset: standard.sh
	@for i in $(TESTSET)/* ; do \
		bash standard.sh "$$i" ;\
	done
