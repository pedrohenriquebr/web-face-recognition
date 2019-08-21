WEB_FACE_RECOGNITION_DIR=$(PWD)
WEB_FACE_RECOGNITION_DOCKERFILE=$(WEB_FACE_RECOGNITION_DIR)/Dockerfile
WEB_FACE_RECOGNITION_IMAGE=web_face_recognition

DOCKER_BUILD_FLAGS=--rm

DATASETDIR := $(PWD)/dataset
TESTSETDIR := $(PWD)/testset
MODELSETDIR := $(PWD)/modelset
BACKUP_FILENAME := backup-$(shell date +"%Y-%m-%d").zip
TMPDIR := $${TMPDIR:-/dev/shm/web_face_recognition}

.PHONY: build run run-dev stop status stop clean rmi rmi-all train terminal

# All production environment tasks
all:
	@make build
	@make run
	@make encoding
	@make train

# SVM training 
all-svm:
	@make build
	@make run
	@make encoding
	@make train-svm
	
# All development environment tasks
all-dev:
	@make build
	@make run-dev
	@make encoding
	@make train

# SVM training in development environment
all-svm-dev:
	@make build
	@make run-dev
	@make encoding
	@make train-svm
	
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

# Development cycle
restart: clean build 

# Run  development environment
run-dev: docker-compose.yml $(MODELSETDIR) 
	@echo "Running in development mode..."
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
	@mkdir -p $(TMPDIR) ;\
	cp -r $(DATASETDIR) $(MODELSETDIR) $(TESTSETDIR) $(TMPDIR) ;\
	cd $(TMPDIR) ;\
	zip -r $(BACKUP_FILENAME) * ;\
	mv $(BACKUP_FILENAME) $${OLDPWD} ;\
	cd $${OLDPWD};\
	rm -rf $(TMPDIR)

# Remove web face base image only
rmi:
	@docker rmi $(WEB_FACE_RECOGNITION_IMAGE)

# Extract face encodings from $DATASETDIR images and save it in encodings.csv
encoding:
	@echo "Extracting faces encodings..."
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


# standard => encoding-raw => train-dbscan => clustering => encoding-clusters
test-clusters:
	bash standard.sh &&\
	rm -rf ./dataset-clusters/* &&\
	cd src &&\
	python3 encoding.py raw &&\
	python3 training_dbscan.py &&\
	python3 clustering.py &&\
	python3 encoding.py  clusters &&\
	python3 prediction_dbscan.py

encoding-raw: dataset-raw/*.jpeg
	@docker-compose exec web python3 encoding.py raw

train-dbscan: dataset-raw/encodings.csv
	@docker-compose exec web python3 training_dbscan.py

clustering: dataset-clusters/clusters.csv
	@docker-compose exec web python3 clustering.py

encoding-clusters:
	@docker-compose exec web python3 encoding.py clusters

pred-dbscan:
	@docker-compose exec web python3 prediction_dbscan.py