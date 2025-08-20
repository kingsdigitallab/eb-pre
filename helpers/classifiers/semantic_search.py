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
        self.index = None
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
        ret = dict(
            # https://top2vec.readthedocs.io/en/stable/api.html?highlight=use_embedding_model_tokenizer

            # embedding_model='universal-sentence-encoder', # POOR results
            # embedding_model='distiluse-base-multilingual-cased', # decent results, promotes short entries
            # To try
            # embedding_model='universal-sentence-encoder-large', # ?
            # all-MiniLM-L6-v2
            # paraphrase-multilingual-MiniLM-L12-v2
            embedding_model='doc2vec',
            # deep-learn doesn' seem worth it on this corpus: takes ~7 hours and not much difference
            # speed='fast-learn'|'learn'|'deep-learn',
            speed='learn',
            # 
            use_embedding_model_tokenizer=True,
            # default 50. Ignore all words with freq < min_count
            # Lowering this will increase the vocabulary & model size
            # 50 -> 25 : files larger by a quarter
            # / doesn't seem to make a large difference in results...
            min_count=40,
            # https://radimrehurek.com/gensim/models/phrases.html
            # Captures 2-grams if True (default is False)
            # + v. interesting word neighbours results
            # +/- Impact on knn docs isn't significant: some noise, but also better capture multiple meanings
            # - Increases size of files by a 3rd
            ngram_vocab=True,
            # False by default, which may mean long docs are truncated
            # If True => doc vector = avg(chunks vectors)
            split_documents=True,
            # default = sequential
            document_chunker = 'sequential',
            # comment to use the default 100 char sequential chunker with 0.5 overlap instead
            # if defined, chunks = sentences
            # + might classify slightly better
            # / no major diffierence in word & doc nearest neighbours
            sentencizer=self.sentencizer,

            # TOPIC
            # default = 0.1; min cosine distance to keep topics apart
            # increase to get less topics
            topic_merge_delta=0.5,

            # if True the content of the document is part of the model
            keep_documents=False,

            # Don't affect model 
            embedding_batch_size=32,  # 32
            workers=12,
            document_ids=[],
            documents=[],
        )

        if ret.get('sentencizer', None):
            ret['document_chunker'] = 'sentence'
        
        return ret

    def get_model_filename(self, edition):
        options = self.get_options()

        parts = [
            ['', self.get_class_key()],
            ['', re.sub(r'\W+', r'_', self.get_query(edition))],
            ['', options["embedding_model"]],
            ['', options["speed"]],
            ['mc', options["min_count"]],
            ['ng', int(options["ngram_vocab"])],
            ['tm', options['topic_merge_delta']],
            ['ch', options['document_chunker']],
        ]

        return '-'.join([
            (f'{k}_{v}' if k else v)
            for k, v in parts
        ]) + '.tv2'

    def before_classify(self, edition=7):
        '''       
        Compute self.domain_results, a dictionnary mapping a domain_key to a 
        {'scores': [], 'aids': []}
        where scores[i] is the similarity of item aids[i] 
        in the embedding model with the domain with key domain_key.

        The dictionnary is saved to a json file.

        If the file already exists self.domain_results is read from it 
        rather than computer.
        '''
        # edition = entry["edition"]
        options = self.get_options()
        top2vec_domains_path = self.get_file_path(f'{settings.DOMAINS_SET}/{self.get_model_filename(edition)}_domains.json')

        # print(f'before_classify: {top2vec_domains_path}')
        if top2vec_domains_path.exists():
            print(f'READ domains neighbours from {top2vec_domains_path}')
            self.domain_results = json.loads(top2vec_domains_path.read_text())
        else:
            print(f'COMPUTE domains neighbours...')
            self.domain_results = {}
            model = self.load_model(edition)

            # if 0:
            #     for seeds in [['SACRED'], ['sacred'], ['sacred', 'SACRED'], ['sacred', 'sacred']]:
            #     # for seeds in [['sacred', 'sacred']]:
            #         res = self.search_documents_by_seeds(model, seeds)
            #     exit()

            for domain_key, domain_def in settings.DOMAINS.items():
                res = self.search_documents_by_seeds(model, domain_def['name_modern'])

                self.domain_results[domain_key] = {
                    'scores': res[0].tolist(),
                    'aids': res[1].tolist(),
                }

            print(f'WRITTEN domains neighbours into {top2vec_domains_path}')

            top2vec_domains_path.write_text(json.dumps(self.domain_results))

    def get_index(self):
        if not self.index:
            from helpers.index import Index
            index = Index()
            index.load()
            self.index = index
        
        return self.index

    def search_documents_by_seeds(self, model, seeds, edition=7):
        # TODO: avoid calling private methods

        vectors = model._words2word_vectors([s for s in seeds if s == s.lower()]).tolist()

        index = self.get_index()
        for seed in seeds:
            if seed != seed.lower():
                query = f'title == "{seed}" and edition == {edition}'
                entries = index.query(query)

                if len(entries) != 1:
                    entries_indexes = ", ".join(entries.index.tolist())
                    raise Exception(f'Query title = {seed} and edition = {edition} in index did not return a single row. ({len(entries)} matches, {entries_indexes})')

                aid = entries.index[0]
                try:
                    doc_idx = model.doc_id2index[aid]
                except KeyError:
                    raise Exception(f'Document with id = {aid} is in the index but not in the model (Query title = {seed} and edition = {edition})')
                vectors.append(model.document_vectors[doc_idx])
                
        vector = model._get_combined_vec(vectors, [])
        
        res = model.search_documents_by_vector(
            vector,
            10000,
            return_documents=False
        )

        # print(f'seeds: {seeds}')
        # print(res[0][:10])

        return res

    def search_documents_by_seeds_old(self, model, seeds):
        res = model.search_documents_by_keywords(
            seeds,
            10000,
            return_documents=False
        )

        print(f'seeds: {seeds}')
        print(res[0][:10])

        return res

    def classify(self, entry, scores=None):
        '''
        Returns the key of the domain 
        which has the highest similarity score 
        to the given entry.

        scores arg is an optional list that will be extended
        with [key, score] for each domain.
        Sorted by score (high to low).
        '''
        ret = ''

        idx = None

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

    def load_model(self, edition):
        '''
        Load the embeding model.
        Or train it if it doesn't already exist.
        '''
        if 0:
            self.model = self.train(edition)

        model_path = self.get_model_path(edition)
        if self.model_path != model_path:
            if model_path.exists():
                print(f'Load model {model_path}...')
                from top2vec import Top2Vec
                self.model = Top2Vec.load(model_path)
            else:
                self.model = self.train(edition)
                self.convert_model_to_json(edition)
            self.model_path = model_path

        self.check_all_docs_in_model(edition)

        return self.model

    def check_all_docs_in_model(self, edition):
        # check that all docs in index are in the model
        model_qt = len(self.model.doc_id2index)
        index = self.get_index()
        entries = index.query(f'edition == {edition}')
        index_qt = len(entries)
        if (index_qt != model_qt):
            # raise Exception(f'Documents in model: {len(self.model.doc_id2index)} <> documents in index: {len(entries)}')
            print(f'Documents in model: {len(self.model.doc_id2index)} <> documents in index: {len(entries)}')

    def convert_model_to_json(self, edition):
        model = self.load_model(edition)
        # ops:
        # . label <-> vector
        res = {}
        if 1:
            vectors = model.word_vectors.tolist()
            res = {
                f'{label}': vectors[idx]
                for label, idx
                in model.word_indexes.items()
            }
            print(f'{len(vectors)} word vectors')
        if 1:
            from helpers.index import Index
            index = Index()
            index.load()

            vectors = model.document_vectors.tolist()
            res = res | {
                f'{index.get_row(label)["title"]}': vectors[idx]
                for label, idx
                in model.doc_id2index.items()
            }
            print(f'{len(vectors)} document vectors')
        print(f'{len(res)} vectors')
        # path_json = Path(settings.DATA_PATH, 'semantic_search', f'edition_{edition}-')
        json_path = Path(str(self.get_model_path(edition)) + '.json')
        json_path.write_text(json.dumps(res))
        print(f'Written {json_path}')

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

        options = self.get_options().copy()
        for aid in tqdm(index.query(query).index):
            body = corpus.read_body(aid)
            if len(body) > 10:
                options['documents'].append(body.lower())
                options['document_ids'].append(aid)
            else:
                print(aid, len(body), index.get_row(aid))
            if max_docs > -1 and len(options['documents']) > max_docs:
                break

        print(f'Training model on {len(options['document_ids'])} documents.')
        # exit()

        model = Top2Vec(
            **options
        )

        model.save(str(self.get_model_path(edition)))

        return model


