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
        "collection1": {
            "attribute1": "examplevalue",
            "attribute2": 3,
        },
        "collection2": {
            "attribute1": [
                "value1",
                "value2",
            ],
        },
    },
    {
        "collection1": {
            "attribute1": "examplevalue2",
            "attribute2": 5,
        },
        "collection2": {
            "attribute1": [
                "value3",
                "value4",
            ],
        },
    }
]
"""

def query(database, specifications):
    if specifications and len(specifications) == 1:
        specification = specifications[0]
        collection = database[specification["collection"]]
        if "project" in specification:
            if "filters" in specification:
                items = list(collection.find(filter = specification["filters"], projection = specification["project"]))
            else:
                items = list(collection.find(projection = specification["project"]))
        else:
            if "filters" in specification:
                items = list(collection.find(filter = specification["filters"]))
            else:
                items = list(collection.find())
        for item in items:
            del item["_id"]
        return items
    else:
        return []
