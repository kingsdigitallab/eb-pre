from bertopic import BERTopic
from helpers import settings
from pathlib import Path
from .base_classifier import BaseClassifier
from helpers.corpus import Corpus

class GuidedTopics(BaseClassifier):

    def __init__(self):
        self.model = None

    def load_or_create_model(self, edition):
        limit = 1000
        path = self.get_file_path(f'edition_{edition}__{limit}.bt')
        if path.exists():
            self.model = BERTopic.load(path)
        else:
            seed_topic_list = [
                d['name_modern']
                for d in settings.DOMAINS.values()
            ]
            self.model = BERTopic(seed_topic_list=seed_topic_list)
            print('read docs')
            corpus = Corpus()
            docs = [
                corpus.read_body(aid)
                for aid in corpus.read_ids()
            ]
            print('fit model')
            self.model.fit_transform(docs)
            self.model.save(str(path))
            print('save model')
            self.model.save(str(path))

    def classify(self, entry):
        self.load_or_create_model(7)
        return ''

