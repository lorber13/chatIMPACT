"""interface to the database object"""

from pymongo import MongoClient
from auth import CONNECTION_STRING


def get_database(name: str):
    """gets the database given the name"""
    client = MongoClient(CONNECTION_STRING)
    return client[name]
