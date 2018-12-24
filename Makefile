BASE_FACE_RECOGNITION_DIR=base_face_recognition
BASE_FACE_RECOGNITION_DOCKERFILE=$(BASE_FACE_RECOGNITION_DIR)/Dockerfile


%.yml : $(BASE_FACE_RECOGNITION_DOCKERFILE)

build: Dockerfile $(BASE_FACE_RECOGNITION_DOCKERFILE)
	mkdir -p modelset
	# Construo os contêineres 
	# Isso aqui demora hein... pegue um cafézinho e tenha paciência...
	echo "Construindo imagens bases..."
	cd $(BASE_FACE_RECOGNITION_DIR)
	docker build --rm -t base_face_recognition .
	cd .. 
	docker build --rm -t web_face_recognition  .
	echo "Imagens bases construídas com sucesso!"

clean: *.yml
	docker-compose -f docker-compose.dev.yml down
	docker-compose -f docker-compose.yml down
	docker-compose -f docker-compose.yml rm -sf
	docker-compose -f docker-compose.dev.yml rm -sf

run: docker-compose.yml
	docker-compose -f docker-compose.yml up -d

run_dev: docker-compose.dev.yml
	docker-compose -f docker-compose.dev.yml up -d --build