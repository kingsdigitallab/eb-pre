import re
import sys
from collections import Counter
from pathlib import Path

from tqdm import tqdm

project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from helpers.index import Index
from helpers.corpus import Corpus


def index_linguistic_properties(index, query=None):
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


def index_in_x(index, query=None):
    '''
    Extract patterns like ", in geography" 
    from the start of an entry 
    and add geography to the index
    '''
    corpus = Corpus()
  
    patterns = {
        'in_x': {
            'regex': r'^[^,]{3,30}, in ([^,.]{3,30})[,.]'
        }
    }

    for p in patterns.values():
        p['groups'] = Counter()

    for aid in tqdm(index.query(query).index):
        body = corpus.read_body(aid)
        for pattern_key, pattern in patterns.items():
            occurrences = re.findall(pattern['regex'], body)
            if occurrences:
                pattern['groups'].update([o.lower() for o in occurrences])
                if pattern_key == 'in_x':
                    # print(occurrences[0].lower())
                    index.update(aid, pattern_key, occurrences[0].lower())

    index.save()

def main():
    index = Index()
    index.load_or_create()

    if 0:
        # takes 30 mins
        print('COMPUTE lexical diversity of every entry and add it to the index')
        index_linguistic_properties(index)

    if 1:
        # takes 2 secs
        print('COMPUTE in_x property of every entry and add it to the index')
        index_in_x(index)

    print('DONE')

main()

# if 0:
#     from helpers.samples import Samples

#     samples = Samples()
#     samples.load()
#     for i, sample in samples.df.iterrows():
#         print(sample['path'])


