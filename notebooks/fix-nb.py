import nbformat

nb_path = 'ld_tests'

with open(f'{nb_path}.ipynb', 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)
with open(f'{nb_path}-fixed.ipynb', 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)
