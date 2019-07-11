WEB_FACE_RECOGNITION_DIR=$(PWD)
WEB_FACE_RECOGNITION_DOCKERFILE=$(WEB_FACE_RECOGNITION_DIR)/Dockerfile
WEB_FACE_RECOGNITION_IMAGE=web_face_recognition

DOCKER_BUILD_FLAGS=--rm

DATASETDIR := $(PWD)/dataset
TESTSETDIR := $(PWD)/testset
MODELSETDIR := $(PWD)/modelset
BACKUP_FILENAME := backup-$(shell date +"%Y-%m-%d").zip

.PHONY: build run run-dev stop status stop clean rmi rmi-all train terminal

all:
	@make build

%.yml: $(WEB_FACE_RECOGNITION_DOCKERFILE)

# Base image building
define build_image
	docker build -f $(1) $(DOCKER_BUILD_FLAGS) -t $(2) $(3)
endef

build: $(WEB_FACE_RECOGNITION_DOCKERFILE) src $(MODELSETDIR)
	@$(call build_image,$(WEB_FACE_RECOGNITION_DOCKERFILE),pedrobraga/$(WEB_FACE_RECOGNITION_IMAGE):"$${TAG:-latest}",$(WEB_FACE_RECOGNITION_DIR))

# Run production environment
run: production.yml $(MODELSETDIR)/*.clf
	docker-compose -f $< up --scale web="$${SCALE:-1}" -d

# Run  development environment
run-dev: docker-compose.yml $(MODELSETDIR) 
	docker-compose -f $< up --scale web="$${SCALE:-1}" -d

# Stop containers
stop: docker-compose.yml
	@docker-compose stop

# Get running containers status
status: docker-compose.yml
	@docker-compose ps

# Remove the containers
clean: docker-compose.yml
	@docker-compose down

# Remove files
clean-data:
	@echo 'cleaning..'
	rm -rf $(DATASETDIR)/*
	rm -rf $(TESTSETDIR)/*
	rm -rf $(MODELSETDIR)/*

# Backing up $DATASETDIR, $MODELSETDIR, $TESTSETDIR
backup:
	@mkdir -p tmp ;\
	cp -r $(DATASETDIR) $(MODELSETDIR) $(TESTSETDIR) ./tmp/ ;\
	cd ./tmp ; zip -r $(BACKUP_FILENAME) * ;\
	mv $(BACKUP_FILENAME) .. ;\
	cd ..;\
	rm -rf ./tmp
# Remove web face base image only
rmi:
	@docker rmi $(WEB_FACE_RECOGNITION_IMAGE)

# Extract face encodings from $DATASETDIR images and save it in encodings.csv
encoding:
	@docker-compose exec web python3 encoding.py
	
# Train all the face recognition models
train: $(DATASETDIR)/encodings.csv
	@docker-compose exec web python3 training_svm.py
	@docker-compose exec web python3 training_knn.py

# Train the knn model
train-knn: $(DATASETDIR)/encodings.csv
	@docker-compose exec web python3 training_knn.py

# Train the svm model 
train-svm: $(DATASETDIR)/encodings.csv
	@docker-compose exec web python3 training_svm.py

# Enter the terminal
terminal:
	@docker-compose exec web bash
