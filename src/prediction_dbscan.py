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
import shutil

MODELSET_DIR = os.getenv('MODELSET_DIR')
DATASET_RAW_DIR = os.getenv('DATASET_RAW_DIR')
DATASET_CLUSTERS_DIR = os.getenv('DATASET_CLUSTERS_DIR')
DATASET_DIR = os.getenv('DATASET_DIR')


model_path = os.path.join(MODELSET_DIR, 'trained_dbscan_model.clf')
dbscan = None
with open(model_path, 'rb') as f:
    dbscan = pickle.load(f)

dt = pd.read_csv(os.path.join(DATASET_RAW_DIR, 'labels.csv'), header=None)
dt2 = pd.read_csv(os.path.join(DATASET_CLUSTERS_DIR,
                               'clusters.csv'), header=None)

names_np = []
for index in range(len(dt)):
    filename_dest = dt.iloc[index, 0]
    name_dest = dt.iloc[index, 1]

    list_ = dt2.where(dt2[1] == filename_dest).dropna(thresh=2).values
    names_np.insert(0, [int(list_[0, 0]), name_dest])
    print('found: {},{}'.format(int(list_[0, 0]), name_dest))

print(DATASET_DIR)
with open(os.path.join(DATASET_CLUSTERS_DIR, 'names.csv'), 'wt') as f:
    for label, name in names_np:
        f.write('{},{}\n'.format(label, name))
        shutil.rmtree(os.path.join(DATASET_DIR, str(name)), True)
        shutil.copytree(os.path.join(DATASET_CLUSTERS_DIR, str(label)),
                        os.path.join(DATASET_DIR, str(name)))
