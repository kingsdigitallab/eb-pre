from helpers import settings
from pathlib import Path
from tqdm import tqdm
from .base_classifier import BaseClassifier
import re
import json


class SemanticSearch(BaseClassifier):
    '''
    Classify entries using top2vec semantic search.
    method:
        . train one embedding & topic model on each edition
        . use top2vec to search for all possible classes/domains
        . return the class/domain where the entry has the highest score
    '''

    def __init__(self):
        # maximum number of documents to train on (for testing purpose); -1: no limit
        self.max_docs = -1
        # the loaded/trained top2vec model
        self.model = None
        # path to the loaded model
        self.model_path = None
        # results of semantic searches on all the pre-defined domains
        # {domain_string: {'scores': [], 'aids': []}, ...}
        self.domain_results = None

    def get_params(self):
        ret = super().get_params()
        options = self.get_options()
        for k in ['speed']:
            ret[k] = options[k]
        return ret

    def get_options(self):
        return dict(
            # embedding_model='universal-sentence-encoder', # POOR results
            # embedding_model='distiluse-base-multilingual-cased', # decent results, promotes short entries
            # To try
            # embedding_model='universal-sentence-encoder-large', # ?
            # all-MiniLM-L6-v2
            # paraphrase-multilingual-MiniLM-L12-v2
            embedding_model='doc2vec',
            speed='fast-learn',
            # speed='deep-learn',
            embedding_batch_size=12,  # 32
            use_embedding_model_tokenizer=True,
            workers=12,
            document_ids=[],
            documents=[],
            keep_documents=False,
            # False by default, which may mean long docs are truncated
            split_documents=True,
        )

    def before_classify(self, entry):

        edition = entry["edition"]
        options = self.get_options()
        top2vec_domains_path = self.get_file_path(f'{self.get_model_filename(edition)}_domains.json')

        if top2vec_domains_path.exists():
            self.domain_results = json.loads(top2vec_domains_path.read_text())
        else:
            self.domain_results = {}
            model = self.load_model(edition)

            for domain_key, domain_def in settings.DOMAINS.items():
                res = model.search_documents_by_keywords(
                    domain_def['name_modern'],
                    10000,
                    return_documents=False
                )

                self.domain_results[domain_key] = {
                    'scores': res[0].tolist(),
                    'aids': res[1].tolist(),
                }

            top2vec_domains_path.write_text(json.dumps(self.domain_results))

    def classify(self, entry, scores=None):
        ret = ''

        idx = None
        self.before_classify(entry)

        domain_scores = []
        for domain_key, results in self.domain_results.items():
            try:
                idx = results['aids'].index(entry['aid'])
                score = results['scores'][idx]
            except ValueError:
                score = 0
            domain_scores.append([domain_key, score])

        domain_scores = sorted(domain_scores, key=lambda ds: ds[1], reverse=True)

        if domain_scores[0][1] > 0:
            ret = domain_scores[0][0]

        if scores is not None:
            scores.extend(domain_scores)

        if 0:
            for idx in [0, 1, -1]:
                print(f'  {domain_scores[idx]}')

        return ret
        # best = {
        #     'score': 0,
        #     'domain': '',
        # }
        # for domain_key, results in self.domain_results.items():
        #     try:
        #         idx = results['aids'].index(entry['aid'])
        #         score = results['scores'][idx]
        #         if score > best['score']:
        #             best['domain'] = domain_key
        #             best['score'] = score
        #     except ValueError:
        #         pass
        #
        # return best['domain']

    def load_model(self, edition):
        model_path = self.get_model_path(edition)
        if self.model_path != model_path:
            if model_path.exists():
                from top2vec import Top2Vec
                self.model = Top2Vec.load(model_path)
            else:
                self.model = self.train(edition)
            self.model_path = model_path

        return self.model

    def train(self, edition):
        from top2vec import Top2Vec

        from helpers.corpus import Corpus
        corpus = Corpus()
        from helpers.index import Index
        index = Index()
        index.load()

        max_docs = self.max_docs
        # max_docs = 1000
        query = self.get_query(edition)

        options = self.get_options()
        for aid in tqdm(index.query(query).index):
            body = corpus.read_body(aid)
            if len(body) > 10:
                options['documents'].append(body.lower())
                options['document_ids'].append(aid)
            if max_docs > -1 and len(options['documents']) > max_docs:
                break

        model = Top2Vec(
            **options
        )

        model.save(str(self.get_model_path(edition)))

        return model

    def get_model_filename(self, edition):
        options = self.get_options()
        query = self.get_query(edition)
        query_hash = re.sub(r'\W+', r'_', query)
        return f'{query_hash}-{self.max_docs}-{options["embedding_model"]}-{options["speed"]}-TK{int(options["use_embedding_model_tokenizer"])}-SD{int(options["split_documents"])}.t2v'

