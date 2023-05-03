from txtai.pipeline import Labels
from helpers import settings

class ZeroShot:
    '''
    txtai zero-shot classifier
    https://github.com/neuml/txtai/blob/master/examples/07_Apply_labels_with_zero_shot_classification.ipynb
    53% accuracy by default on body
    60% accuracy by default on title
    '''

    def __init__(self):
        # Create labels model
        self.labels = Labels()
        self.domain_keys = []
        self.domain_tags = []
        for k, d in settings.DOMAINS.items():
            self.domain_tags.append(', '.join(d['name_modern']))
            self.domain_keys.append(k)

    def classify(self, entry):
        ret = ''
        # res = self.labels(entry['body'], self.domain_tags)[0][0]
        if entry['title']:
            res = self.labels(entry['title'], self.domain_tags)[0][0]
            print(self.domain_tags[res])
            ret = self.domain_keys[res]
        # print(res)
        return ret
