from . import paper_base
from . import utils

class WosPaper(paper_base.PaperBase):

    def __init__(self, *args, **kwargs):
        super(WosPaper, self).__init__(*args, **kwargs)
        self.citations = []


def get_paper_by_id(cursor, paper_id):
    paper = WosPaper.find_cached_paper(paper_id)
    if paper:
        print '** found', paper_id, 'in cache'
        return paper

    cursor.execute("""
        SELECT title, pubname
        FROM papers
        WHERE papers.uid = %s;""", (paper_id, ))
    result = cursor.fetchone()
    if not result:
        return None

    title, pubname = result
    paper = WosPaper(paper_id, title=title, venue=pubname)
    return paper


def get_citations(cursor, paper):
    if paper.citations:
        print '** found citations of', paper.paper_id
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
        cp = WosPaper.find_cached_paper(uid)
        if cp:
            print '** found citation', uid, 'in cache'
            if not cp.venue:
                cp.venue = citedTitle
            if not cp.year:
                cp.year = year
        else:
            cp = WosPaper(uid, title=citedTitle, venue=citedWork, year=year)
        paper.citations.append(cp)
    return paper.citations
