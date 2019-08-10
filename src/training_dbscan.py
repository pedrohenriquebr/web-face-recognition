
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import math
import pickle
import sys
import pandas as pd
from sklearn.cluster import DBSCAN

import settings
import os
import os.path
import encoding


MODELSET_DIR = os.getenv('MODELSET_DIR')
DBSCAN_MODEL = os.getenv('DBSCAN_MODEL')
DATASET_DIR = os.getenv('DATASET_RAW_DIR')
DATASET_CLUSTERS = os.getenv('DATASET_CLUSTERS_DIR')
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
    X,y = encoding.load_encodings_csv(train_dir,labels=True)
    # Create and train the KNN classifier
    dbscan = DBSCAN(metric='euclidean')
    dbscan.fit(X)

    # Save the trained KNN classifier
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump(dbscan, f)

    return dbscan



def main(argv):


    model_save_path = os.path.join(MODELSET_DIR, DBSCAN_MODEL)

    print("Starting DBSCAN model training...")
    dbscan = train(DATASET_DIR, model_save_path=model_save_path,
                   verbose=True,
                   model=FACE_DETECTION_MODEL)

    X, labels= encoding.load_encodings_csv(DATASET_DIR, labels=True)
    data = {
        'cluster': list(dbscan.labels_),
        'filename': list(labels)
    }


    dt = pd.DataFrame(data)
    dt.to_csv(os.path.join(DATASET_CLUSTERS, 'clusters.csv'),
              header=None, index=None)
    print("Training finished!")


if __name__ == "__main__":
    main(sys.argv)