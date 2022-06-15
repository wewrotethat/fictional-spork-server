import os

from firebase_admin import credentials, initialize_app


def initialize_firebase_storage():
    currentDir = os.path.abspath(os.path.dirname(__file__))
    cred = credentials.Certificate(os.path.join(currentDir, "fs-service-acc.json"))
    initialize_app(cred, {'storageBucket': 'fictional-spork-server.appspot.com'})
