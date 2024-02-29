# %%
import sys
import os
from collections import Counter
import re
from pathlib import Path
parent_path = str(Path(__file__).parent.parent)
sys.path.append(parent_path)

from helpers import settings

domains = settings.DOMAINS

from helpers.index import Index
index = Index()
index.load()

from helpers.corpus import Corpus
corpus = Corpus()

from tqdm import tqdm

# %%

patterns = {
    'in_x': {
        'regex': r'^[^,]{3,30}, in ([^,.]{3,30})[,.]'
    }
}

for p in patterns.values():
    p['groups'] = Counter()

query = 'edition == 7'
query = ''
for aid in tqdm(index.query(query).index):
    body = corpus.read_body(aid)
    for pattern_key, pattern in patterns.items():
        occurrences = re.findall(pattern['regex'], body)
        if occurrences:
            pattern['groups'].update([o.lower() for o in occurrences])
            if pattern_key == 'in_x':
                index.update(aid, pattern_key, occurrences[0].lower())

index.save()

print(patterns)

print('done')

# %%



