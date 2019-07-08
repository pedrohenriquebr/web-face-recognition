# -*- encoding: utf-8 -*-
import settings
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import math
from sklearn import neighbors
import os.path
import pickle
import sys
import pandas as pd



ENV_APP = os.getenv('ENV_APP')
DATASET_DIR = os.getenv('DATASET_DIR')
FACE_DETECTION_MODEL = os.getenv('FACE_DETECTION_MODEL', 'hog')
N_NEIGHBORS = os.getenv('N_NEIGHBORS')
MODELSET_DIR = os.getenv('MODELSET_DIR')
KNN_MODEL = os.getenv('KNN_MODEL')

def train(train_dir, model_save_path=None, n_neighbors=None, knn_algo='ball_tree', verbose=False, model='hog'):
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

	base = pd.read_csv(os.path.join(train_dir, 'encodings.csv'))
	y = base.iloc[:, 0].values
	X = base.iloc[:, 1:].values

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
	n_neighbors = 'auto'
	model_save_path = ''
	if N_NEIGHBORS != None and N_NEIGHBORS != 'auto':
		# tento converter para inteiro
		try:
			n_neighbors = int(N_NEIGHBORS)
		except:
			n_neighbors = 1
	model_save_path = os.path.join(MODELSET_DIR, KNN_MODEL)
	print("Starting training...")
	train(DATASET_DIR, model_save_path=model_save_path,
		  n_neighbors=n_neighbors,
		  verbose=True,
		  model=FACE_DETECTION_MODEL)
	print("Training finished!")


if __name__ == "__main__":
	main(sys.argv)
