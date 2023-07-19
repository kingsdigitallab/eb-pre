import sys
from pathlib import Path

from tqdm import tqdm
import re

project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from helpers.index import Index
index = Index()
index.load_or_create()
# index.create()

if 1:
    from helpers.classifiers.semantic_search import SemanticSearch
    semsearch = SemanticSearch()
    model = semsearch.load_model(7)
    print(model.get_num_topics())

    topic_words, word_scores, topic_nums = model.get_topics()
    for i, words in enumerate(topic_words):
        print(i, words[:10])


if 0:
    ''' 7th edition, 0.5 top2vec topics

0 ['baptismal name' 'ellichpoor long' 'puts stop' 'much stress' 'throw off'
 'throw down' 'plastered over' 'novi testamenti' 'pulled off'
 'provincially called']
1 ['county' 'counties' 'parish' 'barony' 'borough' 'galway' 'burgh' 'antrim'
 'forfar' 'longford']
2 ['arsenal' 'dock' 'storehouses' 'stores' 'victualling' 'docks' 'naval'
 'wharf' 'yard' 'ships']
3 ['lunar' 'epact' 'moon' 'epacts' 'intercalary' 'moons' 'intercalation'
 'solar' 'cycle' 'sidereal']
4 ['deceased' 'sepulchres' 'funeral' 'corpse' 'interment' 'dead' 'burial'
 'tombs' 'catacombs' 'person deceased']
5 ['admiral' 'squadron' 'nelson' 'commander' 'fleet' 'admirals' 'commodore'
 'command' 'rodney' 'admiral vernon']
6 ['ohio' 'pennsylvania' 'maryland' 'tennessee' 'columbia' 'alleghany'
 'kentucky' 'mississippi' 'alabama' 'illinois']
7 ['lens' 'focal' 'refracting' 'lenses' 'refracted' 'achromatic' 'glasses'
 'focus' 'optical' 'magnifying']
8 ['wins' 'cards' 'player' 'ace' 'card' 'game' 'tricks' 'played' 'dice'
 'winning']
9 ['hygrometer' 'thermometer' 'atmosphere' 'evaporation' 'humidity'
 'temperature' 'barometer' 'centesimal' 'vapour' 'temperatures']
    '''
    from helpers.classifiers.base_classifier import BaseClassifier
    from helpers.corpus import Corpus
    corpus = Corpus()
    doc = corpus.read_body('eb07/TXT/a3/kp-eb0703-072101-4934-v1.xml')
    doc = '''
    It has been conjectured by Goguet, that the obelisks of Egypt were intended to serve the purpose of gnomons; and this conjecture acquires some probability from their needle-shaped form, and the narrowness of their bases relatively to their heights. It has however been proved by MM. Jollois and Devilliers, in their description of Thebes, that the obelisks were connected with the walls of temples and palaces; a disposition which rendered them entirely unfit for the purposes of astronomical observation. 
    '''
    print('\n'.join(BaseClassifier.sentencizer(doc)[:10]))

if 0:
    from helpers.classifiers.semantic_search import SemanticSearch

    semsearch = SemanticSearch()
    semsearch.convert_model_to_json(7)

if 0:
    from helpers.taxonomies import TaxonomyWikidata

    wiki = TaxonomyWikidata()
    wiki.prepare()

if 0:
    from helpers.classifiers.semantic_search import SemanticSearch
    semsearch = SemanticSearch()
    model = semsearch.load_model(7)
    print(model.get_num_topics())


if 0:
    entries = index.query()
    import pandas as pd
    # pd.set_option('display.max_columns', None)
    # pd.set_option('display.width', 1000)
    print(entries.head(1))

if 0:
    from helpers.fast import Fast
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
    from helpers.corpus import Corpus
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
    from helpers.corpus import Corpus
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

if 0:
    from helpers.samples import Samples
    samples = Samples()
    samples.load()
    print(samples.df.head())

    # print(samples.df.columns)

    index.query().column

if 0:
    # Manually CORRECT missing title in PAINTING entry
    # res = index.query('title == ""')
    # eb07/XML/p16/kp-eb0716-069301-5876-v1.xml
    index.update('eb07/XML/p16/kp-eb0716-069301-5876-v1.xml', 'title', 'PAINTING')
    index.save()
