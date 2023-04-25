from rdflib import Graph


class Fast:

    def load(self):
        self.graph = Graph()
        self.graph.parse('data/fast/FASTTopical.nt')

        print(len(self.graph))

