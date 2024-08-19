def create_query_structure(collection, project, filters):
    query = {
        "collection": collection, 
        "project": project, 
        "filters": filters
    }
    return query

def reworked_query_output(query_output):
    reworked_output = []
    for instance in query_output:
        reworked_instance = {}
        for collection, attributes in instance.items():
            for key, value in attributes.items():
                reworked_instance['.'.join((collection, key))] = value
        reworked_output.append(reworked_instance)
    return reworked_output
