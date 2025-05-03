/*
TODO

S switch ed 7 & 9
S back button
S optimisations
    WIP doc2vec params
    . replace numbers with NUMBER?
C param for number of results
C load progress bar

DONE show density
DONE link to entry
DONE sync URL: query
DONE FE loads corpus index
DONE FE load two indices & runs two searches in //
DONE click results -> search
DONE indicate entry size 

WONT BE create two indices (b/c more modular & efficient)
WONT FE merges auto-complete index
*/

const { createApp } = Vue

function expandURL(relativeURL) {
  let ret = relativeURL
  if (!(location.hostname === "localhost" || location.hostname === "127.0.0.1")) {
    ret = "https://raw.githubusercontent.com/kingsdigitallab/eb-pre/main/docs/" + relativeURL
  }
  return ret
}

class VectorIndex {

    constructor() {
        this.vs = {}
    }

    get_size(type='any') {
        let ret = []
        if (type == 'documents') {
            ret = Object.values(this.vs).filter(v => v.label !== v.label.toLowerCase())
        } else if (type == 'words') {
            ret = Object.values(this.vs).filter(v => v.label == v.label.toLowerCase())
        }
        return ret.length
    }

    findNearestVectors(v, type='any', precision=20) {
        // 100k vectors with 500 dims takes 0.6s on single thread 2022 i7 CPU
        let ret = null
        if (type == 'documents') {
            ret = Object.values(this.vs).filter(v => v.label !== v.label.toLowerCase())
        } else if (type == 'words') {
            ret = Object.values(this.vs).filter(v => v.label == v.label.toLowerCase())
        }
        if (!ret) {
            ret = Object.values(this.vs)
        }
        for (let av of ret) {
            av.similarity = this.computeSimilarity(v, av, precision)
        }
        ret.sort((v1, v2) => v2.similarity - v1.similarity)

        return ret
    }

    computeSimilarity(v1, v2, precision) {
        let ret = 0

        if (precision < 20) {
            v1 = v1.slice()
            v2 = v2.slice()
        }

        for (let i = 0; i < v1.length; i++) {
            if (precision < 20) {
                v1[i] = v1[i].toFixed(precision)
                v2[i] = v2[i].toFixed(precision)
            }

            ret += v1[i] * v2[i]
        }

        return ret / this.computeVectorLength(v1) / this.computeVectorLength(v2)
    }

    computeVectorLength(v) {
        let ret = 0
        for (let c of v) {
            ret += c*c
        }
        return Math.sqrt(ret)
    }

    getVectors() {
        let dims = 500
        let maxLength = 10
        let vectorCount = 100000
        let ret = []
        for (let i = 0; i < vectorCount; i++) {
            let v = []
            for (let d = 0; d < dims; d++) {
                v.push(Math.random() * maxLength)
            }
            ret.push(v)
        }
        return ret
    }

    async loadVectors(edition=7, speed='learn', domainSet='unspecified') {
        let vs = null
        console.log('embeddings - download')
        await fetch(expandURL(`../data/semantic_search/semantic_search-edition_${edition}-doc2vec-${speed}-mc_40-ng_1-tm_0.5-ch_sentence-de_2.tv2.json`))
        // await fetch(`../data/semantic_search/semantic_search-edition_${edition}-doc2vec-${speed}-mc_50-ng_0-tm_0.1-ch_sequential.tv2.json`)
            .then(response => response.json())
            .then(json => {
                this.vs = json
            });

        // console.log('embedding - quantise')
        // for (let [k, v] of Object.entries(this.vs)) {
        //     for (let i = 0; i < v.length; i++) {
        //         v[i] = v[i].toFixed(1)
        //     }
        // }

        console.log('embeddings - add labels')
        for (let [k, v] of Object.entries(this.vs)) {
            v.label = k
        }

        return this.vs
    }

    getVectorFromLabel(label) {
        return this.vs[label]
    }

    async testSimilarity() {
        // let vs = getVectors()

        let vs = await this.loadVectors()

        // let v1 = vs[0]

        let v1 = this.getVectorFromLabel('medicine')

        let t0 = new Date()
    //    for (let v of vs) {
    //        let d = computeSimilarity(v1, v)
    //        // console.log(d)
    //    }

        this.findNearestVectors(v1, vs)

        let t1 = new Date()
        console.log(t1 - t0)

        for (let i = 0; i < 30; i++) {
            console.log(vs[i].label)
        }
    }

}
// testSimilarity()

