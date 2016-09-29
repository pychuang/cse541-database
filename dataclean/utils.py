import requests


def result_iter(cursor, size=1000):
    while True:
        results = cursor.fetchmany(size)
        if not results:
            break
        for result in results:
            yield result


def query_solr(solr_url, q, start=0, rows=10):
    params = {
        'q': q,
        'start': start,
        'rows': rows,
    }
    r = requests.get(solr_url, params=params)
    if r.status_code != 200:
        print "Failed to query %s with params=%s" % (solr_url, params)
        return None

    return r.json()


def docs_of_solr_result(result):
    response = result['response']
    return response['docs']
