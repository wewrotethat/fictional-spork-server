from flask import current_app,g
from flask_pymongo import pymongo

# TODO: can be moved to config file
CONNECTION_STRING = "mongodb+srv://malaria_watch:tnItUo46YB3Z1mqM@cluster0.go4nn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

def connect_to_mongo_db():
    client = pymongo.MongoClient(
            # current_app.config['DATABASE']
            CONNECTION_STRING
            )
    g.db = client.get_database('malaria_watch')
    print("connected to db")


def get_db():
    return g.db



