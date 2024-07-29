from pymongo import MongoClient
from auth import CONNECTION_STRING

def getDatabase(name):
    client = MongoClient(CONNECTION_STRING)
    return client[name]
