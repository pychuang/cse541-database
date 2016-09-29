from . import paper_base
from . import utils


class CsxCluster(paper_base.PaperBase):

    def __init__(self, *args, **kwargs):
        super(CsxCluster, self).__init__(*args, **kwargs)
        self.citedby = None


    def find_citing_clusters(self, solr_url):
        if self.citedby is not None:
            return self.citedby

        '''
        cursor.execute("""
            SELECT citing
            FROM citegraph
            WHERE cited = %s;""", (clusterid,))
        result = cursor.fetchall()
        self.citedby = [d[0] for d in result]
        '''

        self.citedby = []
        q = "cites:%d" % self.paper_id
        result = utils.query_solr(solr_url, q)
        for doc in utils.docs_of_solr_result(result):
            cluster_id = doc['id']
            cluster = CsxCluster.find_cached_paper(cluster_id)
            if not cluster:
                if 'title' not in doc:
                    continue

                title = doc['title']
                if 'venue' in doc:
                    venue = doc['venue']
                else:
                    venue = None
                if 'year' in doc:
                    year = doc['year']
                else:
                    year = None

                cluster = CsxCluster(cluster_id, title=title, venue=venue, year=year)
            self.citedby.append(cluster)

        return self.citedby


def find_clusters_by_title(cursor, title):
    if not title:
        return None

    cursor.execute("""
        SELECT id, ctitle, cvenue, cyear
        FROM clusters
        WHERE ctitle = %s;""", (title, ))

    clusters = []
    for result in utils.result_iter(cursor):
        cid, ctitle, cvenue, cyear = result
        cluster = CsxCluster.find_cached_paper(cid)
        if not cluster:
            cluster = CsxCluster(cid, title=ctitle, venue=cvenue, year=cyear)
        clusters.append(cluster)
    return clusters
