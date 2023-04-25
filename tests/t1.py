import sys
from pathlib import Path

from tqdm import tqdm

project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from tools.index import Index
index = Index()
index.load_or_create()
# index.create()

def compute_linguistic_properties():
    from lexicalrichness import LexicalRichness

    # index.df['chars'] = 0

    query = 'edition == 9 and volume == 1'
    query = None

    for aid in tqdm(index.query(query).index):
        # item = index.df.loc[aid]
        text = index.corpus.read_body(aid)
        lex = LexicalRichness(text)
        # print(len(text))
        vocd = msttr = 0
        try:
            vocd = lex.vocd(within_sample=100)
        except ValueError:
            pass
        try:
            msttr = lex.msttr(segment_window=25)
        except ValueError:
            pass
        chars = len(text)
        # print(lex.words, lex.terms, vocd)
        index.update(aid, 'chars', chars)
        index.update(aid, 'vocd', vocd)
        index.update(aid, 'msttr', msttr)

    index.save()

# compute_linguistic_properties()
if 0:
    from tools.fast import Fast
    fast = Fast()
    fast.load()
    # fast.getParents('')

if 1:
    eds_titles = {}
    for ed in [7, 9]:
        eds_titles[ed] = set(index.query(f'edition=={ed}')['title'])

    print(f'Same titles: {len(eds_titles[7].intersection(eds_titles[9]))}')

if 0:
    import os
    os.environ['TF_ENABLE_ONEDNN_OPTS'] = "0"
    os.environ['CUDA_VISIBLE_DEVICES'] = "-1"

    from top2vec import Top2Vec

    aids = [
        'eb09/XML/h12/kp-eb0912-060001-0615-v1.xml'
    ]
    from tools.corpus import Corpus
    corpus = Corpus()
    documents = []
    for aid in tqdm(index.query('edition==9').index):
    # for aid in tqdm(index.query('edition==9').index):
        body = corpus.read_body(aid)
        if len(body) > 10:
            documents.append(body)

    embedding_model = 'doc2vec'

    model = Top2Vec(
        documents,
        # embedding_model='universal-sentence-encoder', # POOR results
        embedding_model=embedding_model,
        speed='deep-learn',
        embedding_batch_size=16, # 32
        use_embedding_model_tokenizer=True,
        workers=10,
    )

    model.save(str(Path(project_path, "data", "models", f'{embedding_model}-9')))

    num_topics = model.get_num_topics()
    print(len(documents), num_topics)

    res = model.get_topics(min(num_topics, 10))
    for i in range(len(res[0])):
        print(res[0][i][:8])

    documents, document_scores, document_ids = model.search_documents_by_keywords(
        keywords=["medical"],
        num_docs=20
    )
    for doc, score, doc_id in zip(documents, document_scores, document_ids):
        print(f"Document: {doc_id}, Score: {score}")
        print("-----------")
        print(doc[:300])
        print("-----------")
        print()