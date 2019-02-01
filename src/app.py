import os

import face_recognition
import prediction
import settings
import training
from flask import Flask, jsonify, redirect, render_template, request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FACE_DETECTION_MODEL = os.getenv('FACE_DETECTION_MODEL','hog')
MODELSET_DIR = os.getenv('MODELSET_DIR')
KNN_MODEL  = os.getenv('KNN_MODEL')
THRESHOLD = os.getenv('THRESHOLD')
ENV_APP = os.getenv('ENV_APP')
HOST_RUN = os.getenv('HOST_RUN','0.0.0.0')

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
		model = FACE_DETECTION_MODEL
		
		if file.filename == '':
			return redirect(request.url)

		if file and allowed_file(file.filename):
			return detect_faces_in_image(file,model=model)
	

if ENV_APP == 'devel':
	@app.route('/', methods=['GET'])
	def index():
		return render_template('index.html')


def detect_faces_in_image(file_stream,model='hog'):

	app.logger.debug('MODELSET_DIR: {}'.format(MODELSET_DIR))
	app.logger.debug('KNN_MODEL: {}'.format(KNN_MODEL))
	app.logger.debug('THRESOLD: {}'.format(THRESHOLD))

	img  = face_recognition.load_image_file(file_stream)
	classifier_model = os.path.join(MODELSET_DIR, KNN_MODEL)
		
	recognition = prediction.predict_frame(img,model_path=classifier_model,model=model)
	#landmarks  = face_recognition.face_landmarks(img)
	#app.logger.debug(' resultado : {}'.format(result))
	#app.logger.debug(' landmarks: {}'.format(landmarks))
	app.logger.debug(' recognition: {}'.format(recognition))
	return jsonify(recognition)		   


	
if __name__ == "__main__":
	app.run(debug=(ENV_APP=='devel'),port=5000,host=HOST_RUN)