createApp({
    data() {
      return {
        edition: 7,
        speed: 'learn',

        precision: 20,

        query: '',
        limit: 25,
        minLength: 0,
        maxLength: 0,

        items: {
            'documents': [],
            'words': []
        },
        stats: {
            ngrams_count: 0,
            entries_count: 0
        },

        suggestions: ['a', 'bb'],
        status: 'loading',
        domainSets: ['2025-04-30', '2024-07-09-fixed', '2024-07-09-bugged', '2023'],
        // domainSet: '2024-07-09',
        // domainSet: '2023',
        domainSet: '2025-04-30',
    }
    },
    async mounted() {
        this.setSelectionFromAddressBar()
        await this.loadDatasets()
    },
    computed: {
        density() {
            let ret = 0
            for (item of this.items.documents) {
                ret += this.titlesEntry[item.label].mtld
            }
            if (ret > 0) {
                ret /= this.items.documents.length
            }
            return ret.toFixed(2);
        },
    },
    methods: {
      onSubmitForm() {
        this.search()
      },
      onClickItem(item) {
        this.query = item.label
        this.search()
      },
      async loadCorpusIndex() {
        await fetch(expandURL(`../data/${this.domainSet}/index.json`))
          .then(response => response.json())
          .then(json => {
            this.corpusIndex = json.data
            this.titlesEntry = {}
            for (let entry of this.corpusIndex) {
                this.titlesEntry[entry.title] = entry
            }
          })
      },
      getItemLength(item) {
        return this.titlesEntry[item.label].words
      },
      getTextUrlFromItem(item) {
        return 'https://raw.githubusercontent.com/TU-plogan/kp-editions/main/' + this.getTextPathFromId(this.titlesEntry[item.label].index);
      },
      getTextPathFromId(aid) {
        return aid.replace('xml', 'txt').replace('XML', 'TXT')
      },
      search() {
        let v = this.index.getVectorFromLabel(this.query)
        if (v) {
            this.items = {
                words: this.index.findNearestVectors(v, 'words', this.precision).slice(0, this.limit),
                documents: this.filterNearestDocVectorsByLength(this.index.findNearestVectors(v, 'documents', this.precision)),
            }
        } else {
            this.items.words = []
            this.items.documents = []
        }
        console.log(`${this.query} done`)
        this.setAddressBarFromSelection()
      },
      filterNearestDocVectorsByLength(vs) {
        let ret = []
        for (let v of vs) {
            let len = this.getItemLength(v)
            if (len > this.minLength && (this.maxLength == 0 || len < this.maxLength)) {
                // console.log(v.label, this.getItemLength(v))
                ret.push(v)
                if (ret.length >= this.limit) break;
            }
        }
        return ret
      },
      setAddressBarFromSelection() {
        // ?p1.so=&p1.co=&p2.so=...
        // let searchParams = new URLSearchParams(window.location.search)
        let searchParams = "";

        searchParams += `q=${this.query}`
        searchParams += `&l=${this.limit}`
        searchParams += `&ml=${this.minLength}`
        searchParams += `&xl=${this.maxLength}`

        let newRelativePathQuery =
          window.location.pathname + "?" + searchParams;
        history.pushState(null, "", newRelativePathQuery);
      },
      async setSelectionFromAddressBar() {
        let searchParams = new URLSearchParams(window.location.search);

        this.query = searchParams.get('q', '') || ''
        this.limit = parseInt(searchParams.get('l', '10') || '10')
        this.minLength = parseInt(searchParams.get('ml', '0') || '0')
        this.maxLength = parseInt(searchParams.get('xl', '0') || '0')
      },
      async loadDatasets() {
        this.status = 'loading'
        this.index = new VectorIndex()
        await this.index.loadVectors(this.edition, this.speed, this.domainSet)

        this.stats.ngrams_count = this.index.get_size('words')
        this.stats.entries_count = this.index.get_size('documents')

        await this.loadCorpusIndex()
        this.suggestions = Object.keys(this.index.vs).sort()
        this.search()
        this.status = 'loaded'
      },
      async onDomainSetChanged() {
        await this.loadDatasets()
      }
    },
}).mount('#semsearch')
