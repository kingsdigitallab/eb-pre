[Experimental prototypes](https://kingsdigitallab.github.io/eb-pre/) based on [the TEI corpus](https://github.com/TU-plogan/kp-editions/tree/b476dc7ad2dadc1201e43f7dd4a053f7251d1b99) produced by the [Nineteenth-Century Knowledge Project](https://tu-plogan.github.io/source/c_about.html) led by Peter M. Logan.

[Introduction to this prototype on KDL website](https://kdl.kcl.ac.uk/projects/encyclopedia-britannica-exploratory-prototypes/)

[Documentation](https://github.com/kingsdigitallab/eb-pre/wiki)

# How to reproduce this proof of concept?

* clone this repository: `git clone --recursive https://github.com/kingsdigitallab/eb-pre.git`
* step inside: `cd eb-pre`

## Launch the web interfaces in a browser

* `bash launch.sh`
* CTRL+C to exit

## Run tools

To run tools, you first need to enter the development environment:

`bash activate.sh`

## Run notebooks

To open JupyterLab (for the notebooks in `notebooks/`) inside the development container:

`bash notebook.sh`

then open `http://localhost:8888/lab` (it opens automatically when ready). CTRL+C to exit.

# Data files

| ID   | Name   | Size | Format  | Produced from                  | Produced by                          | Path |
| :--- | :---   | :--- | :---    | :---                           | :---                                 | :--- |
| 1    | corpus | 4GB  | XML,TXT | Britannica 7th & 9th editions  | Nineteenth-Century Knowledge Project | data/kp-editions/ |   
| 2    | domain definitions | 1MB  | Python | Research | PI,KDL | Data  | helpers/settings.py |   
| 3    | entries index  | 23MB | JSON    | 1 (XML)                | tools/index.py                        | data/DOMAINS_SET/index.json |   
| 4    | embedding model | 146MB | TV2 (topic2vec) & JSON | 1 (TXT)      | tools/classify.py | app/data/semantic_search/semantic_search-edition_7-doc2vec-learn-mc_40-ng_1-tm_0.5-ch_sentence.tv2 & .json|   
| 5    | compressed model | 48MB  | JSON | 4 (JSON) | tools/compress.py | data/semantic_search/semantic_search-edition_7-doc2vec-learn-mc_40-ng_1-tm_0.5-ch_sentence-de_2.tv2.json |
| 6    | domain neighbours | 5MB  | JSON | 2, 4 (TV2) | tools/classify.py | data/semantic_search/DOMAINS_SET/semantic_search-edition_7-doc2vec-learn-mc_40-ng_1-tm_0.5-ch_sentence.tv2_domains.json |   
   

Note that: 
* `classify.py` also updates the index with the nearest domain to each entry and their cosine similarity;
* `DOMAINS_SET` is a variable defined in `helpers/settings.py` which determines which domain set the system should work with
* `DOMAINS_SETS` variable in settings.py contains all set definitions

# Maintenance

## Create a new a domains set

Because this system keeps old versions of the models and index, 
if anything change (e.g. corpus, domains set, ...) you need to 
create a new domains set for it.

Duplicate the most recent domain set in `helpers/settings.py` `DOMAINS_SETS`
and give it the current date. In index.py set `DOMAINS_SET` to that date.

Open `docs/kwsearch.html`, locate `domainSets: [`. 
Insert the new date at the beginning of that array.
Also change `domainSet: ` just below with that new date.

## How to incorporate a new version of the corpus?

First follow instructions from "Create a new domain set".

Then bring the corpus submodule up to date:

```bash
cd data/pk-editions
git checkout main
cd ../..
git commit -m "chore(data): updated the corpus" data/kp-editions
git push
```

Finally, build the index:

```bash
cd tools
python index.py
```

This operation takes approximately 30 minutes.

Follow sections below on how to "rebuild the words and entries embeddings" 
and "classify using new domain definitions".

## How to (re)build the embeddings model?

```bash
cd tools
python classify.py --rebuild
```

That command will also (re)classify the entries.

## How to reclassify entries using new domain definitions?

After adding new domain definitions in `settings.py`, reclassify like this:

```bash
cd tools
python classify.py
```

The index will be updated so each each entry records 
its top domain and their cosine score.
