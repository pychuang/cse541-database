class Paper(object):

    def __init__(self, title=None, authors=None, venue=None, year=None):
        self.title = title
        self.authors = authors
        self.venue = venue
        self.year = year


    def __str__(self):
        return "T:%s A:%s V:%s Y:%s"  % (self.title, self.authors, self.venue, self.year)


    def __repr__(self):
        return "<T:%s A:%s V:%s Y:%s>"  % (self.title, self.authors, self.venue, self.year)
