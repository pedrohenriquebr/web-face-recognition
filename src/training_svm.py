# -*- encoding: utf-8 -*-
import settings
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import math
import os.path
import pickle
import sys
import pandas as pd
from sklearn import svm

MODELSET_DIR = os.getenv('MODELSET_DIR')
SVM_MODEL = os.getenv('SVM_MODEL')
DATASET_DIR = os.getenv('DATASET_DIR')
FACE_DETECTION_MODEL = os.getenv('FACE_DETECTION_MODEL')
def train(train_dir, model_save_path=None, verbose=False, model='hog'):
    """
    Trains Suppport Vectors Machine classifier for face recognition.

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
    :param verbose: verbosity of training
    :return: returns svm classifier that was trained on the given data.
    """
    X = []
    y = []
    base = pd.read_csv(os.path.join(train_dir, 'encodings.csv'))
    y = base.iloc[:, 0].values
    X = base.iloc[:, 1:].values

    # Create and train the KNN classifier
    svm_clf = svm.SVC(kernel='linear')
    svm_clf.fit(X, y)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(svm_clf, f)

    return svm_clf


def main(argv):

    model_save_path = os.path.join(MODELSET_DIR, SVM_MODEL)

    print("Starting SVM model training...")
    train(DATASET_DIR, model_save_path=model_save_path,
          verbose=True,
          model=FACE_DETECTION_MODEL)
    print("Training finished!")


if __name__ == "__main__":
    main(sys.argv)
