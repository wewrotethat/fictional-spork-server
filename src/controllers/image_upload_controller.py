from flask import Response,request
from flask_restful import Resource, output_json
from firebase_admin import credentials, initialize_app, storage
from werkzeug.utils import secure_filename
import os
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(image_file):
    currentDir = os.path.abspath(os.path.dirname( __file__))
    cred = credentials.Certificate(os.path.join(currentDir, "fs-service-acc.json"))
    initialize_app(cred, {'storageBucket': 'fictional-spork-server.appspot.com'})

    # Put your local file path
    fileName = image_file
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

    blob.make_public()

    print("your file url", blob.public_url)

class ImageUploadController(Resource):
    def post(self):
        # check if the post request has the file part
        if 'file' not in request.files:
           return {'errorMessage': 'No file part'}, 400
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return {'errorMessage': 'No selected file'}, 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_image(image_file=filename)
        # TODO: save save test entry id and image url to database
        print("uploaded")
        pass


