import sys
from pathlib import Path

from tqdm import tqdm
import re

project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from tools.index import Index
index = Index()
index.load_or_create()
# index.create()

if 0:
    entries = index.query()
    import pandas as pd
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', 1000)
    print(entries.head(1))

def index_linguistic_properties(query=None):
    '''
    Calculate linguistic properties of entries and add them to the index.
    query is a panda query over the index, which entries should be processed.
        query = 'edition == 9 and volume == 1'
    Takes ~30 mins for 2 editions.
    '''
    from tools import nlp

    for aid in tqdm(index.query(query).index):
        # item = index.df.loc[aid]
        text = index.corpus.read_body(aid)
        props = nlp.compute_linguistic_properties(text)

        for k, v in props.items():
            index.update(aid, k, v)

    index.save()

if 0:
    index_linguistic_properties()


if 0:
    from tools.fast import Fast
    fast = Fast()
    fast.load()
    # fast.getParents('')

if 0:
    eds_titles = {}
    for ed in [7, 9]:
        eds_titles[ed] = set(index.query(f'edition=={ed}')['title'])

    print(f'Same titles: {len(eds_titles[7].intersection(eds_titles[9]))}')

if 0:
    import os
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = "0"
    # os.environ['CUDA_VISIBLE_DEVICES'] = "-1"

    from top2vec import Top2Vec

    aids = [
        'eb09/XML/h12/kp-eb0912-060001-0615-v1.xml'
    ]
    from tools.corpus import Corpus
    corpus = Corpus()
    documents = []

    max_docs = -1
    # max_docs = 1000
    query = 'edition==9'
    options = dict(
        embedding_model='doc2vec',
        #embedding_model='distiluse-base-multilingual-cased', # decent results, promotes short entries
        speed='deep-learn',
        embedding_batch_size=24,  # 32
        use_embedding_model_tokenizer=True,
        workers=12,
    )

    query_hash = re.sub(r'\W+', r'_', query)

    for aid in tqdm(index.query(query).index):
        body = corpus.read_body(aid)
        if len(body) > 10:
            documents.append(body.lower())
        if max_docs > -1 and len(documents) > max_docs:
            break

    model_filename = f'{query_hash}-{max_docs}-{options["embedding_model"]}-{options["speed"]}-{options["use_embedding_model_tokenizer"]}.d2v'

    model = Top2Vec(
        documents,
        # embedding_model='universal-sentence-encoder', # POOR results
        **options
    )

    model.save(str(Path(project_path, "data", "models", model_filename)))

    num_topics = model.get_num_topics()
    print(len(documents), num_topics)

    res = model.get_topics(min(num_topics, 10))
    for i in range(len(res[0])):
        print(res[0][i][:8])

    documents, document_scores, document_ids = model.search_documents_by_keywords(
        keywords=[settings.DOMAINS[0]['name_modern']],
        num_docs=20
    )
    for doc, score, doc_id in zip(documents, document_scores, document_ids):
        print(f"Document: {doc_id}, Score: {score}")
        print("-----------")
        print(doc[:300])
        print("-----------")
        print()

if 0:
    from bertopic import BERTopic
    from tools.corpus import Corpus
    corpus = Corpus()
    documents = []

    max_docs = -1
    # max_docs = 1000
    query = 'edition==9'
    options = dict(
        embedding_model='doc2vec',
        #embedding_model='distiluse-base-multilingual-cased', # decent results, promotes short entries
        speed='deep-learn',
        embedding_batch_size=24,  # 32
        use_embedding_model_tokenizer=True,
        workers=12,
    )

    query_hash = re.sub(r'\W+', r'_', query)

    for aid in tqdm(index.query(query).index):
        body = corpus.read_body(aid)
        if len(body) > 10:
            documents.append(body.lower())
        if max_docs > -1 and len(documents) > max_docs:
            break

    model_filename = f'{query_hash}-{max_docs}.bt'

    model = BERTopic(
    )

    topics, probs = model.fit_transform(documents)

    print(model.get_topic_info())

    model.save(str(Path(project_path, "data", "models", model_filename)))
