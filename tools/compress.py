import sys
import re
from pathlib import Path
import json
import math

doc = ''' 
Usage: compress.py FILE DECIMALS

FILE    : the input filename, containing a dictionary of vectors
          {LABEL: [0.8, 0.4, ...], ...}
DECIMALS: number of decimals to keep in the output file (default=4)
'''

argv = sys.argv[:]
if len(argv) > 1:
    argv.pop(0)
    path_in = argv.pop(0)
    decimals = 4
    if len(argv) > 0:
        decimals = int(argv.pop(0))
    path_out = re.sub(r'(\.tv2\.json)', fr'-de_{decimals}\1', path_in)

    k = math.pow(10, decimals)

    t0 = Path(path_in).read_text()
    vectors = json.loads(t0)

    for label, v in vectors.items():
        vectors[label] = [int(c*k) for c in v]

    t1 = json.dumps(vectors, separators=(',', ':'))
    Path(path_out).write_text(t1)

    print(f'done ({len(t0)/1024/1024}MB -> {len(t1)/1024/1024}MB {path_out})')

else:
    print(doc)
