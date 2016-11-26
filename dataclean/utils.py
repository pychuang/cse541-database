import requests
import re


def result_iter(cursor, size=1000):
    while True:
        results = cursor.fetchmany(size)
        if not results:
            break
        for result in results:
            yield result


def query_solr(solr_url, q, start, rows, mm=None):
    params = {
        'q': q,
        'start': start,
        'rows': rows,
    }
    if mm:
        params['mm'] = mm
    r = requests.get(solr_url, params=params)
    if r.status_code != 200:
        print("Failed to query %s with params=%s" % (solr_url, params))
        return []

    return r.json()


def query_solr_iter(solr_url, q, mm=None, limit=0):
    start = 0
    rows = 1000
    while True:
        if limit:
            if start >= limit:
                break
            if start + rows > limit:
                rows = limit - start
        result = query_solr(solr_url, q, start, rows, mm)
        response = result['response']
        docs = response['docs']
        if not docs:
            break
        for doc in docs:
            yield doc
        if len(docs) < rows:
            break
        start += len(docs)


def normalize_query_string(s):
    # remove all punctuations and digits
    s  = re.sub(r"\d\s\p", r' ', s)
    return ' '.join(s.split())
