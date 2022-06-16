import os

import werkzeug
from firebase_admin import storage
from flask import request
from flask_restful.reqparse import RequestParser
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}


def upload_image_service(parser: RequestParser, id: str) -> str:
    parser.add_argument(
        "file", type=werkzeug.datastructures.FileStorage, location="files"
    )
    args = parser.parse_args()
    file = args.get("file")
    if file is None or file.filename == "":
        return

    if file and allowed_file(file.filename):
        file.filename = id + "." + file.filename.rsplit(".", 1)[1].lower()
        upload_result = upload_image_to_cloud_storage(file)
        return upload_result


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_image_to_cloud_storage(file):
    bucket = storage.bucket()
    # file is just an object from request.files e.g. file = request.files['myFile']
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)
    blob.make_public()
    return blob.public_url
