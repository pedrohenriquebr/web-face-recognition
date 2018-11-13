from flask import Flask, jsonify, request, redirect, render_template
from werkzeug.utils import secure_filename
import training 
import prediction
import face_recognition
import os
import settings



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
			return detect_faces_in_image(file,model=os.getenv('FACE_DETECTION_MODEL','hog'))

	return render_template('index.html')


def detect_faces_in_image(file_stream,model='hog'):
	img  = face_recognition.load_image_file(file_stream)
	classifier_model = os.path.join(os.getenv('MODELSET_DIR'), os.getenv('KNN_MODEL'))
		
	result = prediction.predict_frame(img,model_path=classifier_model,model='cnn')
	return jsonify(result)		   


	
if __name__ == "__main__":
	app.run(debug=True,port=5000,host='0.0.0.0')