from . import paper_base
from . import utils


class CsxCluster(paper_base.PaperBase):

    def __init__(self, *args, **kwargs):
        super(CsxCluster, self).__init__(*args, **kwargs)
        self.citedby = None


    def find_citing_clusters_ids(self, cursor):
        if self.citedby is not None:
            return self.citedby

        cursor.execute("""
            SELECT citing
            FROM citegraph
            WHERE cited = %s;""", (self.paper_id, ))
        result = cursor.fetchall()
        self.citedby = [d[0] for d in result]
        return self.citedby


    @classmethod
    def get_cluster_by_id(cls, cursor, cluster_id):
        cluster = cls.find_cached_paper(cluster_id)
        if cluster:
            return cluster

        cursor.execute("""
            SELECT ctitle, cvenue, cyear
            FROM clusters
            WHERE id = %s;""", (cluster_id, ))
        result = cursor.fetchone()
        if not result:
            return None

        ctitle, cvenue, cyear = result
        cluster = cls(cluster_id, title=ctitle, venue=cvenue, year=cyear)
        return cluster


    @classmethod
    def find_clusters_by_title(cls, solr_url, title):
        if not title:
            return None

        clusters = []
        q = "title:\"%s\"" % title
        for doc in utils.query_solr_iter(solr_url, q):
            cluster_id = doc['id']
            cluster = cls.find_cached_paper(cluster_id)
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

                cluster = cls(cluster_id, title=title, venue=venue, year=year)
            clusters.append(cluster)

        return clusters
