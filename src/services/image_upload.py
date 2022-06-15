import os

import werkzeug
from firebase_admin import storage
from flask import request
from flask_restful.reqparse import RequestParser


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

UPLOAD_DIR = os.path.abspath(os.path.dirname(__file__))

def upload_image_service(parser: RequestParser):
    parser.add_argument("file", type=werkzeug.datastructures.FileStorage, location='files')
    args = parser.parse_args()
    file = args.get("file")
    if file is None:
        return {'errorMessage': 'No file part'}, 400

    if file.filename == '':
        return {'errorMessage': 'No selected file'}, 400
    if file and allowed_file(file.filename):
        file.save(os.path.join(UPLOAD_DIR, file.filename))
        return upload_image_to_cloud_storage(os.path.join(UPLOAD_DIR, file.filename))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image_to_cloud_storage(image_file):
    fileName = image_file
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    blob.make_public()
    return blob.public_url
