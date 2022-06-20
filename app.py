import os
from flask import Flask
from flask_restful import Api
from model_service import getModel
from src.database.db import initialize_db
from src.routes import initialize_routes
from src.infra.gc_storage.gcloud_storage import initialize_firebase_storage
from dotenv import load_dotenv

load_dotenv()

model = getModel()

app = Flask(__name__)
api = Api(app)
print(os.environ.get("MONGODB_URI"))
app.config["MONGODB_SETTINGS"] = {"host": os.environ.get("MONGODB_URI")}

initialize_db(app)
initialize_routes(api)
initialize_firebase_storage()

if __name__ == "__main__":
    app.run()
