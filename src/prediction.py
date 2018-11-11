
import math
from sklearn import neighbors
import os
from os import environ
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import sys

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def predict_frame(X_img_frame, knn_clf=None, model_path=None, distance_threshold=0.6,model='hog'):
	"""
	Recognizes faces in given image using a trained KNN classifier

	:param X_img_frame: path to image to be recognized
	:param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
	:param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
	:param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
		   of mis-classifying an unknown person as a known one.
	:return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
		For faces of unrecognized persons, the name 'unknown' will be returned.
	"""

	#if not os.path.isfile(X_img_frame) or os.path.splitext(X_img_frame)[1][1:] not in ALLOWED_EXTENSIONS:
	#    raise Exception("Invalid image path: {}".format(X_img_frame))

	if knn_clf is None and model_path is None:
		raise Exception(
			"Must supply knn classifier either thourgh knn_clf or model_path")

	# Load a trained KNN model (if one was passed in)
	if knn_clf is None:
		with open(model_path, 'rb') as f:
			knn_clf = pickle.load(f)

	# Load image file and find face locations
	X_face_locations = face_recognition.face_locations(X_img_frame,model)

	THRESHOLD=os.getenv('THRESHOLD')
	
	# If no faces are found in the image, return an empty result.
	if len(X_face_locations) == 0:
		return []

	# Find encodings for faces in the test iamge
	faces_encodings = face_recognition.face_encodings(
		X_img_frame, known_face_locations=X_face_locations)

	# Use the KNN model to find the best matches for the test face
	closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)

	if THRESHOLD:
		are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
	else:
		are_matches = [closest_distances[0][i][0] for i in range(len(X_face_locations))]

	# Predict classes and remove classifications that aren't within the threshold
	result = []
	if THRESHOLD:
		result  = [(pred, loc) if rec else (os.environ.get('UNKNOWN_LABLE','unkown'), loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]
	else:
		result  = [(pred, loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

	return result


def predict(X_img_path, knn_clf=None, model_path=None, distance_threshold=0.6,model='hog'):
	"""
	Recognizes faces in given image using a trained KNN classifier

	:param X_img_path: path to image to be recognized
	:param knn_clf: (optional) a knn classifier object. if not specified, model_save_path must be specified.
	:param model_path: (optional) path to a pickled knn classifier. if not specified, model_save_path must be knn_clf.
	:param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
		   of mis-classifying an unknown person as a known one.
	:return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
		For faces of unrecognized persons, the name 'unknown' will be returned.
	"""
	if not os.path.isfile(X_img_path):
		raise Exception("Invalid image path: {}".format(X_img_path))

	if knn_clf is None and model_path is None:
		raise Exception(
			"Must supply knn classifier either thourgh knn_clf or model_path")

	# Load a trained KNN model (if one was passed in)
	if knn_clf is None:
		with open(model_path, 'rb') as f:
			knn_clf = pickle.load(f)

	# Load image file and find face locations
	X_img = face_recognition.load_image_file(X_img_path)
	X_face_locations = face_recognition.face_locations(X_img,model)

	# If no faces are found in the image, return an empty result.
	if len(X_face_locations) == 0:
		return []

	# Find encodings for faces in the test iamge
	faces_encodings = face_recognition.face_encodings(
		X_img, known_face_locations=X_face_locations)

	# Use the KNN model to find the best matches for the test face
	closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)

	if THRESHOLD:
		are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
	else:
		are_matches = [closest_distances[0][i][0] for i in range(len(X_face_locations))]

	# Predict classes and remove classifications that aren't within the threshold
	result = []
	if THRESHOLD:
		result  = [(pred, loc) if rec else (os.environ.get('UNKNOWN_LABLE','unkown'), loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]
	else:
		result  = [(pred, loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]

	return result