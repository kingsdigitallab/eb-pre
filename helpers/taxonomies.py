from collections import Counter
from pathlib import Path
from helpers import settings
import sqlite3

class Taxonomy:

    def __init__(self):
        self.concepts = {}
        self.related = {}
        self.load()

    def load(self):
        raise Exception('This method must be implemented in subclass')

    def get_concept(self, concept):
        concept = concept.lower().strip()
        return self.concepts.get(concept, None)

    def get_parents(self, conceptid):
        return self.related.get(conceptid, [])

    def count_parent_terms(self, termids, levels_left=0, terms_count=None, expanded=None):
        if terms_count is None:
            terms_count = Counter()
        if expanded is None:
            expanded = []
        
        terms_count.update(termids)
        
        if levels_left:
            levels_left -= 1

            for term in termids:
                if term not in expanded:
                    expanded.append(term)
                    parents = [parent for parent in self.related.get(term, [])]
                    self.count_parent_terms(parents, levels_left, terms_count, expanded)

        return terms_count


class TaxonomyLCSH(Taxonomy):

    def load(self):
        con = sqlite3.connect(str(Path(settings.DATA_PATH, 'lcsh1910.db')))
        cur = con.cursor()
        res = cur.execute("select ConceptURI, PrefLabel from CONCEPT")

        self.concepts = {}

        for rec in res.fetchall():
            label = rec[1].lower().strip()
            uri = rec[0].lower().strip()
            self.concepts[label] = uri
            self.concepts[uri] = label
        
        res = cur.execute("select ConceptURI, RelatedURI from RELATED")

        self.related = {}

        for rec in res.fetchall():
            uri = rec[1].lower().strip()
            if uri not in self.related:
                self.related[uri] = []
            self.related[uri].append(rec[0].lower().strip())
            
