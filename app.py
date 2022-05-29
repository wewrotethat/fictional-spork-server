import os
from flask import Flask
from flask_restful import Api
from src.database.db import initialize_db
from src.routes import initialize_routes
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
api = Api(app)
print(os.environ.get("MONGODB_URI"))
app.config["MONGODB_SETTINGS"] = {"host": os.environ.get("MONGODB_URI")}

initialize_db(app)
initialize_routes(api)

if __name__ == "__main__":
    app.run()
