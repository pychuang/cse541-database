import requests


def result_iter(cursor, size=1000):
    while True:
        results = cursor.fetchmany(size)
        if not results:
            break
        for result in results:
            yield result


def query_solr(solr_url, q, start, rows):
    params = {
        'q': q,
        'start': start,
        'rows': rows,
    }
    r = requests.get(solr_url, params=params)
    if r.status_code != 200:
        print("Failed to query %s with params=%s" % (solr_url, params))
        return []

    return r.json()


def query_solr_iter(solr_url, q, limit=0):
    start = 0
    rows = 1000
    while True:
        if limit and start + rows > limit:
            rows = limit - start
        result = query_solr(solr_url, q, start, rows)
        response = result['response']
        docs = response['docs']
        if not docs:
            break
        for doc in docs:
            yield doc
        start += len(docs)
        if limit and start > limit:
            break
