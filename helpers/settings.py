from pathlib import Path

def get_path_from_top_directory(directory_name):
    ret = Path(Path(__file__).parent.parent, Path(directory_name))
    if not ret.is_dir():
        raise Exception(f'"{ret}" is not a directory')
    return ret

# sociology?, economy?, philosophy? Under history
DOMAINS_SETS = {
    '2025-06-05': {
        # Memory
        'sacred_history': {
            'name': 'Sacred History',
            'name_modern': ['ecclesiastical', 'prophet', 'SACRED'],
        },
        'civil_history': {
            'name': 'Civil History',
            'name_modern': ['antiquities', 'civilization', 'CHRONICLE', 'historian', 'MEMOIRS', 'STATISTICS'],
        },
        'natural_history': {
            'name': 'Natural History',
            'name_modern': ['ANIMAL KINGDOM', 'BOTANY', 'celestial', 'METEOR', 'monsters', 'MINERALOGY',
                            'NATURAL HISTORY',
                            'PHYSICAL GEOGRAPHY', 'wonders'],
        },
        'useful_arts': {
            'name': 'Useful Arts',
            'name_modern': ['FORGE', 'GLASS', 'goldsmith', 'handicraft', 'LAPIDARY', 'manufacture', 'masonry', 'mills',
                            'skins',
                            'WEAVING'],
        },
        # Reason
        'theology': {
            'name': 'Theology',
            'name_modern': ['demons', 'DIVINATION', 'religion', 'SUPERSTITION', 'THEOLOGY'],
        },
        'philosophy': {
            'name': 'Philosophy',
            'name_modern': ['ETHICS', 'GRAMMAR', 'ideas', 'INDUCTION', 'LEGISLATION', 'logic', 'MEMORY', 'PRINTING',
                            'PROPOSITION',
                            'RHETORIC', 'SOUL', 'syllogism', 'WRITING'],
        },
        'natural_philosophy': {
            'name': 'Natural Philosophy',
            'name_modern': ['ARITHMETIC', 'ASTRONOMY', 'DYNAMICS', 'ELECTRICITY', 'GEOMETRY', 'OPTICS', 'PNEUMATICS',
                            'POLITICAL ECONOMY', 'PROBABILITY', 'STATICS', 'anatomy',
                            'ANGLING, or the art of fishing with rod and line', 'ATMOSPHERE', 'BOTANY', 'CHEMISTRY',
                            'COSMOLOGY', 'HORSEMANSHIP', 'HYDRODYNAMICS', 'METEOROLOGY', 'MINERALOGY', 'ORNITHOLOGY',
                            'PHYSIC, PRACTICE OF', 'PHYSIOLOGY', 'veterinary medicine'],
        },
        # Imagination
        'fine_arts': {
            'name': 'Fine Arts',
            'name_modern': ['ARCHITECT', 'DRAMA', 'ENGRAVING', 'MUSIC', 'novel', 'PAINTING', 'POETRY', 'SCULPTURE'],
        },
    },
    # Received 2025-04-14
    '2025-04-30': {
        # Memory
        'sacred_history': {
            'name': 'Sacred History',
            'name_modern': ['ecclesiastical history', 'divine', 'SACRED', 'scriptures'],
        },
        'civil_history': {
            'name': 'Civil History',
            'name_modern': ['civilization', 'CHRONICLE', 'died', 'historian', 'kingdom', 'wars'],
        },
        'natural_history': {
            'name': 'Natural History',
            'name_modern': [
                'astronomer', 'chemists', 'geographers', 'geologists', 'NATURAL HISTORY', 
                'monsters', 'wonders',
                'city', 'inhabitants', 'mountains', 'river'
            ],
        },
        'useful_arts': {
            'name': 'Useful Arts',
            'name_modern': ['DAIRY', 'engineers', 'FURNACE', 'handicraft', 'masonry', 'mills', 'roads', 'SEAMANSHIP', 'ware', 'WEAVING'],
        },
        # Reason
        'theology': {
            'name': 'Theology',
            'name_modern': ['creator', 'DIVINATION', 'ETERNITY', 'revelation', 'SUPERSTITION', 'THEOLOGY'],
        },
        'philosophy': {
            'name': 'Philosophy',
            'name_modern': ['ETHICS', 'induction', 'LEGISLATION', 'logic', 'GRAMMAR', 'PERCEPTION', 'PHILOLOGY'],
        },
        'natural_philosophy': {
            'name': 'Natural Philosophy',
            'name_modern': [
                'ALGEBRA', 'ARITHMETIC', 'ASTRONOMY', 'ELECTRICITY', 'GEOMETRY', 'OPTICS', 'POLITICAL ECONOMY', 'MAGNETISM', 'QUANTITY', 'STATICS',
                'BOTANY', 'CHEMISTRY', 'METEOROLOGY', 'PHYSIC, PRACTICE OF', 'PHYSIOLOGY', 'ZOOLOGY'
            ],
        },
        # Imagination
        'fine_arts': {
            'name': 'Fine Arts',
            'name_modern': ['ARCHITECT', 'DANCE, or Dancing', 'DRAMA', 'ENGRAVING', 'MUSIC', 'PAINTING', 'POETRY', 'SCULPTURE'],
        },
    },
    '2024-07-09-fixed': {
        'sacred_history': {
            'name': 'Sacred History',
            'name_modern': ['ecclesiastical history', 'divine', 'SACRED', 'scriptures', 'superstition'],
        },
        'civil_history': {
            'name': 'Civil History',
            'name_modern': ['annals', 'civilization', 'died', 'historian', 'wars'],
        },
        'natural_history': {
            'name': 'Natural History',
            'name_modern': [
                'astronomer', 'chemists', 'geographers', 'geologists', 'NATURAL HISTORY', 
                'monsters', 'wonders',
                'city', 'inhabitants', 'mountains', 'river'
            ],
        },
        'useful_arts': {
            'name': 'Useful Arts',
            'name_modern': ['DAIRY', 'engineers', 'FURNACE', 'handicraft', 'hydrostatics', 'masonry', 'mills', 'roads', 'SEAMANSHIP', 'ware', 'WEAVING'],
        },
        'theology': {
            'name': 'Theology',
            'name_modern': ['DIVINATION', 'SUPERSTITION', 'THEOLOGY'],
        },
        'philosophy': {
            'name': 'Philosophy',
            'name_modern': ['ETHICS', 'induction', 'laws', 'logic', 'GRAMMAR', 'MEMORY'],
        },
        'natural_philosophy': {
            'name': 'Natural Philosophy',
            'name_modern': [
                'ARITHMETIC', 'ASTRONOMY', 'ELECTRICITY', 'GEOMETRY', 'mechanics', 'OPTICS', 'POLITICAL ECONOMY',
                'BOTANY', 'CHEMISTRY', 'medicine', 'METEOROLOGY', 'PHYSICS', 'PHYSIOLOGY', 'ZOOLOGY'
            ],
        },
        'fine_arts': {
            'name': 'Fine Arts',
            'name_modern': ['ARCHITECT', 'DANCE, or Dancing', 'DRAMA', 'ENGRAVING', 'MUSIC', 'PAINTING', 'POETRY', 'SCULPTURE'],
        },
    },
    '2024-07-09-bugged': {
        'sacred_history': {
            'name': 'Sacred History',
            'name_modern': ['ecclesiastical history', 'divine', 'sacred', 'scriptures', 'superstition'],
        },
        'civil_history': {
            'name': 'Civil History',
            'name_modern': ['annals', 'civilization', 'died', 'historian', 'wars'],
        },
        'natural_history': {
            'name': 'Natural History',
            'name_modern': [
                'astronomer', 'chemists', 'geographers', 'geologists', 'natural history', 
                'monsters', 'wonders',
                'city', 'inhabitants', 'mountains', 'river'
            ],
        },
        'useful_arts': {
            'name': 'Useful Arts',
            'name_modern': ['dairy', 'engineers', 'furnace', 'handicraft', 'hydrostatics', 'masonry', 'mills', 'roads', 'seamanship', 'ware', 'weaving'],
        },
        'theology': {
            'name': 'Theology',
            'name_modern': ['divination', 'superstition', 'theology'],
        },
        'philosophy': {
            'name': 'Philosophy',
            'name_modern': ['ethics', 'induction', 'laws', 'logic', 'grammar', 'memory'],
        },
        'natural_philosophy': {
            'name': 'Natural Philosophy',
            'name_modern': [
                'arithmetic', 'astronomy', 'electricity', 'geometry', 'mechanics', 'optics', 'political economy',
                'botany', 'chemistry', 'medicine', 'meteorology', 'physics', 'physiology', 'zoology'
            ],
        },
        'fine_arts': {
            'name': 'Fine Arts',
            'name_modern': ['architect', 'dance', 'drama', 'engraving', 'music', 'painting', 'poetry', 'sculpture'],
        },
    },
    '2023': {
        'medicine': {
            'name': 'Medicine',
            'path': 'eb09/XML/m15/kp-eb0915-079401-0825-v1.xml', # not in 7!
            'name_modern': ['medicine', 'medical', 'health'],
            'fast': ['medicine', 'human biology'],
            'desc': '',
        },
        'history': {
            'name': 'History',
            'path': 'eb07/XML_V2/h11/kp-eb0711-046904-5192-v2.xml',
            'name_modern': ['history', 'mythology', 'legend', 'religion', 'society', 'war', 'biography'],
            'fast': ['history'],
            'desc': 'Includes biblical history of the earth and growth of society under "Civil History". See also entries on countries, like RUSSIA--these are generally histories.',
            # See 7.History: But that which chiefly merits the name of history, and which is here considered as such, is an account of the principal transactions of mankind since the beginning of the world; and this is naturally divided into two parts, civil and ecclesiastical
        },
        'natural_philosophy': {
            'name': 'Natural Philosophy',
            'path': 'eb07/XML_V2/n15/kp-eb0715-074001-8829-v2.xml',
            'name_modern': ['physics', 'mechanics', 'optics', 'astronomy', 'magnetism', 'electricity'],
            'fast': ['physics'],
            'desc': 'Similar to Physics. "NATURAL PHILOSOPHY is commonly defined to be that branch of knowledge which considers the powers and properties of natural bodies, and their mutual actions on one another. This term serves to indicate, not one, but a cluster of sciences. Those generally comprehended under it are the following, viz. 1. Mechanics; 2. Hydrostatics; 3. Optics; 4. Astronomy; 5. Magnetism; 6. Electricity." (kp-eb0715-8829-0740-01)',
        },
        'natural_history': {
            'name': 'Natural History',
            'path': 'eb07/XML_V2/n15/kp-eb0715-073804-8803-v2.xml',
            'name_modern': ['meteorology', 'mineralogy', 'botany', 'zoology'], # 'hydrography': not enough occurrences
            'fast': ['biology', 'life science', 'earth sciences', 'natural history'],
            'desc': 'that part of natural knowledge which teaches us to distinguish and describe the objects of nature; to examine their appearance, structure, properties, and uses; and to collect, preserve, and arrange them',
            # See 7.History: "to this day the descriptions of plants, animals, and minerals, are called by the general name of Natural History"
        },
        'useful_arts': {
            'name': 'Useful Arts',
            'path': 'eb09/XML/a2/kp-eb0902-063601-0697-v1.xml', # !! = "art" = Useful + Fine Arts
            # engineering only 62 times in ed7 => construction instead
            'name_modern': ['goods', 'cotton', 'machinery', 'manufacture', 'construction'], # textile does not appear in edition 7 => cotton & goods
            'fast': ['hardware', 'industries'],
            'desc': '"Useful Arts" is also called "Civil Engineering, Arts, and Manufactures"',
        },
        'fine_arts': {
            'name': 'Fine Arts',
            'path': 'eb09/XML/f9/kp-eb0909-019401-0203-v1.xml', # not in 7!
            'name_modern': ['poetry', 'painting', 'sculpture', 'engraving', 'dance', 'music'],
            'fast': [''],
            'desc': '"the art of imitating visible form by means of solid substances, such as marble, wood, or metals"',
        },
    }
}

