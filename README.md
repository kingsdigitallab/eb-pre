https://github.com/TU-plogan/kp-editions

# TODO

DONE add subject terms to index & search results
DONE nlp over entire corpus
. domain1: fast?
. domain2: 0-shot
. domain3: topic modeling
. correlation: ...
. search: 

# Methods

1. clustering directly from subject terms without labelling domains -> clusters may not correspond to intuitive domains
2. map set of subject terms to set domains (e.g. fast hierarchy, wikidata)
    2.1 - FAST is very large dataset
    2.2 - domain not always broadest parent
    2.3 - not all terms have broader relationship
    2.4 - set of article terms may be insufficient to determine domain
3. classify body into set domains (0-shot)
4. topic modeling (top2vec, txtai): body -> topics
5. use article heading -> domain (via existing taxonomy or other method)
S 6. semantic search: doc2vec
   6.1 DYNAMIC: no authoritative set of domains & can query with almost any term

Object of categorisation:
* body
* title
* subject terms

Domain target:
* intrinsic: corpus keywords
* extrinsic: taxonomy or domain vocabulary

# Modules

* domain classifers
* domain vocabularies
* corpus reader
* index
* linguistic processor

# Notebooks

* create_index
* 
* group_from_subject_terms
* group_from_entry_body
* correlate

-> data/index.json

# Setup

* clone https://github.com/TU-plogan/kp-editions
* symlink that repo as a subdirectory kp-editions

# Problems & questions

. some .txt files are missing kp-editions/eb07/TXT/p18/kp-eb0718-076202-2281-v1.txt
. why do we have two sets of fast terms in some articles? kp-eb0924-073802-0783-v1.xml
. what was the purpose of subject term extraction? what tasks are they supposed to support & how was that tested?


# References

## datasets

https://github.com/TU-plogan/kp-editions
https://fast.oclc.org/fast/ontology/1.0/

## ui

https://bulma.io/documentation/components/panel/
https://github.com/itemsapi/itemsjs

## nlp

https://github.com/neuml/txtai
https://github.com/ddangelov/Top2Vec

## data processing

https://rdflib.readthedocs.io/en/stable/index.html
https://pandas.pydata.org/pandas-docs/stable/index.html
