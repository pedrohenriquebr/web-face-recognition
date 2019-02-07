from dotenv import load_dotenv
import os

all_keys = os.environ.keys()

# The default values
if not 'DATASET_DIR' in all_keys: 
    os.environ['DATASET_DIR']='/dataset'

if not 'MODELSET_DIR' in all_keys:
    os.environ['MODELSET_DIR']='/modelset'

if not 'KNN_MODEL' in all_keys:
    os.environ['KNN_MODEL']='trained_knn_model.clf'

if not 'N_NEIGHBORS' in all_keys:
    os.environ['N_NEIGHBORS']=''

if not 'FACE_DETECTION_MODEL' in all_keys:
    os.environ['FACE_DETECTION_MODEL']='hog'

if not 'UNKNOWN_LABEL' in all_keys:
    os.environ['UNKNOWN_LABEL']='unknown'

if not 'THRESHOLD' in all_keys:
    os.environ['THRESHOLD']='FALSE'

# The .env file should override environment variables
load_dotenv()