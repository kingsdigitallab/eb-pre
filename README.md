[Experimental prototypes](https://kingsdigitallab.github.io/eb-pre/) based on the dataset produced by the [Nineteenth-Century Knowledge Project](https://tu-plogan.github.io/source/c_about.html) led by Peter M. Logan.

[Documentation](https://github.com/kingsdigitallab/eb-pre/wiki)

## How to reproduce this proof of concept?

To reproduce the POC from this repository and the corpus.

### get the code & data
1. create a new folder poc
2. clone this repository into poc/eb-pre
3. clone the Encyclopedia repository in a separate folder poc/kp-editions

### link the data into the code base

4. `cd poc/eb-pre/data`
5. `ln -s ../../kp-editions`

And remove superseded copies of the encyclopedia entries:

6. `rm -rf kp-editions/eb07/TXT/ kp-editions/eb07/XML/`

## create & active the python environment

7. `cd poc/eb-pre`
8. `python3 -m venv venv`
9. `source venv/bin/activate`
10. `pip install -U pip`
11. `pip install build/requirements.txt`

## (re-)index the entries with linguistic properties

12. `cd poc/eb-pre/tools`
13. `rm ../data/index.json`
14. `python prep.py`

## (re-)create the embeddings

15. `cd poc/eb-pre/tools`
16. `rm ../data/semantic_search/*`
17. `python classify.py`
18. `python compress.py ../data/semantic_search/semantic_search-edition_7-doc2vec-learn-mc_40-ng_1-tm_0.5-ch_sentence.tv2.json 2`

## launch & visit the web application

19. `cd poc/eb-pre`
20. `python3 -m http.server 8000`
21. visit the following URL with your browser: http://localhost:8000/docs/

