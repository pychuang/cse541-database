from . import paper

class CitegraphCluster(paper.Paper):

    def __init__(self, clusterid, *args, **kwargs):
        super(CitegraphCluster, self).__init__(*args, **kwargs)
        self.clusterid = clusterid


    def get_title(self):
        return (self.title, self.authors, self.venue, self.year)
