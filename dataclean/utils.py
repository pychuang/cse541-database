def result_iter(cursor, size=1000):
    while True:
        results = cursor.fetchmany(size)
        if not results:
            break
        for result in results:
            yield result
