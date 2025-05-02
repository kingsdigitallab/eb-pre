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
        folder = Path(settings.DATA_PATH, cls.get_class_key())
        if not folder.exists():
            folder.mkdir()
        return Path(folder, filename)

    @classmethod
    def get_class_key(cls):
        return re.sub(r'(\B[A-Z])', r'_\1', cls.__name__).lower()

    def before_classify(self, edition):
        pass

    def classify(self, entry):
        raise Exception('Not implemented')

    def get_model_path(self, edition):
        return self.get_file_path(self.get_model_filename(edition))

    def get_query(self, edition):
        return f'edition=={edition}'

    def get_params(self):
        ret = {
            'classifier': self.__class__.__name__,
        }
        return ret

    def get_params_str(self):
        return ', '.join([f'{p}={v}' for p, v in self.get_params().items()])

    @classmethod
    def sentencizer(cls, doc):
        # returns the list of sentences extracted from the given doc
        # method: split around . and ;
        # but don't split around . if preceded by uppercase letter (e.g. MR.)
        return [
            p.strip() 
            for p
            in re.split(r'(?:[^A-Z])\.|;|\?|!', doc)
        ]

    