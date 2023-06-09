import pandas as pd
from helpers import settings
import re

class Samples:
    '''
    Loads sample entries from CSV file into a pandas dataframe.
    Columns:
        domain  = medicine
        heading = MEDICAL JURISPRUDENCE
        path    = eb07/XML/m14/kp-eb0714-049001-6192-v1.xml
    '''

    def load(self):
        self.df = None
        path = settings.SAMPLES_PATH
        if path.exists():
            self.df = pd.read_csv(path)
            self.df = self.df.rename(columns={'entry term': 'heading'})
            self.df = self.df[self.df['heading'].notnull()]
            self.df['path'] = self.df['URI'].apply(lambda uri: re.sub(r'^.*/main/', '', uri))
            self.df['domain'] = self.df['domain'].apply(lambda domain: re.sub(r'\W+', '_', domain.lower().strip()))

    def add_custom_samples(self):
        samples = pd.DataFrame(settings.CUSTOM_SAMPLES)
        self.df = pd.concat([self.df, samples], ignore_index=True)

    def get_all(self):
        return [row for i, row in self.df.iterrows()]

    @classmethod
    def read_all(cls):
        samples = cls()
        samples.load()
        samples.add_custom_samples()
        return samples.get_all()

