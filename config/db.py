from flask_pymongo import pymongo
CONNECTION_STRING = "mongodb+srv://malaria_watch:tnItUo46YB3Z1mqM@cluster0.go4nn.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('malaria_watch')
