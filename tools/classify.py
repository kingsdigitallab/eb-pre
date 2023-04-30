import sys
from pathlib import Path
from tqdm import tqdm
import re

project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from helpers import settings
from helpers.samples import Samples
from helpers.corpus import Corpus
from helpers.index import Index
index = Index()
index.load_or_create()

corpus = Corpus()

def test_classifier(ClassifierClass):
    ret = {
        'tested': 0,
        'correct': 0,
    }

    classifier = ClassifierClass()

    for sample in Samples.read_all():
        data = corpus.read_body_and_metadata(sample['path'])
        predicted = classifier.classify(data)
        expected = sample['domain'].lower().strip()
        print(f'{sample["heading"]}: expected: {expected}, predicted: {predicted}')
        ret['tested'] += 1
        if expected == predicted:
            ret['correct'] += 1

        if sample['domain'] not in settings.DOMAINS:
            print(f'Domain not found in index: {sample["domain"]}')

    return ret


# from helpers.classifiers.test import Test as Classifier
from helpers.classifiers.semantic_search import SemanticSearch as Classifier
res = test_classifier(Classifier)
print(f'{Classifier.__name__} - Tested: {res["tested"]}, Accuracy: {res["correct"] / res["tested"]}')
