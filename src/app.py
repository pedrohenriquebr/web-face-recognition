import os
import signal
from multiprocessing import Process
import face_recognition
import prediction_knn
import prediction_svm

import settings
from flask import Flask, jsonify, redirect, render_template, request
from werkzeug.utils import secure_filename
import socket

print(socket.gethostname())

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
FACE_DETECTION_MODEL = os.getenv('FACE_DETECTION_MODEL', 'hog')
MODELSET_DIR = os.getenv('MODELSET_DIR')
KNN_MODEL = os.getenv('KNN_MODEL')
SVM_MODEL = os.getenv('SVM_MODEL')
THRESHOLD = os.getenv('THRESHOLD')
ENV_APP = os.getenv('ENV_APP')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/recognition/<clf>', methods=['POST'])
def face_recognition_api(clf):
    # por enquanto somente KNN
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']
        model = FACE_DETECTION_MODEL
        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            return detect_faces_in_image(file, model=model, clf=clf)


if ENV_APP == 'devel':
    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')


def detect_faces_in_image(file_stream, model='hog', clf='svm'):

    app.logger.debug('MODELSET_DIR: {}'.format(MODELSET_DIR))
    app.logger.debug('FACE_DETECTION_MODEL: {}'.format(FACE_DETECTION_MODEL))
    img = face_recognition.load_image_file(file_stream)
    recognition = []
    classifier_model = None
    if clf == 'svm':
        app.logger.debug('SVM_MODEL: {}'.format(SVM_MODEL))
        classifier_model = os.path.join(MODELSET_DIR, SVM_MODEL)
        recognition = prediction_svm.predict_frame(
            img, model_path=classifier_model, model=model)

    elif clf == 'knn':
        app.logger.debug('KNN_MODEL: {}'.format(KNN_MODEL))
        app.logger.debug('THRESOLD: {}'.format(THRESHOLD))
        classifier_model = os.path.join(MODELSET_DIR, KNN_MODEL)
        recognition = prediction_knn.predict_frame(
            img, model_path=classifier_model, model=model)

    app.logger.debug(' recognition: {}'.format(recognition))
    return jsonify(recognition)


if __name__ == "__main__":
    def server_handler(signum, frame):
        print('Signal handler called with signal', signum)
        server.terminate()
        server.join()

    signal.signal(signal.SIGTERM, server_handler)

    def run_server():
        app.run(debug=True, port=5000, host="0.0.0.0")

    server = Process(target=run_server)
    server.start()
