import os

import face_recognition
import prediction
import settings
import training
from flask import Flask, jsonify, redirect, render_template, request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/recognition',methods=['POST'])
def face_recognition_api():
	# por enquanto somente KNN
	if request.method == 'POST':
		if 'file' not in request.files:
			return redirect(request.url)
		
		file = request.files['file']
		model = request.values['model']  # por padrão será o Hog

		if model == None:
			model = os.getenv('FACE_DETECTION_MODEL','hog')
		
		if file.filename == '':
			return redirect(request.url)

		if file and allowed_file(file.filename):
			# The image file seems valid! Detect faces and return the result.
			return detect_faces_in_image(file,model=model)
	


@app.route('/', methods=['GET', 'POST'])
def upload_image():
	# Check if a valid image file was uploaded
	if request.method == 'POST':
		if 'file' not in request.files:
			return redirect(request.url)

		file = request.files['file']

		if file.filename == '':
			return redirect(request.url)

		if file and allowed_file(file.filename):
			# The image file seems valid! Detect faces and return the result.
			FACE_DETECTION_MODEL = os.getenv('FACE_DETECTION_MODEL','hog')
			app.logger.debug('FACE_DETECTION_MODEL: {}'.format(FACE_DETECTION_MODEL))
			return detect_faces_in_image(file,model=FACE_DETECTION_MODEL)
	
	return render_template('index.html')


def detect_faces_in_image(file_stream,model='hog'):
	MODELSET_DIR = os.getenv('MODELSET_DIR')
	KNN_MODEL  = os.getenv('KNN_MODEL')

	app.logger.debug('MODELSET_DIR: {}'.format(MODELSET_DIR))
	app.logger.debug('KNN_MODEL: {}'.format(KNN_MODEL))

	img  = face_recognition.load_image_file(file_stream)
	classifier_model = os.path.join(MODELSET_DIR, KNN_MODEL)
		
	result = prediction.predict_frame(img,model_path=classifier_model,model=model)
	return jsonify(result)		   


	
if __name__ == "__main__":
	app.run(debug=True,port=5000,host='0.0.0.0')
