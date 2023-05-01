from .title_taxonomy import TitleTaxonomy
import re
from collections import Counter

class SubjectsTaxonomy(TitleTaxonomy):

    def classify(self, entry):
        print('-'*40)

        terms = []
        for term in entry['terms']:
            termid = re.sub(r'lcsh1910:', '', term['ref'])
            if term['ref'] != termid:
                terms.append(termid)
                print(
                    termid, 
                    self.taxonomy.get_concept(termid),
                    '<',
                    ' ; '.join([self.taxonomy.get_concept(parent) for parent in self.taxonomy.get_parents(termid)])
                )

        terms_count = self.taxonomy.count_parent_terms(terms, 10)
        print([
            (self.taxonomy.get_concept(t[0]), t[1]) 
            for t in
            terms_count.most_common(3)
        ])

        return ''

