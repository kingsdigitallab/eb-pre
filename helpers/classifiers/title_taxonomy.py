from .base_classifier import BaseClassifier
from ..taxonomies import TaxonomyLCSH, TaxonomyFastTopical

class TitleTaxonomy(BaseClassifier):

    def __init__(self):
        # self.taxonomy = TaxonomyFastTopical()
        self.taxonomy = TaxonomyLCSH()
        self.max_levels = 5

    def get_params(self):
        ret = super().get_params()
        ret['taxonomy'] = self.taxonomy.__class__.__name__
        ret['depth'] = self.max_levels
        return ret

    def classify(self, entry):
        ret = ''

        title = entry['title']
        uri = self.taxonomy.get_nearest_concept(title)
        if uri:
            terms_count = self.taxonomy.count_parent_terms([uri], self.max_levels)
            print([
                (self.taxonomy.get_concept(t[0]), t[1]) 
                for t in
                terms_count.most_common(3)
            ])
            # for parent in self.related.get(uri, []):
            #     print('', self.concepts[parent])

        return ret

'''
issues:
1. title doesn't match exact preflabel
2. some concepts don't have parents
3. related can be related (drift) or broader
4. may need more than one hop to reach top label


'''