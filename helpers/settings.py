from pathlib import Path

def get_path_from_top_directory(directory_name):
    ret = Path(Path(__file__).parent.parent, Path(directory_name))
    if not ret.is_dir():
        raise Exception(f'"{ret}" is not a directory')
    return ret

SUBCORPUS = ['kp-eb0901-\d+-\d+-\d+']
# sociology?, economy?, philosophy? Under history
DOMAINS = {
    'medicine': {
        'name': 'Medicine',
        'name_modern': ['medicine', 'health', 'body'],
        'desc': '',
    },
    'history': {
        'name': 'History',
        'name_modern': ['history', 'mythology', 'legend', 'religion', 'politics', 'war'],
        'desc': '"the art of imitating visible form by means of solid substances, such as marble, wood, or metals".',
    },
    'natural_philosophy': {
        'name': 'Natural Philosophy',
        'name_modern': ['physics', 'mechanics', 'optics', 'astronomy', 'magnetism', 'electricity'],
        'desc': '',
    },
    'natural_history': {
        'name': 'Natural History',
        'name_modern': ['meteorology', 'mineralogy', 'botany', 'zoology'],
        'desc': 'that part of natural knowledge which teaches us to distinguish and describe the objects of nature; to examine their appearance, structure, properties, and uses; and to collect, preserve, and arrange them',
    },
    'useful_arts': {
        'name': 'Useful Arts',
        'name_modern': ['engineer', 'craft', 'manufacturing', 'machinery', 'architecture', 'tool'],
        'desc': '"Useful Arts" is also called "Civil Engineering, Arts, and Manufactures"',
    },
    'fine_arts': {
        'name': 'Fine Arts',
        'name_modern': ['arts', 'painting', 'sculpture', 'engraving', 'dance', 'sing'],
        'desc': '"the art of imitating visible form by means of solid substances, such as marble, wood, or metals"',
    },
}

DATA_PATH = get_path_from_top_directory('data')
CORPUS_PATH = Path(DATA_PATH, Path('kp-editions'))
INDEX_PATH = Path(DATA_PATH, Path('index.json'))
SAMPLES_PATH = Path(DATA_PATH, Path('kp_sample_entries.csv'))

CUSTOM_SAMPLES = [
    {
        'heading': 'HYPOCHONDRIASIS',
        'path': 'eb09/XML/h12/kp-eb0912-059801-0613-v1.xml',
        'domain': 'medicine'
    },
    {
        'heading': 'HAMMER',
        'path': 'eb07/XML/h11/kp-eb0711-012702-0746-v1.xml',
        'domain': 'useful_arts'
    },
    {
        'heading': 'RUSSIA',
        'path': 'eb07/XML/r19/kp-eb0719-052701-0539-v1.xml',
        'domain': 'history'
    },
]