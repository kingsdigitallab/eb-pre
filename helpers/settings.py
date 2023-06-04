from pathlib import Path

def get_path_from_top_directory(directory_name):
    ret = Path(Path(__file__).parent.parent, Path(directory_name))
    if not ret.is_dir():
        raise Exception(f'"{ret}" is not a directory')
    return ret

# sociology?, economy?, philosophy? Under history
DOMAINS = {
    'medicine': {
        'name': 'Medicine',
        'name_modern': ['medicine', 'health', 'body'],
        'fast': ['medicine', 'human biology'],
        'desc': '',
    },
    'history': {
        'name': 'History',
        'name_modern': ['history', 'mythology', 'legend', 'religion', 'politics', 'war'],
        'fast': ['history'],
        'desc': 'Includes biblical history of the earth and growth of society under "Civil History". See also entries on countries, like RUSSIA--these are generally histories.',
    },
    'natural_philosophy': {
        'name': 'Natural Philosophy',
        'name_modern': ['physics', 'mechanics', 'optics', 'astronomy', 'magnetism', 'electricity'],
        'fast': ['physics'],
        'desc': 'Similar to Physics. "NATURAL PHILOSOPHY is commonly defined to be that branch of knowledge which considers the powers and properties of natural bodies, and their mutual actions on one another. This term serves to indicate, not one, but a cluster of sciences. Those generally comprehended under it are the following, viz. 1. Mechanics; 2. Hydrostatics; 3. Optics; 4. Astronomy; 5. Magnetism; 6. Electricity." (kp-eb0715-8829-0740-01)',
    },
    'natural_history': {
        'name': 'Natural History',
        'name_modern': ['meteorology', 'mineralogy', 'botany', 'zoology'],
        'fast': ['biology', 'life science', 'earth sciences', 'natural history'],
        'desc': 'that part of natural knowledge which teaches us to distinguish and describe the objects of nature; to examine their appearance, structure, properties, and uses; and to collect, preserve, and arrange them',
    },
    'useful_arts': {
        'name': 'Useful Arts',
        'name_modern': ['engineer', 'craft', 'manufacturing', 'machinery', 'architecture', 'tool'],
        'fast': ['hardware', 'industries'],
        'desc': '"Useful Arts" is also called "Civil Engineering, Arts, and Manufactures"',
    },
    'fine_arts': {
        'name': 'Fine Arts',
        'name_modern': ['arts', 'painting', 'sculpture', 'engraving', 'dance', 'sing'],
        'fast': [''],
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

CUSTOM_SAMPLES += [
    {
        'heading': 'NAMUR',
        'path': 'eb07/XML/n15/kp-eb0715-068902-8166-v1.xml',
        'domain': 'history'
    },
    {
        'heading': 'MILAN',
        'path': 'eb07/XML/m15/kp-eb0715-006306-0028-v1.xml',
        'domain': 'history'
    },
    {
        'heading': 'OEDIPUS',
        'path': 'eb07/XML/o16/kp-eb0716-032407-1077-v1.xml',
        'domain': 'history'
    },
    {
        'heading': 'PLAGUE',
        'path': 'eb07/XML/p17/kp-eb0717-077207-1123-v1.xml',
        'domain': 'medicine'
    },
    {
        'heading': 'SYMPHONY',
        'path': 'eb07/XML/s21/kp-eb0721-005309-0071-v1.xml',
        'domain': 'fine_arts'
    },
    {
        'heading': 'REFRACTION',
        'path': 'eb07/XML/r19/kp-eb0719-009701-0107-v1.xml',
        'domain': 'natural_philosophy'
    },
    {
        'heading': 'FRICTION',
        'path': 'eb07/XML/f10/kp-eb0710-023209-6983-v1.xml',
        'domain': 'natural_philosophy'
    }
]