# DOMAINS_SET = '2023'
# DOMAINS_SET = '2024-07-09' # becomes '2024-07-09-bugged'
# DOMAINS_SET = '2024-07-09-bugged'
# DOMAINS_SET = '2024-07-09-fixed'
# DOMAINS_SET = '2025-04-30'
DOMAINS_SET = '2025-06-05'
DOMAINS = DOMAINS_SETS[DOMAINS_SET]


DATA_PATH = get_path_from_top_directory('data')
CORPUS_PATH = Path(DATA_PATH, Path('kp-editions'))
INDEX_PATH = Path(DATA_PATH, DOMAINS_SET, Path('index.json'))
SAMPLES_PATH = Path(DATA_PATH, Path('kp_sample_entries.csv'))

UNNAMED_ENTRY = 'UNNAMED ENTRY'

CUSTOM_SAMPLES = [
    {
        'heading': 'HYPOCHONDRIASIS',
        'path': 'eb09/XML/h12/kp-eb0912-059801-0613-v1.xml',
        'domain': 'medicine'
    },
    {
        'heading': 'HAMMER',
        'path': 'eb07/XML_V2/h11/kp-eb0711-012702-0746-v2.xml',
        'domain': 'useful_arts'
    },
    {
        'heading': 'RUSSIA',
        'path': 'eb07/XML_V2/r19/kp-eb0719-052701-0539-v2.xml',
        'domain': 'history'
    },
]

