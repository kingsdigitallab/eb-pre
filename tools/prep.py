import sys
from pathlib import Path

from tqdm import tqdm
import re

project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from helpers.index import Index
index = Index()
index.load_or_create()

def index_linguistic_properties(query=None):
    '''
    Calculate linguistic properties of entries and add them to the index.
    query is a panda query over the index, which entries should be processed.
        query = 'edition == 9 and volume == 1'
    Takes ~30 mins for 2 editions.
    '''
    from helpers import nlp

    for aid in tqdm(index.query(query).index):
        # item = index.df.loc[aid]
        text = index.corpus.read_body(aid)
        props = nlp.compute_linguistic_properties(text)

        for k, v in props.items():
            index.update(aid, k, v)

    index.save()

if 1:
    index_linguistic_properties()

if 0:
    import re
    from helpers.samples import Samples

    samples = Samples()
    samples.load()
    for i, sample in samples.df.iterrows():
        print(sample['path'])


