from . import settings
from .corpus import Corpus
import pandas as pd
from tqdm import tqdm


class Index:
    def __init__(self):
        self.corpus = Corpus()
        self.df = None

    def load(self):
        self.df = None
        if settings.INDEX_PATH.exists():
            self.df = pd.read_json(settings.INDEX_PATH.read_text(), orient='table')

    def query(self, q=None):
        ret = self.df
        if q:
            ret = ret.query(q)
        # print(f'{len(ret)} entries for query = {q}')
        return ret

    def create(self):
        """Indexes the title and edition of all articles in the corpus.
        And saves the index as a json file."""
        ids = list(self.corpus.read_ids())
        titles = len(ids) * [None]
        editions = len(ids) * [None]
        volumes = len(ids) * [None]
        pages = len(ids) * [None]
        labels = len(ids) * [None]
        refs = len(ids) * [None]

        for i, aid in tqdm(enumerate(ids)):
            parts = self.corpus.decode_id(aid)
            # print(parts)
            editions[i] = parts['edition']
            volumes[i] = parts['volume']
            pages[i] = parts['page']

            parts = self.corpus.read_metadata(aid)
            titles[i] = parts['title']
            labels[i] = [t['label'] for t in parts['terms']]
            refs[i] = [t['ref'] for t in parts['terms']]

        self.df = pd.DataFrame({
            'edition': editions,
            'volume': volumes,
            'page': pages,
            'title': titles,
            'labels': labels,
            'refs': refs,
        }, index=ids)

        # print(self.df.head(3))

        # self.corpus.read_body(self.df.index[0])

        self.save()

    def save(self):
        """Saves the index in a json file."""
        settings.INDEX_PATH.write_text(self.df.to_json(orient='table'))

    def load_or_create(self):
        self.load()
        if self.df is None:
            self.create()

    def update(self, aid, column, value):
        self.df.at[aid, column] = value
