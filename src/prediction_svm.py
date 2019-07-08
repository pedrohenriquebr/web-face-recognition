import math
from sklearn import svm
import os
from os import environ
import os.path
import pickle
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import sys

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def predict(X_img_path, svm_clf=None, model_path=None, model='hog'):
    """
    Recognizes faces in given image using a trained KNN classifier

    :param X_img_path: path to image to be recognized
    :param svm_clf: (optional) a svm classifier object. if not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled svm classifier. if not specified, model_save_path must be svm_clf.
    :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
               of mis-classifying an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
            For faces of unrecognized persons, the name 'unknown' will be returned.
    """
    if not os.path.isfile(X_img_path):
        raise Exception("Invalid image path: {}".format(X_img_path))

    if svm_clf is None and model_path is None:
        raise Exception(
            "Must supply svm classifier either thourgh svm_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if svm_clf is None:
        with open(model_path, 'rb') as f:
            svm_clf = pickle.load(f)

    # Load image file and find face locations
    X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(X_img, model=model)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(
        X_img, known_face_locations=X_face_locations)

    # Predict classes and remove classifications that aren't within the threshold
    result = []
    result = [(pred, loc) for pred, loc  in zip(
        svm_clf.predict(faces_encodings), X_face_locations)]

    return result

def predict_frame(X_img, svm_clf=None, model_path=None, model='hog'):
    """
    Recognizes faces in given image using a trained KNN classifier

    :param X_img: Numpy array image
    :param svm_clf: (optional) a svm classifier object. if not specified, model_save_path must be specified.
    :param model_path: (optional) path to a pickled svm classifier. if not specified, model_save_path must be svm_clf.
    :param distance_threshold: (optional) distance threshold for face classification. the larger it is, the more chance
               of mis-classifying an unknown person as a known one.
    :return: a list of names and face locations for the recognized faces in the image: [(name, bounding box), ...].
            For faces of unrecognized persons, the name 'unknown' will be returned.
    """

    if svm_clf is None and model_path is None:
        raise Exception(
            "Must supply svm classifier either thourgh svm_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if svm_clf is None:
        with open(model_path, 'rb') as f:
            svm_clf = pickle.load(f)

    X_face_locations = face_recognition.face_locations(X_img, model=model)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(
        X_img, known_face_locations=X_face_locations)

    # Predict classes and remove classifications that aren't within the threshold
    result = []
    result = [(pred, loc) for pred, loc  in zip(
        svm_clf.predict(faces_encodings), X_face_locations)]

    return result


if __name__=='__main__':
	import settings
	if len(sys.argv) != 2:
		print('prediction_svm.py <img_path>')
		exit(1)
	img_path = sys.argv[1]
	model_path = os.path.join(os.getenv('MODELSET_DIR'),os.getenv('SVM_MODEL'))
	X_img = face_recognition.load_image_file(img_path)

	print(predict_frame(X_img = X_img ,model_path=model_path))