CUSTOM_SAMPLES += [
    {
        'heading': 'NAMUR',
        'path': 'eb07/XML_V2/n15/kp-eb0715-068902-8166-v2.xml',
        'domain': 'history'
    },
    {
        'heading': 'MILAN',
        'path': 'eb07/XML_V2/m15/kp-eb0715-006306-0028-v2.xml',
        'domain': 'history'
    },
    {
        'heading': 'OEDIPUS',
        'path': 'eb07/XML_V2/o16/kp-eb0716-032407-1077-v2.xml',
        'domain': 'history'
    },
    {
        'heading': 'PLAGUE',
        'path': 'eb07/XML_V2/p17/kp-eb0717-077207-1123-v2.xml',
        'domain': 'medicine'
    },
    {
        'heading': 'SYMPHONY',
        'path': 'eb07/XML_V2/s21/kp-eb0721-005309-0071-v2.xml',
        'domain': 'fine_arts'
    },
    {
        'heading': 'REFRACTION',
        'path': 'eb07/XML_V2/r19/kp-eb0719-009701-0107-v2.xml',
        'domain': 'natural_philosophy'
    },
    {
        'heading': 'FRICTION',
        'path': 'eb07/XML_V2/f10/kp-eb0710-023209-6983-v2.xml',
        'domain': 'natural_philosophy'
    }
]
