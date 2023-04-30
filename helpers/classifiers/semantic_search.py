from top2vec import Top2Vec
from helpers import settings
from pathlib import Path
from tqdm import tqdm
import re
import json


class SemanticSearch:
    '''
    Classify entries using top2vec semantic search.
    method:
        . train one embedding & topic model on each edition
        . use top2vec to search for all possible classes/domains
        . return the class/domain where the entries has the highest score
    '''

    def __init__(self):
        # maximum number of documents to train on (for testing purpose); -1: no limit
        self.max_docs = -1
        # the loaded/trained top2vec model
        self.model = None
        # path to the loaded model
        self.model_path = None

    def get_options(self):
        return dict(
            embedding_model='doc2vec',
            # embedding_model='universal-sentence-encoder', # POOR results
            # embedding_model='distiluse-base-multilingual-cased', # decent results, promotes short entries
            speed='fast-learn',
            embedding_batch_size=12,  # 32
            use_embedding_model_tokenizer=True,
            workers=12,
            document_ids=[],
            documents=[]
        )

    def before_classify(self):
        top2vec_domains_path = Path(settings.DATA_PATH, "models", 'top2vec_domains.json')

        domain_results = {}

        model_filename = 'edition_7--1-doc2vec-deep-learn-True.d2v'
        path = str(Path(settings.DATA_PATH, "models", model_filename))
        self.model = Top2Vec.load(path)
        print('loaded')

        aids = []
        titles = []
        query = 'edition==7'
        from helpers.index import Index
        from helpers.corpus import Corpus
        corpus = Corpus()
        index = Index()
        index.load()
        for aid in index.query(query).index:
            body = corpus.read_body(aid)
            if len(body) > 10:
                # documents.append(body.lower())
                aids.append(aid)
                titles.append(body[:20])

        for domain_key, domain_def in settings.DOMAINS.items():
            print(domain_key)
            res = list(zip(*self.model.search_documents_by_keywords(domain_def['name_modern'], 10000)))

            for r in res[:4]:
                print(r[0][:20])
                print(r[2], aids[r[2]], titles[r[2]])
            exit()

            domain_results[domain_key] = [
                p.tolist() for p in res
            ]

        top2vec_domains_path.write_text(json.dumps(domain_results))

    def classify(self, entry):
        ret = 'history'

        model = self.load_model(entry['edition'])

        return ret

    def load_model(self, edition):
        model_path = self.get_model_path(edition)
        if self.model_path != model_path:
            if model_path.exists():
                self.model = Top2Vec.load(model_path)
            else:
                self.model = self.train(edition)
            self.model_path = model_path

        return self.model

    def train(self, edition):
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

    def get_model_path(self, edition):
        return Path(settings.DATA_PATH, "models", self.get_model_filename(edition))

    def get_model_filename(self, edition):
        options = self.get_options()
        query = self.get_query(edition)
        query_hash = re.sub(r'\W+', r'_', query)
        return f'{query_hash}-{self.max_docs}-{options["embedding_model"]}-{options["speed"]}-{options["use_embedding_model_tokenizer"]}.t2v'

    def get_query(self, edition):
        return f'edition=={edition}'


        # num_topics = model.get_num_topics()
        # print(len(documents), num_topics)
        #
        # res = model.get_topics(min(num_topics, 10))
        # for i in range(len(res[0])):
        #     print(res[0][i][:8])
        #
        # documents, document_scores, document_ids = model.search_documents_by_keywords(
        #     keywords=[settings.DOMAINS[0]['name_modern']],
        #     num_docs=20
        # )
        # for doc, score, doc_id in zip(documents, document_scores, document_ids):
        #     print(f"Document: {doc_id}, Score: {score}")
        #     print("-----------")
        #     print(doc[:300])
        #     print("-----------")
        #     print()
