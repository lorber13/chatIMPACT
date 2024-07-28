from pymongo import MongoClient
from auth import CONNECTION_STRING

def getDatabase():
    client = MongoClient(CONNECTION_STRING)
    return client['Paper']

db = getDatabase()

