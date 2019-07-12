# -*- encoding: utf-8 -*-
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import os.path
import sys
import numpy as np
import settings
import pandas as pd
ENV_APP = os.getenv('ENV_APP')

def encoding(dataset_dir,encoding_file='encodings.csv', verbose=False,model='hog'):
	X = []
	y = []

	# Loop through each person in the training set
	for class_dir in os.listdir(dataset_dir):
		if not os.path.isdir(os.path.join(dataset_dir, class_dir)):
			continue

		# Loop through each training image for the current person
		for img_path in image_files_in_folder(os.path.join(dataset_dir, class_dir)):
			print('Found image: %s'%(img_path),end='')
			image = face_recognition.load_image_file(img_path)

			face_bounding_boxes = face_recognition.face_locations(image,model=model)
			if len(face_bounding_boxes) != 1:
				# If there are no people (or too many people) in a training image, skip the image.
				if verbose:
					print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(
						face_bounding_boxes) < 1 else "Found more than one face"))
			else:
				# Add face encoding for current image to the training set
				is_cached, encodings = make_cache(img_path,class_dir,model)
				X.append(encodings)
				y.append(class_dir)

				print('=> cached: %s'%(is_cached))

	with open(os.path.join(dataset_dir,encoding_file),'wt') as f:
		for name,encoding in zip(y,X):
			f.write(name)

			for i in range(128):
				f.write(',')
				f.write(str(encoding[i]))

			f.write('\n')

'''
1. I verify the cache dir
2. I verify the sub cache dir for current person
3. Is there any cache file for my current file ? 
	Yes:
		Verify the last modified date in time stamp
		if the time stamp is differente, so I update cache file.
		EXTRACTING FACE ENCODINGS
	No:

		Then, I create cache file, and write the 'name' person  
		followed by the face encodings fields, separetd by commas .
		EXTRACTING FACE ENCODINGS 
'''
def make_cache(path,class_dir='',model='hog'):
	filename = path.split('/')[-1]
	last_dot = len(filename) - 1 - filename[::-1].index('.')
	cache_dir = os.path.join(os.getenv('DATASET_DIR'),'__cache__',class_dir)
	cachename = os.path.join(cache_dir,filename[:last_dot]+'.csv')
	encodings = []
	is_cached = False
	if not os.path.exists(os.path.join(os.getenv('DATASET_DIR'),'__cache__')):
		os.mkdir(os.path.join(os.getenv('DATASET_DIR'),'__cache__'))
		
		
	if not os.path.exists(cache_dir):
		os.mkdir(cache_dir)
	

	# CREATE
	if not os.path.exists(cachename):
		is_cached = False
		cache_file = open(cachename,'w')
		image = face_recognition.load_image_file(path)
		face_bounding_boxes = face_recognition.face_locations(image,model=model)
		encodings = face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0]
		# save face encodings
		cache_file.write(class_dir)
		for i in range(128):
			cache_file.write(',')
			cache_file.write(str(encodings[i]))
		cache_file.close()
	else:
		is_cached = True
		if os.stat(path).st_mtime > os.stat(cachename).st_mtime:
			# Update cache
			cache_file = open(cachename,'w')
			image = face_recognition.load_image_file(path)
			face_bounding_boxes = face_recognition.face_locations(image,model=model)
			encodings = face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0]
			# save face encodings
			cache_file.write(class_dir)
			for i in range(128):
				cache_file.write(',')
				cache_file.write(str(encodings[i]))
			cache_file.close()
			
		else:
			# Load
			base = pd.read_csv(cachename,header=None)

			y = base.iloc[0, 0]
			X = base.iloc[0, 1:].values
			# load face encodings
			encodings = X
	return is_cached,encodings


def main(argv):
	DATASET_DIR = os.getenv('DATASET_DIR')
	encoding(DATASET_DIR, verbose=True,model=os.getenv('FACE_DETECTION_MODEL'))

if __name__ == "__main__":
	main(sys.argv)
	