import os
from flask import Flask
from flask_restful import Api
from src.services.model_service import run_recognition_model
from src.database.db import initialize_db
from src.routes import initialize_routes
from src.infra.gc_storage.gcloud_storage import initialize_firebase_storage
from dotenv import load_dotenv
from flask_apscheduler import APScheduler

load_dotenv()

app = Flask(__name__)
api = Api(app)
print(os.environ.get("MONGODB_URI"))
app.config["MONGODB_SETTINGS"] = {"host": os.environ.get("MONGODB_URI")}

initialize_db(app)
initialize_routes(api)
initialize_firebase_storage()

# initialize scheduler
scheduler = APScheduler()
# if you don't wanna use a config, you can set options here:
# scheduler.api_enabled = True
scheduler.init_app(app)

@scheduler.task('cron', id='run_model', minute='*')
def run_model():
    run_recognition_model()
    print('run_model executed')

scheduler.start()

if __name__ == "__main__":
    app.run()
