from helpers import settings
from pathlib import Path
from tqdm import tqdm
import re
import json


class BaseClassifier:
    '''
    '''

    @classmethod
    def get_file_path(cls, filename=None):
        folder = Path(settings.DATA_PATH, re.sub(r'(\B[A-Z])', r'_\1', cls.__name__).lower())
        if not folder.exists():
            folder.mkdir()
        return Path(folder, filename)

    def classify(self, entry):
        raise Exception('Not implemented')

    def get_model_path(self, edition):
        return self.get_file_path(self.get_model_filename(edition))

    def get_query(self, edition):
        return f'edition=={edition}'

