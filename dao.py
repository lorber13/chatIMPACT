"""interface used to make requests to the database"""

# query = [
#     {
#         "collection": "Models",
#         "project": [
#             "name",
#             "openSource"
#         ],
#         "filters": {
#             "name": "ll", "openSource": True
#         }
#     },
#     {
#         "collection", "Downstream Tasks",
#         "project": [
#             "name",
#         ],
#         "filters": {
#             "name": "RO"
#         }
#     }
# ]
#
# result = [
#     {
#         "collection1": {
#             "attribute1": "examplevalue",
#             "attribute2": 3,
#         },
#         "collection2": {
#             "attribute1": [
#                 "value1",
#                 "value2",
#             ],
#         },
#     },
#     {
#         "collection1": {
#             "attribute1": "examplevalue2",
#             "attribute2": 5,
#         },
#         "collection2": {
#             "attribute1": [
#                 "value3",
#                 "value4",
#             ],
#         },
#     }
# ]


import sys

from pymongo import MongoClient
from auth import CONNECTION_STRING


class Dao:
    """data access object"""

    def __init__(self, name) -> None:
        self.database = MongoClient(CONNECTION_STRING)[name]

    def drop(self, collection_name):
        """drop collection with name"""
        self.database[collection_name].drop()

    def insert_many(self, collection, documents):
        """insert documents into collection"""
        ids = self.database[collection].insert_many(documents)
        return ids

    def query(self, specifications):
        """perform a query"""
        if specifications and len(specifications) == 1:
            return self.__single_collection_query(specifications[0])
        if not specifications:
            return []
        return self.__single_join_query(specifications)

    def __single_collection_query(self, specification):
        collection = self.database[specification["collection"]]
        results = []
        if "project" in specification:
            if "filters" in specification:
                items = list(
                    collection.find(
                        filter=specification["filters"],
                        projection=specification["project"],
                    )
                )
            else:
                items = list(collection.find(projection=specification["project"]))
        else:
            if "filters" in specification:
                items = list(collection.find(filter=specification["filters"]))
            else:
                items = list(collection.find())
        for item in items:
            del item["_id"]
            result = {}
            result[collection.name] = item
            results.append(result)
        return results

    def __construct_match_obj(self, specifications):
        match_obj = {"$match": {}}
        for specification in specifications:
            if "filters" in specification:
                for filt in specification["filters"]:
                    field = f"{specification["collection"]}.{filt}"
                    value = specification["filters"][filt]
                    match_obj["$match"][field] = value
        return match_obj

    def __project_obj(self, specifications):
        project_obj = {"$project": {"_id": False}}
        for specification in specifications:
            if "project" in specification:
                for project in specification["project"]:
                    field = f"{specification["collection"]}.{project}"
                    project_obj["$project"][field] = True
        return project_obj

    def __join_database(self, specifications):
        collections = set()
        for specification in specifications:
            collections.add(specification["collection"])
        if "Models" in collections and "Metrics" in collections:
            join_database = self.database["Evaluate"]
        elif "Models" in collections and "Downstream Tasks" in collections:
            join_database = self.database["Suited For"]
        elif "Models" in collections and "Datasets" in collections:
            join_database = self.database["Train"]
        elif "Datasets" in collections and "Downstream Tasks" in collections:
            join_database = self.database["Enable"]
        elif "Metrics" in collections and "Downstream Tasks" in collections:
            join_database = self.database["Assess"]
        else:
            join_database = None
        return join_database

    def __construct_join_obj(self, specifications):
        collections = set()
        for specification in specifications:
            collections.add(specification["collection"])
        if "Models" in collections and "Metrics" in collections:
            join_obj = [
                {
                    "$lookup": {
                        "from": "Models",
                        "localField": "Models",
                        "foreignField": "_id",
                        "as": "Models",
                    },
                },
                {
                    "$lookup": {
                        "from": "Metrics",
                        "localField": "Metrics",
                        "foreignField": "_id",
                        "as": "Metrics",
                    },
                },
                {"$unwind": {"path": "$Models"}},
                {"$unwind": {"path": "$Metrics"}},
            ]
        elif "Models" in collections and "Downstream Tasks" in collections:
            join_obj = [
                {
                    "$lookup": {
                        "from": "Models",
                        "localField": "Models",
                        "foreignField": "_id",
                        "as": "Models",
                    },
                },
                {
                    "$lookup": {
                        "from": "Downstream Tasks",
                        "localField": "Downstream Tasks",
                        "foreignField": "_id",
                        "as": "Downstream Tasks",
                    },
                },
                {"$unwind": {"path": "$Models"}},
                {"$unwind": {"path": "$Downstream Tasks"}},
            ]
        elif "Models" in collections and "Datasets" in collections:
            join_obj = [
                {
                    "$lookup": {
                        "from": "Models",
                        "localField": "Models",
                        "foreignField": "_id",
                        "as": "Models",
                    },
                },
                {
                    "$lookup": {
                        "from": "Datasets",
                        "localField": "Datasets",
                        "foreignField": "_id",
                        "as": "Datasets",
                    },
                },
                {"$unwind": {"path": "$Models"}},
                {"$unwind": {"path": "$Datasets"}},
            ]
        elif "Datasets" in collections and "Downstream Tasks" in collections:
            join_obj = [
                {
                    "$lookup": {
                        "from": "Datasets",
                        "localField": "Datasets",
                        "foreignField": "_id",
                        "as": "Datasets",
                    },
                },
                {
                    "$lookup": {
                        "from": "Downstream Tasks",
                        "localField": "Downstream Tasks",
                        "foreignField": "_id",
                        "as": "Downstream Tasks",
                    },
                },
                {"$unwind": {"path": "$Datasets"}},
                {"$unwind": {"path": "$Downstream Tasks"}},
            ]
        elif "Metrics" in collections and "Downstream Tasks" in collections:
            join_obj = [
                {
                    "$lookup": {
                        "from": "Metrics",
                        "localField": "Metrics",
                        "foreignField": "_id",
                        "as": "Metrics",
                    },
                },
                {
                    "$lookup": {
                        "from": "Downstream Tasks",
                        "localField": "Downstream Tasks",
                        "foreignField": "_id",
                        "as": "Downstream Tasks",
                    },
                },
                {"$unwind": {"path": "$Metrics"}},
                {"$unwind": {"path": "$Downstream Tasks"}},
            ]
        else:
            sys.exit(1)  # error
        return join_obj

    def __remove_ids(self, specifications):
        unset = {"$unset": ["_id"]}
        for specification in specifications:
            unset["$unset"].append(f"{specification["collection"]}._id")
        return unset

    def __single_join_query(self, specifications):
        join_database = self.__join_database(specifications)

        if join_database is None:
            return []

        pipeline = self.__construct_join_obj(specifications)
        pipeline.append(self.__construct_match_obj(specifications))
        pipeline.append(self.__remove_ids(specifications))
        pipeline.append(self.__project_obj(specifications))

        return list(join_database.aggregate(pipeline))

    def __multiple_join_query(self, specifications):
        return []
