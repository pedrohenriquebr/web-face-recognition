import os
import face_recognition
from random import random
import pandas as pd


class CacheSystem:

    def __init__(self, parent_dir, cache_dir='__cache__'):
        self.cache_dir = cache_dir
        self.parent_dir = parent_dir

        if not os.path.exists(self.get_full_path_cache_dir()):
            os.makedirs(self.get_full_path_cache_dir())

    def get_full_path_cache_dir(self):
        return os.path.join(self.parent_dir, self.cache_dir)

    def save(self, src_path, dest_file, model='hog'):
        dest_path = os.path.join(self.get_full_path_cache_dir(), dest_file)

        img = face_recognition.load_image_file(src_path)
        face_bounding_boxes = face_recognition.face_locations(img, model=model)
        if len(face_bounding_boxes) != 1:
            msg = "Image {} not suitable for training: {}".format(src_path, "Didn't find a face" if len(
                face_bounding_boxes) < 1 else "Found more than one face")

            raise Exception(msg)

        encodings = face_recognition.face_encodings(
            img, known_face_locations=face_bounding_boxes)[0]
        


        with open(dest_path, 'w') as f:
            f.write(str(encodings[0]))
            for i in range(1, 128):
                f.write(',')
                f.write(str(encodings[i]))
            f.write('\n')

        return encodings

    def check(self, src_path,model='hog'):
        dest_file = src_path.split('/')[-1]
        last_dot = len(dest_file) - 1 - dest_file[::-1].index('.')
        dest_file = dest_file[:last_dot]+'.csv'

        encodings = []
        is_cached = False
        if not os.path.exists(os.path.join(self.get_full_path_cache_dir(), dest_file)):
            is_cached= False
            encodings = self.save(src_path, dest_file,model=model)

        elif os.stat(src_path).st_mtime > os.stat(os.path.join(self.get_full_path_cache_dir(), dest_file)).st_mtime:
            is_cached = True
            encodings = self.save(src_path, dest_file,model=model)

        else:
            is_cached = True
            encodings = self.load(dest_file)

        return is_cached,encodings

    def load(self, dest_file):
        base = pd.read_csv(os.path.join(
            self.get_full_path_cache_dir(), dest_file), header=None)
        encodings = base.iloc[0].values
        return encodings