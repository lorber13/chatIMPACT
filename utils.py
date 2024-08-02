import json 

def create_query_structure(collection, project, filters):
    query = {
        "collection": collection,
        "project": project,
        "filters": filters
    }
    return json.dumps(query, indent=2)
