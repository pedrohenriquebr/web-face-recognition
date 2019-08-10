# -*- encoding: utf-8 -*-
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import os.path
import sys
import numpy as np

import settings
import os
import pandas as pd

DATASET_CLUSTERS_DIR = os.getenv('DATASET_CLUSTERS_DIR')
DATASET_RAW_DIR = os.getenv('DATASET_RAW_DIR')
dataframe = pd.read_csv(os.path.join(DATASET_CLUSTERS_DIR,'clusters.csv'),header=None)

for k in range(len(dataframe)):
    cluster_dir = os.path.join(DATASET_CLUSTERS_DIR,str(dataframe.iloc[k,0]))
    img_file  = os.path.join(DATASET_RAW_DIR,str(dataframe.iloc[k,1]))
    os.system("mkdir -p {} && cp {} {} ".format(cluster_dir,img_file,cluster_dir))