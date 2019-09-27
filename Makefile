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
	@make standard
	@make encoding
	@make train
	@make run

# SVM training 
all-svm:
	@make standard
	@make encoding
	@make train-svm
	@make run

# All development environment tasks
all-dev:
	@make standard
	@make encoding
	@make train
	@make run-dev

# SVM training in development environment
all-svm-dev:
	@make standard
	@make encoding
	@make train-svm
	@make run-dev

# Run production environment
run:  $(MODELSETDIR)/*.clf
	@python3 src/app.py

# Run  development environment
run-dev: $(MODELSETDIR) 
	@echo "Running in development mode..."
	@python3 src/app.py

# Remove files
clean-data:
	@echo 'cleaning..'
	rm -rf $(DATASETDIR)/*
	rm -rf $(TESTSETDIR)/*
	rm -rf $(MODELSETDIR)/*

# Backing up $DATASETDIR, $MODELSETDIR, $TESTSETDIR
backup:
	@mkdir -p $(TMPDIR) ;\
	cp -r dataset-raw $(DATASETDIR) $(MODELSETDIR) $(TESTSETDIR) $(TMPDIR) ;\
	cd $(TMPDIR) ;\
	zip -r $(BACKUP_FILENAME) * ;\
	mv $(BACKUP_FILENAME) $${OLDPWD} ;\
	cd $${OLDPWD};\
	rm -rf $(TMPDIR)

# Extract face encodings from $DATASETDIR images and save it in encodings.csv
encoding:
	@echo "Extracting faces encodings..."
	@python3 src/encoding.py
	
# Train all the face recognition models
train: $(DATASETDIR)/encodings.csv
	@python3 src/training_svm.py
	@python3 src/training_knn.py

# Train the knn model
train-knn: $(DATASETDIR)/encodings.csv
	@python3 src/training_knn.py

# Train the svm model 
train-svm: $(DATASETDIR)/encodings.csv
	@python3 src/training_svm.py

# standard => encoding-raw => train-dbscan => clustering => encoding-clusters

standard:
	@bash standard.sh

clean-clusters:
	@rm -rf ./dataset-clusters/*

encoding-raw: dataset-raw/*.jpeg
	@python3 src/encoding.py raw

train-dbscan: dataset-raw/encodings.csv
	@python3 src/training_dbscan.py

clustering: dataset-clusters/clusters.csv
	@python3 src/clustering.py

encoding-clusters:
	@python3 src/encoding.py clusters

test-clusters:
	@make standard encoding-raw clean-clusters train-dbscan clustering encoding-clusters

pred-dbscan:
	@python3 src/prediction_dbscan.py