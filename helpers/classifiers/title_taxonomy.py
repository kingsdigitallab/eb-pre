import difflib
from ..taxonomies import TaxonomyLCSH

class TitleTaxonomy:

    def __init__(self):
        self.taxonomy = TaxonomyLCSH()
        self.max_levels = 10
    
    def classify(self, entry):
        ret = ''

        title = entry['title']
        uri = self.get_uri_from_term_label(title)
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

    def get_uri_from_term_label(self, label):
        '''Return exact match if it exists in the taxonomy.
        Otherwise returns the best match based on string similarity.'''
        ret = self.taxonomy.get_concept(label)
        if not ret:
            print(f'WARNING: term label not found in taxonomy: "{label}"')
        return ret

        label = label.lower().strip()
        ret = self.concepts.get(label, None)
        if not ret:
            print(f'WARNING: term label not found in taxonomy: "{label}"')
            print('\t', difflib.get_close_matches(label, self.concepts.keys(), 5))

        return ret


'''
issues:
1. title doesn't match exact preflabel
2. some concepts don't have parents
3. related can be related (drift) or broader
4. may need more than one hop to reach top label

(venv) jeff@j3470:~/src/prj/brit19$ python tools/classify.py 
 law
 surgery, operative—jurisprudence
 evidence (law)
 negligence
 malpractice
 medical laws and legislation
 poisons
 pharmacists
 chemistry, forensic
MEDICAL JURISPRUDENCE: expected: medicine, predicted: 
 biology
 medicine
 hygiene
 science
 anatomy
PHYSIOLOGY: expected: medicine, predicted: 
HISTORY: expected: history, predicted: 
ROMAN HISTORY: expected: history, predicted: 
 footprints, fossil
 engineering
 kinematics
 machinery
 physics
 dynamics
 motion
 mathematics
MECHANICS: expected: natural_philosophy, predicted: 
 light
 physics
 photometry
OPTICS: expected: natural_philosophy, predicted: 
 bas-relief
 decoration and ornament
 statues
 esthetics
 art
SCULPTURE: expected: fine_arts, predicted: 
PAINTING: expected: fine_arts, predicted: 
ARCHITECT: expected: useful_arts, predicted: 
COTTON MANUFACTURE: expected: useful_arts, predicted: 
 geography
 earth
 geology
PHYSICAL GEOGRAPHY: expected: natural_history, predicted: 
 natural history
 science
 plants
 nature study
 fixed ideas
BOTANY: expected: natural_history, predicted: 
HYPOCHONDRIASIS: expected: medicine, predicted: 
HAMMER: expected: useful_arts, predicted: 
RUSSIA: expected: history, predicted: 
TitleTaxonomy - Accuracy: 0% = 0 / 15
'''