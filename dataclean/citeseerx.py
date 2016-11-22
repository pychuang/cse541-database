from . import paper_base
from . import utils


class CgCluster(paper_base.PaperBase):

    def __init__(self, *args, **kwargs):
        super(CgCluster, self).__init__(*args, **kwargs)
        self.citedby = None
        self.cites = None
        self.citations = []
        self.dois = None


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


    def find_cited_clusters_ids(self, cursor):
        if self.cites is not None:
            return self.cites

        cursor.execute("""
            SELECT cited
            FROM citegraph
            WHERE citing = %s;""", (self.paper_id, ))
        result = cursor.fetchall()
        self.cites = [d[0] for d in result]
        return self.cites


    def get_dois(self, cursor):
        if self.dois is not None:
            return self.dois

        cursor.execute("""
            SELECT id
            FROM papers
            WHERE cluster = %s;""", (self.paper_id, ))
        result = cursor.fetchall()
        self.dois = [d[0] for d in result]
        return self.dois


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
    def get_citations(cls, cursor, cluster):
        if cluster.citations:
            return cluster.citations

        cites = cluster.find_cited_clusters_ids(cursor)
        for cite in cites:
            cited_cluster = cls.get_cluster_by_id(cursor, cite)
            cluster.citations.append(cited_cluster)

        return cluster.citations


    @classmethod
    def find_clusters_by_title(cls, cursor, title):
        if not title:
            return None

        cursor.execute("""
            SELECT id, ctitle, cvenue, cyear
            FROM clusters
            WHERE ctitle = %s;""", (title, ))
        results = cursor.fetchall()

        clusters = []
        for result in results:
            cluster_id, ctitle, cvenue, cyear = result
            if cluster_id in cls.papers:
                cluster= cls.papers[cluster_id]
            else:
                cluster = cls(cluster_id, title=ctitle, venue=cvenue, year=cyear)
            clusters.append(cluster)
        return clusters


    @classmethod
    def find_clusters_by_title_on_solr(cls, solr_url, title):
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


class CsxPaper(paper_base.PaperBase):

    def __init__(self, *args, **kwargs):
        super(CsxPaper, self).__init__(*args, **kwargs)
        self.citedby = None


    @classmethod
    def get_paper_by_id(cls, cursor, paper_id):
        paper = cls.find_cached_paper(paper_id)
        if paper:
            return paper

        cursor.execute("""
            SELECT title, venue, year
            FROM papers
            WHERE id = %s;""", (paper_id, ))
        result = cursor.fetchone()
        if not result:
            return None

        title, venue, year = result
        paper = cls(paper_id, title=title, venue=venue, year=year)
        return paper


    @classmethod
    def find_papers_ids_with_citations_matched_by_title(cls, cursor, title):
        cursor.execute("""
            SELECT DISTINCT paperid
            FROM citations
            WHERE title = %s;""", (title, ))

        papers_ids = []
        for result in utils.result_iter(cursor):
            paper_id, = result
            papers_ids.append(paper_id)
        return papers_ids
