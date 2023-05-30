from bertopic import BERTopic
from helpers import settings
from pathlib import Path
from .base_classifier import BaseClassifier
from helpers.corpus import Corpus

class GuidedTopics(BaseClassifier):

    def __init__(self):
        self.model = None
        self.remove_stop_words = True
        self.use_guided_topics = False
        self.less_outliers = True

    def load_or_create_model(self, edition):
        limit = -1
        fn = ''
        if self.less_outliers:
            fn += '-lessoutliers'
        if self.use_guided_topics:
            fn += '-guided'
        if self.remove_stop_words:
            fn += '-stopwords'
        path = self.get_file_path(f'edition-{edition}{fn}.bt')
        if path.exists():
            self.model = BERTopic.load(path)
        else:
            options = {}

            if self.less_outliers:
                from hdbscan import HDBSCAN

                hdbscan_model = HDBSCAN(
                    min_cluster_size=10, metric='euclidean', 
                    cluster_selection_method='eom', prediction_data=True, min_samples=5
                )

                options['hdbscan_model'] = hdbscan_model

            if self.remove_stop_words:
                from bertopic.vectorizers import ClassTfidfTransformer
                ctfidf_model = ClassTfidfTransformer(reduce_frequent_words=True)
                options['ctfidf_model'] = ctfidf_model

            if self.use_guided_topics:
                seed_topic_list = [
                    d['name_modern']
                    for d in settings.DOMAINS.values()
                ]
                options['seed_topic_list'] = seed_topic_list

            self.model = BERTopic(**options)
            print('read docs')
            corpus = Corpus()
            docs = [
                corpus.read_body(aid)
                for aid in corpus.read_ids()
            ]
            print('fit model')
            self.model.fit_transform(docs)
            print('save model')
            self.model.save(str(path))
        
        return self.model

    def classify(self, entry):
        self.load_or_create_model(9)
        return ''
