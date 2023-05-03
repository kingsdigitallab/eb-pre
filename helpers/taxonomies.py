from collections import Counter
from pathlib import Path
from helpers import settings
import sqlite3
import difflib
import re
import json 

class Taxonomy:

    prefix = None

    def __init__(self):
        self.concepts = {}
        self.related = {}
        self.load()

    def get_termids_from_entry(self, entry):
        '''
        Returns the URIs of the terms in entry which are part of this taxonomy.
        entry is a dictionary as returned by Corpus.read_body_and_metadata()
        entry['terms] = [
            {'label': '', 'ref': ''},
        ]
        '''
        ret = []
        for term in entry['terms']:
            termid = re.sub(self.prefix, '', term['ref'])
            if termid != term['ref']:
                if termid in self.concepts:
                    ret.append(termid)

        return ret

    def load(self):
        raise Exception('This method must be implemented in subclass')

    def get_concept(self, concept):
        concept = concept.lower().strip()
        return self.concepts.get(concept, None)

    def get_nearest_concept(self, concept):
        concept = concept.lower().strip()
        ret = self.get_concept(concept)
        if ret is None:
            candidates = difflib.get_close_matches(concept, self.concepts.keys(), 10)
            # print('\t', candidates)
            
            # WARNING: concept not found cotton manufacture
            # ['carbon—manufacture', 'cotton growing and manufacture', 'straw manufacture', 'manufactures', 'ice—manufacture']
            parts = re.findall(r'[a-z]+', concept)
            pattern = '.*'.join([fr'\b{p}' for p in parts])
            for c in candidates:
                if re.search(pattern, c):
                    ret = self.concepts[c]
                    break
            if not ret and len(parts) > 1:
                ret = self.get_concept(parts[-1])
            
            if ret:
                print(f'\tWARNING: nearest concept to {concept} -> {self.get_concept(ret)}')
            else:
                print(f'\tWARNING: no nearest concept to {concept}')
        
        return ret

    def get_parents(self, conceptid):
        ret = self.related.get(conceptid, [])
        # print([(c, self.get_concept(c)) for c in ret])
        return ret

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
                    parents = self.get_parents(term)
                    print('  ' * (5 - levels_left), self.get_concept(term))
                    parent_labels = [self.get_concept(p) for p in parents]
                    # print(f'\t{levels_left}, {self.get_concept(term)} < {parent_labels}')
                    self.count_parent_terms(parents, levels_left, terms_count, expanded)
        else:
            for term in termids:
                print('  ' + ('  ' * (5 - levels_left)), self.get_concept(term))

        return terms_count


class TaxonomyLCSH(Taxonomy):

    prefix = 'lcsh1910:'


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
            uris = [uri.lower().strip() for uri in rec]
            # for i in [0, 1]:
            for i in [1]:
                if uris[i] not in self.related:
                    self.related[uris[i]] = []
                if uris[1-i] not in self.related[uris[i]]:
                    self.related[uris[i]].append(uris[1-i])

        res = cur.execute("select ConceptURI, AlternateURI from ALTERNATE")

        for rec in res.fetchall():
            uris = [uri.lower().strip() for uri in rec]
            for i in [0, 1]:
                if uris[i] not in self.related:
                    self.related[uris[i]] = []
                if uris[1-i] not in self.related[uris[i]]:
                    self.related[uris[i]].append(uris[1-i])


class TaxonomyFastTopical(Taxonomy):

    prefix = 'fast:'

    # <http://id.worldcat.org/fast/966912> <http://www.w3.org/2004/02/skos/core#prefLabel> "Identity (Psychology) in old age" .
    # <http://id.worldcat.org/fast/966912> <http://schema.org/name> "Identity (Psychology) in old age" 
    # <http://id.worldcat.org/fast/966912> <http://www.w3.org/2004/02/skos/core#broader> <http://id.worldcat.org/fast/1199124> .
    # <http://id.worldcat.org/fast/829189> <http://schema.org/sameAs> <http://id.loc.gov/authorities/subjects/sh85012640> .

    def load(self):
        path_json = Path(settings.DATA_PATH, 'fast', 'FASTTopical.json')
        if (path_json.exists()):
            content = json.loads(path_json.read_text())
            self.concepts = content['concepts']
            self.related = content['related']
        else:
            path = Path(settings.DATA_PATH, 'fast', 'FASTTopical.nt')
            content = path.read_text()

            # concept names

            pattern = '<http://id.worldcat.org/fast/([^>]+)> (?:<http://www.w3.org/2000/01/rdf-schema#label>|<http://schema.org/name>) "([^"]+)"'

            self.concepts = {}
            self.related = {}

            for m in re.findall(pattern, content):
                m = [p.lower().strip() for p in m]
                if m[0] not in self.concepts:
                    self.concepts[m[0]] = m[1]
                self.concepts[m[1]] = m[0]

            # broader

            pattern = '<http://id.worldcat.org/fast/([^>]+)> <http://www.w3.org/2004/02/skos/core#broader> <http://id.worldcat.org/fast/([^>]+)>'

            for m in re.findall(pattern, content):
                m = [p.lower().strip() for p in m]
                if m[0] not in self.related:
                    self.related[m[0]] = []
                if m[1] not in self.related[m[0]]:
                    self.related[m[0]].append(m[1])

            # seealso, replacedby

            if 0:

                # pattern = '<http://id.worldcat.org/fast/([^>]+)> (?:<http://purl.org/dc/terms/isReplacedBy>|<http://www.w3.org/2000/01/rdf-schema#seeAlso>) <http://id.worldcat.org/fast/([^>]+)>'
                pattern = '<http://id.worldcat.org/fast/([^>]+)> (?:<http://purl.org/dc/terms/isReplacedBy>) <http://id.worldcat.org/fast/([^>]+)>'

                for m in re.findall(pattern, content):
                    m = [p.lower().strip() for p in m]
                    if m[0] not in self.related:
                        self.related[m[0]] = []
                    if m[1] not in self.related[m[0]]:
                        self.related[m[0]].append(m[1])
                    if m[1] not in self.related:
                        self.related[m[1]] = []
                    if m[0] not in self.related[m[1]]:
                        self.related[m[1]].append(m[0])

            # save

            path_json.write_text(json.dumps({
                'concepts': self.concepts,
                'related': self.related,
            }))

        # print(len(self.concepts.keys()))
        # print(len(self.related.keys()))

        # exit()
