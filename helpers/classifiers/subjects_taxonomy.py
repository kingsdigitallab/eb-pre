from .title_taxonomy import TitleTaxonomy
import re
from collections import Counter

class SubjectsTaxonomy(TitleTaxonomy):

    def classify(self, entry):

        terms = self.taxonomy.get_termids_from_entry(entry)
        for termid in terms:
            print(
                termid,
                self.taxonomy.get_concept(termid),
                '<',
                ' ; '.join([self.taxonomy.get_concept(parent) for parent in self.taxonomy.get_parents(termid)])
            )

        terms_count = self.taxonomy.count_parent_terms(terms, self.max_levels)
        print([
            (self.taxonomy.get_concept(t[0]), t[1]) 
            for t in
            terms_count.most_common(3)
        ])

        return ''

