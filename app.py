import config.db as mongo
from flask import Flask

app = Flask(__name__)

@app.route('/test')
def test():
    mongo.db.collection.insert_one({"name": "John"})
    return "Connected to the data base!"

