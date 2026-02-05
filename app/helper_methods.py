import pynamodb.pagination

def response_to_dict(query: pynamodb.pagination.ResultIterator):
    results = []
    for item in query:
        to_dict = item.to_simple_dict()
        results.append(to_dict)
    return results