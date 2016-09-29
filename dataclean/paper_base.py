class PaperBase(object):

    papers = {}


    def __new__(cls, paper_id, *args, **kwargs):
        obj = object.__new__(cls)
        cls.papers[paper_id] = obj
        return obj

    def __init__(self, paper_id, title=None, authors=None, venue=None, year=None):
        self.paper_id = paper_id
        self.title = title
        self.authors = authors
        self.venue = venue
        self.year = year


    @classmethod
    def find_cached_paper(cls, paper_id):
        if paper_id in cls.papers:
            return cls.papers[paper_id]
        else:
            return None


    def __str__(self):
        return "%s\tT:%s A:%s V:%s Y:%s"  % (self.paper_id, self.title, self.authors, self.venue, self.year)


    def __repr__(self):
        return "<%s\tT:%s A:%s V:%s Y:%s>"  % (self.paper_id, self.title, self.authors, self.venue, self.year)
