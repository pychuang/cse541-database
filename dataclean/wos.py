from . import paper
from . import utils

class WosPaper(paper.Paper):

    papers = {}

    def __init__(self, paper_id, *args, **kwargs):
        super(WosPaper, self).__init__(*args, **kwargs)
        self.paper_id = paper_id
        self.citations = []
        WosPaper.papers[paper_id] = self


    def __str__(self):
        return "%s T:%s A:%s V:%s Y:%s"  % (self.paper_id, self.title, self.authors, self.venue, self.year)


    def __repr__(self):
        return "<%s T:%s A:%s V:%s Y:%s>"  % (self.paper_id, self.title, self.authors, self.venue, self.year)


def get_wos_paper_by_id(cursor, paper_id):
    if paper_id in WosPaper.papers:
        print 'found', paper_id, 'in cache'
        return WosPaper.papers[paper_id]

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
        print 'found citations of', paper.paper_id
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
        if uid in WosPaper.papers:
            print 'found citation', uid, 'in cache'
            cp = WosPaper.papers[uid]
            if not cp.venue:
                cp.venue = citedTitle
            if not cp.year:
                cp.year = year
        else:
            cp = WosPaper(uid, title=citedTitle, venue=citedWork, year=year)
        paper.citations.append(cp)
    return paper.citations
