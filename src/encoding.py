# -*- encoding: utf-8 -*-
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import os.path
import sys
import numpy as np

import settings
import os
import pandas as pd
from cachesystem import CacheSystem


def encoding(dataset_dir, encoding_file='encodings.csv', verbose=False, model='hog'):
    X = []
    y = []

    # Loop through each person in the training set
    for class_dir in os.listdir(dataset_dir):
        if not os.path.isdir(os.path.join(dataset_dir, class_dir)) or class_dir in ['__cache__']:
            continue
        cache = CacheSystem(
            dataset_dir, cache_dir=os.path.join('__cache__', class_dir))

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(dataset_dir, class_dir)):
            print('Found image: %s' % (img_path), end='')
            image = face_recognition.load_image_file(img_path)

            face_bounding_boxes = face_recognition.face_locations(
                image, model=model)
            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(
                        face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the training set
                """ is_cached, encodings = make_cache(img_path,class_dir,model) """
                is_cached, encodings = cache.check(img_path, model=model)
                X.append(encodings)
                y.append(class_dir)

                print('=> cached: %s' % (is_cached))

    # save to encodings.csv
    save_encodings_csv(os.path.join(dataset_dir, encoding_file), X, y)


def encoding_nolabels(dataset_dir, encoding_file='encodings.csv', verbose=False, model='hog'):
    X = []
    labels = []
    cache = CacheSystem(dataset_dir, cache_dir='__cache__')

    # Loop through each training image for the current person
    for img_path in image_files_in_folder(os.path.join(dataset_dir)):
        print('Found image: %s' % (img_path), end='')
        image = face_recognition.load_image_file(img_path)

        face_bounding_boxes = face_recognition.face_locations(
            image, model=model)
        if len(face_bounding_boxes) != 1:
             # If there are no people (or too many people) in a training image, skip the image.
            if verbose:
                print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(
                    face_bounding_boxes) < 1 else "Found more than one face"))
        else:
            is_cached, encodings = cache.check(img_path, model=model)
            X.append(encodings)
            labels.append(img_path.split('/')[-1])
            print('=> cached: %s' % (is_cached))
    # save to encodings.csv
    save_encodings_csv(os.path.join(
        dataset_dir, encoding_file), X, labels=labels)


def save_encodings_csv(dest_path, encodings, labels=None):
    X = encodings
    y = labels

    if labels == None:
        with open(dest_path, 'wt') as f:
            for encoding in X:
                f.write(str(encoding[0]))
                for i in range(1, 128):
                    f.write(',')
                    f.write(str(encoding[i]))
                f.write('\n')

        return

    with open(dest_path, 'wt') as f:
        for name, encoding in zip(y, X):
            f.write(name)
            for i in range(128):
                f.write(',')
                f.write(str(encoding[i]))

            f.write('\n')


def load_encodings_csv(path, filename='encodings.csv', labels=True):
    X = []
    y = []
    base = pd.read_csv(os.path.join(path, filename), header=None)
    if labels:
        y = base.iloc[:, 0].values
        X = base.iloc[:, 1:].values

        return X, y

    X = base.iloc[:].values
    return X


def main(argv):
    dataset = os.getenv('DATASET_DIR')
    model = os.getenv('FACE_DETECTION_MODEL')

    if len(sys.argv) == 2:
        option = sys.argv[1]
        if option == 'raw':
            dataset = os.getenv('DATASET_RAW_DIR')
            encoding_nolabels(dataset, verbose=True, model=model)
        elif option == 'clusters':
            dataset = os.getenv('DATASET_CLUSTERS_DIR')
            encoding(dataset, verbose=True, model=model)
        elif option == 'normal':
            encoding(dataset, verbose=True, model=model)
        else:
            print('invalid option!')
            exit(1)
    else:
        encoding(dataset, verbose=True, model=model)


if __name__ == "__main__":
    main(sys.argv)
