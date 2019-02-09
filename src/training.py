# -*- encoding: utf-8 -*-
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import math
from sklearn import neighbors
import os.path
import pickle
import sys

ENV_APP = os.getenv('ENV_APP')

def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False,model='hog'):
	"""
	Trains a k-nearest neighbors classifier for face recognition.

	:param train_dir: directory that contains a sub-directory for each known person, with its name.

	 (View in source code to see train_dir example tree structure)

	 Structure:
		<train_dir>/
		├── <person1>/
		│   ├── <somename1>.jpeg
		│   ├── <somename2>.jpeg
		│   ├── ...
		├── <person2>/
		│   ├── <somename1>.jpeg
		│   └── <somename2>.jpeg
		└── ...

	:param model_save_path: (optional) path to save model on disk
	:param n_neighbors: (optional) number of neighbors to weigh in classification. Chosen automatically if not specified
	:param knn_algo: (optional) underlying data structure to support knn.default is ball_tree
	:param verbose: verbosity of training
	:return: returns knn classifier that was trained on the given data.
	"""
	X = []
	y = []

	# Loop through each person in the training set
	for class_dir in os.listdir(train_dir):
		if not os.path.isdir(os.path.join(train_dir, class_dir)):
			continue

		# Loop through each training image for the current person
		for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
			print('Found image: %s'%(img_path))
			image = face_recognition.load_image_file(img_path)
			face_bounding_boxes = face_recognition.face_locations(image,model=model)

			if len(face_bounding_boxes) != 1:
				# If there are no people (or too many people) in a training image, skip the image.
				if verbose:
					print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(
						face_bounding_boxes) < 1 else "Found more than one face"))
			else:
				# Add face encoding for current image to the training set
				X.append(face_recognition.face_encodings(
					image, known_face_locations=face_bounding_boxes)[0])
				y.append(class_dir)

	# Determine how many neighbors to use for weighting in the KNN classifier
	if n_neighbors is None or n_neighbors == 'auto':
		n_neighbors = int(round(math.sqrt(len(X))))
		if verbose:
			print("Chose n_neighbors automatically:", n_neighbors)

	# Create and train the KNN classifier
	knn_clf = neighbors.KNeighborsClassifier(
		n_neighbors=n_neighbors, algorithm=knn_algo, weights='distance')
	knn_clf.fit(X, y)

	# Save the trained KNN classifier
	if model_save_path is not None:
		with open(model_save_path, 'wb') as f:
			pickle.dump(knn_clf, f)

	return knn_clf
	
def main(argv):
	DATASET_DIR = os.getenv('DATASET_DIR')
	FACE_DETECTION_MODEL = os.getenv('FACE_DETECTION_MODEL','hog')
	N_NEIGHBORS = os.getenv('N_NEIGHBORS')

	model_save_path = ''

	persons = len(os.listdir(DATASET_DIR))
	if persons <= 1:
		print("Insufficient people")
		print("Found only {} persons ".format(persons))
		exit()

	if N_NEIGHBORS != None and N_NEIGHBORS != 'auto':
	# tento converter para inteiro
		try:
			N_NEIGHBORS = int(N_NEIGHBORS)
		except:
			N_NEIGHBORS = 1
	model_save_path = os.path.join(os.getenv('MODELSET_DIR'), os.getenv('KNN_MODEL'))
	
	print("Starting training...")
	train(DATASET_DIR, model_save_path=model_save_path, n_neighbors=N_NEIGHBORS,verbose=(ENV_APP == 'devel'),model=FACE_DETECTION_MODEL)
	print("Training finished!")

if __name__ == "__main__":
	if ENV_APP == "devel":
		main(sys.argv)
	else:
		print("Not allowed!")
	