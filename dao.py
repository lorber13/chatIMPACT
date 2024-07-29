from database import db

"""
query = [
    {
        "collection": "Models",
        "project": [
            "name",
            "openSource"
        ],
        "filters": {
            "name": "ll",
            "openSource": True
        }
    },
    {
        "collection", "Downstream Tasks",
        "project": [
            "name",
        ],
        "filters": {
            "name": "RO"
        }
    }
]
"""

"""
result = [
    {
        "collection1.attribute1": "examplevalue",
        "collection1.attribute2": 3,
        "collection2.attribute1": ["value1", "value2"]
    },
    {
        "collection1.attribute1": "examplevalue2",
        "collection1.attribute2": 5,
        "collection2.attribute1": ["value3", "value4"]
    }
]
"""

def query(specification):
    pass

