import math
from PIL import Image
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

import cv2 as cv

app = Flask(__name__)

app.secret_key = "My-Informatics"

UPLOAD_FOLDER = 'static/uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def main():
    return 'formalinapp_api works !'


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'fileUpload' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('fileUpload')

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'

    if success and errors:

        errors['message'] = 'File(s) successfully uploaded But Something went wrong !'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        img = Image.open(file.stream)
        image = cv.imread(file.stream)
        # (h, w) = image.shape[:2]

        # Machine Learning Code Below
        # ------------------------------------------------
        # Radius = random()

        # -------------------------------------------------------
        resp = jsonify({'message': 'Files successfully uploaded',
                       'size': [img.width, img.height], "Centroid": [h//2, w//2],"Path_img":"/Upload"})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


if __name__ == '__main__':
    app.run(debug=True)
