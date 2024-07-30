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


class Dao:
    """data access object"""

    def __init__(self, database) -> None:
        self.database = database

    def query(self, specifications):
        """perform a query"""
        if specifications and len(specifications) == 1:
            return self.__single_collection_query(specifications[0])
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

    def __single_join_query(self, specifications):
        return []

    def __multiple_join_query(self, specifications):
        return []
