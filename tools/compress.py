import sys
from pathlib import Path

project_path = Path(__file__).parent.parent
sys.path.append(str(project_path))

from helpers.classifiers.semantic_search import SemanticSearch

doc = ''' 
Usage: compress.py FILE DECIMALS

FILE    : the input filename, containing a dictionary of vectors
          {LABEL: [0.8, 0.4, ...], ...}
DECIMALS: number of decimals to keep in the output file (default=2)
'''

argv = sys.argv[:]
if len(argv) > 1:
    argv.pop(0)
    path_in = argv.pop(0)
    decimals = 2
    if len(argv) > 0:
        decimals = int(argv.pop(0))

    classifier = SemanticSearch()
    classifier.compress_embedding_file(path_in, decimals)

else:
    print(doc)
