"""
query = [
    {
        "collection": "Models",
        "project": [
            "name",
            "openSource"
        ],
        "filters": {
            "name": "ll", "openSource": True
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

class Dao:
    def __init__(self, database) -> None:
        self.database = database

    def query(self, specifications):
        if specifications and len(specifications) == 1:
            return self.__singleCollectionQuery(specifications[0])
        else:
            return self.__singleJoinQuery(specifications)

    def __singleCollectionQuery(self, specification):
        collection = self.database[specification["collection"]]
        results = []
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
            result = {}
            result[collection.name] = item
            results.append(result)
        return results

    def __singleJoinQuery(self, specifications):
        return []

    def __multipleJoinQuery(self, specifications):
        return []
