import argparse
import sys
from pathlib import Path

import pandas as pd

project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from helpers import settings

DATA_PATH = settings.DATA_PATH
INDEX_FILENAME = 'index.json'
DOMAIN_LABEL_COLUMN = 'semantic_search-label'
SCORE_COLUMN = 'semantic_search-score'
EXCLUDED_EDITION = 9
DEFAULT_TOP = 5


def get_domain_order(variant: str, df: pd.DataFrame) -> list:
    '''Return domain keys for the variant, ordered by settings if defined, else from the index.'''
    ret = []
    data_domains = set(df[DOMAIN_LABEL_COLUMN].dropna().unique())
    if variant in settings.DOMAINS_SETS:
        ret = [d for d in settings.DOMAINS_SETS[variant].keys() if d in data_domains]
    ret += sorted(data_domains - set(ret))
    return ret


def top_entries_for_domain(df: pd.DataFrame, domain: str, n: int) -> pd.DataFrame:
    '''Return the n highest-scoring entries classified into the given domain.'''
    ret = df[df[DOMAIN_LABEL_COLUMN] == domain].nlargest(n, SCORE_COLUMN)
    return ret[['title', SCORE_COLUMN]]


def list_top_entries(variant: str, n: int, data_path: Path):
    '''Print the top n entries per domain for the given variant index.'''
    path = Path(data_path, variant, INDEX_FILENAME)
    if not path.exists():
        print(f'ERROR: no index found for variant "{variant}" at {path}')
        return
    df = pd.read_json(path, orient='table')
    df = df[df['edition'] != EXCLUDED_EDITION]
    for domain in get_domain_order(variant, df):
        top = top_entries_for_domain(df, domain, n)
        print(domain)
        titles = top['title'].tolist()
        width = max((len(t) for t in titles), default=0)
        for i, (title, score) in enumerate(zip(titles, top[SCORE_COLUMN].tolist()), 1):
            print(f'  {i}. {title:<{width}}  {score:.3f}')
        print()


def main():
    parser = argparse.ArgumentParser(description='List the top entries per domain for a given variant.')
    parser.add_argument('variant', help='Variant name, e.g. 2026-07-19')
    parser.add_argument('-n', '--top', type=int, default=DEFAULT_TOP, help='Number of top entries per domain (default 5)')
    args = parser.parse_args()
    list_top_entries(args.variant, args.top, DATA_PATH)


if __name__ == '__main__':
    main()
