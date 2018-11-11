from flask import Flask, jsonify, request, redirect
from werkzeug.utils import secure_filename
import training 
import prediction
import face_recognition
import os


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/recognition',methods=['POST','GET'])
def face_recognition_api():
	# Check if a valid image file was uploaded
	if request.method == 'POST':
		if 'file' not in request.files:
			return redirect(request.url)

		file = request.files['file']

		if file.filename == '':
			return redirect(request.url)

		if file and allowed_file(file.filename):
			# The image file seems valid! Detect faces and return the result.
			return detect_faces_in_image(file)
	elif request.method == 'GET':
		

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
			return detect_faces_in_image(file)

	# If no valid image file was uploaded, show the file upload form:
	return '''
	<!doctype html>
	<title>Reconhecimento Facial</title>
	<h1>Envie uma imagem para o reconhecimento facial !</h1>
	<form method="POST" enctype="multipart/form-data">
	  <input type="file" name="file">
	  <input type="submit" value="Upload">
	</form>
	'''


def detect_faces_in_image(file_stream):
	img  = face_recognition.load_image_file(file_stream)
	knn_model = os.path.join(os.getenv('MODELSET_DIR'), os.getenv('KNN_MODEL'))
	result = prediction.predict_frame(img,model_path=knn_model)
	return jsonify(result)		   

@app.route("/train/knn")
def train_dataset():
	train_folder = os.getenv('DATASET_DIR')
	knn_model = os.path.join(os.getenv('MODELSET_DIR'), os.getenv('KNN_MODEL'))
	classifier = training.train(train_folder, model_save_path=knn_model, n_neighbors=1,verbose=True)
	return 'Treinamento completo !!'

 
if __name__ == "__main__":
	app.run(debug=True,port=5000,host='0.0.0.0')