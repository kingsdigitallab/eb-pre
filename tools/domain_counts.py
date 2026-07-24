import sys
from pathlib import Path
from collections import Counter

import pandas as pd

project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from helpers import settings

DATA_PATH = settings.DATA_PATH
INDEX_FILENAME = 'index.json'
DOMAIN_LABEL_COLUMN = 'semantic_search-label'
EXCLUDED_EDITION = 9


def get_variants(data_path: Path) -> list:
    '''Return the sorted names of data subdirectories that contain an index.json.'''
    ret = []
    for path in sorted(data_path.iterdir()):
        if path.is_dir() and (path / INDEX_FILENAME).exists():
            ret.append(path.name)
    return ret


def count_domains(variant: str, data_path: Path) -> Counter:
    '''Count non-9th-edition entries per domain for the given variant index.'''
    ret = Counter()
    path = Path(data_path, variant, INDEX_FILENAME)
    df = pd.read_json(path, orient='table')
    df = df[df['edition'] != EXCLUDED_EDITION]
    for domain, n in df[DOMAIN_LABEL_COLUMN].value_counts().items():
        ret[domain] = n
    return ret


def build_table(data_path: Path) -> pd.DataFrame:
    '''Build a variants x domains count table across all variant indexes.'''
    ret = pd.DataFrame()
    rows = {}
    for variant in get_variants(data_path):
        rows[variant] = count_domains(variant, data_path)
    ret = pd.DataFrame(rows).T.fillna(0).astype(int)
    preferred = list(settings.DOMAINS.keys())
    columns = [c for c in preferred if c in ret.columns]
    columns += sorted(c for c in ret.columns if c not in preferred)
    ret = ret[columns].sort_index()
    return ret


def main():
    table = build_table(DATA_PATH)
    print(table.to_string())


if __name__ == '__main__':
    main()
