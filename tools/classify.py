import sys
from pathlib import Path

from tqdm import tqdm
import re

project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from helpers.samples import Samples
from helpers.index import Index
index = Index()
index.load_or_create()

from helpers.corpus import Corpus
corpus = Corpus()

def test_classifier(ClassifierClass):
    classifier = ClassifierClass()

    ret = {
        'tested': 0,
        'correct': 0,
    }

    for sample in Samples.read_all():
        data = corpus.read_body_and_metadata(sample['path'])
        predicted = classifier.classify(data)
        expected = 'medicine'
        print(f'{sample["heading"]}: expected {expected}, predicted: {predicted}')
        ret['tested'] += 1
        if expected == predicted:
            ret['correct'] += 1

    return ret

from helpers.classifiers.test import Test
res = test_classifier(Test)
print(f'Tested: {res["tested"]}, Accuracy: {res["correct"] / res["tested"]}')
