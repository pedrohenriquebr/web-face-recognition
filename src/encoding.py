# -*- encoding: utf-8 -*-
import os
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import os.path
import sys
import numpy as np
import settings

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
			print('Found image: %s'%(img_path))
			image = face_recognition.load_image_file(img_path)

			face_bounding_boxes = face_recognition.face_locations(image,model=model)
			if len(face_bounding_boxes) != 1:
				# If there are no people (or too many people) in a training image, skip the image.
				if verbose:
					print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(
						face_bounding_boxes) < 1 else "Found more than one face"))
			else:
				# Add face encoding for current image to the training set
				X.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
				y.append(class_dir)

	with open(os.path.join(dataset_dir,encoding_file),'wt') as f:
		for name,encoding in zip(y,X):
			f.write(name)

			for i in range(128):
				f.write(',')
				f.write(str(encoding[i]))

			f.write('\n')
		

	
def main(argv):
	DATASET_DIR = os.getenv('DATASET_DIR')

	encoding(DATASET_DIR, verbose=True,model='cnn')

if __name__ == "__main__":
	main(sys.argv)
	