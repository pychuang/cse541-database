from . import paper_base
from . import utils

class CitegraphCluster(paper_base.PaperBase):
    pass


def find_cluster_by_title(cursor, title):
    if not title:
        return None

    cursor.execute("""
        SELECT id, ctitle, cvenue, cyear
        FROM clusters
        WHERE ctitle = %s;""", (title, ))

    clusters = []
    for result in utils.result_iter(cursor):
        cid, ctitle, cvenue, cyear = result
        clusters.append(result)
    return clusters
