from pathlib import Path

def get_path_from_top_directory(directory_name):
    ret = Path(Path(__file__).parent.parent, Path(directory_name))
    if not ret.is_dir():
        raise Exception(f'"{ret}" is not a directory')
    return ret

SUBCORPUS = ['kp-eb0901-\d+-\d+-\d+']
DOMAINS = {
    'medicine': {
        'name': 'Medicine',
        'name_modern': 'medicine',
        'desc': '',
    },
    'history': {
        'name': 'History',
        'name_modern': 'history',
        'desc': '',
    },
    'natural_philosophy': {
        'name': 'Natural Philosophy',
        'name_modern': 'physics',
        'desc': '',
    },
    'natural_history': {
        'name': 'Natural History',
        'name_modern': 'Science',
        'desc': 'Applied Science',
    },
    'useful_arts': {
        'name': 'Useful Arts',
        'name_modern': 'manufacturing',
        'desc': 'Engineering and manufacturing',
    },
    'fine_arts': {
        'name': 'Fine Arts',
        'name_modern': 'Arts',
        'desc': '',
    },
}
DATA_PATH = get_path_from_top_directory('data')
CORPUS_PATH = Path(DATA_PATH, Path('kp-editions'))
INDEX_PATH = Path(DATA_PATH, Path('index.json'))

