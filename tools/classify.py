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
        'classifier': None,
    }

    classifier = ClassifierClass()
    ret['classifier'] = classifier

    for sample in Samples.read_all():
        print('-'*40)

        if 'eb07' in sample['path']:
            sample['path'] = sample['path'].replace('eb07/XML/', 'eb07/XML_v2/').replace('-v1.', '-v2.').replace('eb07/XML_V2/', 'eb07/XML_v2/')
        else:
            continue

        data = corpus.read_body_and_metadata(sample['path'])
        predicted = classifier.classify(data)
        expected = sample['domain'].lower().strip()
        ret['tested'] += 1
        status = 'SAME'
        if expected == predicted:
            ret['correct'] += 1
        else:
            status = 'DIFF'

        print(f'{status} {sample["heading"]}: expected: {expected}, predicted: {predicted}')

        if sample['domain'] not in settings.DOMAINS:
            print(f'Domain not found in index: {sample["domain"]}')

    return ret


def classify_corpus(ClassifierClass, edition=7):
    classifier = ClassifierClass()

    print(classifier.get_model_filename(7))

    for aid, entry in tqdm(index.query(f'edition == {edition}').iterrows()):
        entry = index.get_dict_from_entry(entry)
        entry['aid'] = aid
        scores = []
        domain = classifier.classify(entry, scores)
        # print(entry['title'], domain)
        index.update(aid, f'{ClassifierClass.get_class_key()}-label', scores[0][0])
        index.update(aid, f'{ClassifierClass.get_class_key()}-score', scores[0][1])

    index.save()

# from helpers.classifiers.test import Test as Classifier
# from helpers.classifiers.subjects_taxonomy import SubjectsTaxonomy as Classifier
# from helpers.classifiers.title_taxonomy import TitleTaxonomy as Classifier
# from helpers.classifiers.zero_shot import ZeroShot as Classifier
# from helpers.classifiers.guided_topics import GuidedTopics as Classifier
from helpers.classifiers.semantic_search import SemanticSearch as Classifier
from datetime import datetime
if 0:
    print(f'{Classifier.__name__} - {datetime.now().ctime()}')
    print('='*40)
    res = test_classifier(Classifier)
    print('-'*40)
    print(res['classifier'].get_params_str())
    print(f'Accuracy: {int(res["correct"] / res["tested"] * 100)}% = {res["correct"]} / {res["tested"]}')
else:
    classify_corpus(Classifier)
