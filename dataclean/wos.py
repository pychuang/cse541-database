from . import paper_base
from . import utils


class WosPaper(paper_base.PaperBase):

    def __init__(self, *args, **kwargs):
        super(WosPaper, self).__init__(*args, **kwargs)
        self.citations = []


    def get_authors(self, cursor):
        if self.authors:
            return self.authors

        cursor.execute("""
            SELECT wos_standard_name
            FROM names
            WHERE paperid = %s;""", (self.paper_id, ))

        self.authors = []
        for result in utils.result_iter(cursor):
            author, = result
            self.authors.append(author)
        return self.authors


    @classmethod
    def get_paper_by_id(cls, cursor, paper_id):
        paper = cls.find_cached_paper(paper_id)
        if paper:
            return paper

        cursor.execute("""
            SELECT title, pubname, date
            FROM papers
            WHERE papers.uid = %s;""", (paper_id, ))
        result = cursor.fetchone()
        if not result:
            return None

        title, pubname, date_time = result
        year = date_time.year
        paper = cls(paper_id, title=title, venue=pubname, year=year)
        return paper


    @classmethod
    def get_citations(cls, cursor, paper):
        if paper.citations:
            return paper.citations

        cursor.execute("""
            SELECT uid, citedTitle, citedWork, year
            FROM citations
            WHERE paperid = %s;""", (paper.paper_id, ))

        for result in utils.result_iter(cursor):
            uid, citedTitle, citedWork, year = result
            if not uid:
                continue
            if not citedTitle:
                continue
            cp = cls.find_cached_paper(uid)
            if cp:
                if not cp.venue:
                    cp.venue = citedTitle
                if not cp.year:
                    cp.year = year
            else:
                cp = cls(uid, title=citedTitle, venue=citedWork, year=year)
            paper.citations.append(cp)
        return paper.citations
