import sys
sys.path.extend(['../qe'])

from stemmers.krovetz import KrovetzStemmer
from stemmers.lovins import LovinsStemmer
from stemmers.paicehusk import PaiceHuskStemmer
from stemmers.porter import PorterStemmer
from stemmers.porter2 import Porter2Stemmer
from stemmers.sstemmer import SRemovalStemmer
from stemmers.trunc4 import Trunc4Stemmer
from stemmers.trunc5 import Trunc5Stemmer

anserini = {
    'path': '../anserini'
}

database = {
    'robust04': {
        'index': '../ds/robust04/lucene-index.robust04.pos+docvectors+rawdocs',
        'size': 520000,
        'topics': '',
        'prels': '',
        'w_t': 2.25,#OnFields
        'w_a': 1,#OnFields
        'tokens': 148000000,
    },
    'gov2': {
        'index': '../ds/gov2/lucene-index.gov2.pos+docvectors+rawdocs',
        'size': 25000000,
        'topics': '',
        'prels': '',
        'w_t': 4,#OnFields
        'w_a': 0.25,#OnFields
        'tokens': 17000000000,
    },
    'clueweb09b': {
        'index': '../ds/clueweb09b/lucene-index.cw09b.pos+docvectors+rawdocs',
        'size': 50000000,
        'topics': '',
        'prels': '',
        'w_t': 1,#OnFields
        'w_a': 0,#OnFields
        'tokens': 31000000000,
    },
    'clueweb12b13': {
        'index': '../ds/clueweb12b13/lucene-index.cw12b13.pos+docvectors+rawdocs ',
        'size': 50000000,
        'topics': '',
        'prels': '',
        'w_t': 4,#OnFields
        'w_a': 0,#OnFields
        'tokens': 31000000000,
    },
        'antique': {
        'index': '/home/negar/ReQue/Antique/index/lucene-index-antique',
        'size': 403000,
        'topics': '',
        'prels': '',
        'w_t': 2.25,#OnFields # to be tuned
        'w_a': 1,#OnFields # to be tuned
        'tokens': 16000000,
    }
}
# print(database['robust04']['index'])
# #TypeError: unhashable type: 'dict'
# thesaurus = {
#     {},
#     {
#         'replace': True,
#     }
# }
# wordnet = {
#     {},
#     {
#         'replace': True,
#     }
# }
# word2vec = {
#     {
#         'vectorfile' : '../pre/wiki-news-300d-1M.vec'
#     },
#     {
#         'replace': True,
#         'vectorfile' : '../pre/wiki-news-300d-1M.vec'
#     }
# }
# glove = {
#     {
#         'vectorfile': '../pre/glove.6B.300d'
#     },
#     {
#         'replace': True,
#         'vectorfile': '../pre/glove.6B.300d'
#     }
# }
# anchor = {
#     {
#         'anchorfile': '../pre/anchor_text_en.ttl',
#         'vectorfile': '../pre/wiki-anchor-text-en-ttl-300d.vec'
#     },
#     {
#         'replace': True,
#         'anchorfile': '../pre/anchor_text_en.ttl',
#         'vectorfile': '../pre/wiki-anchor-text-en-ttl-300d.vec'
#     }
# }
# wiki = {
#     {
#         'vectorfile': '../pre/temp_model_Wiki'
#     },
#     {
#         'replace': True,
#         'vectorfile': '../pre/temp_model_Wiki'
#     }
# }
# tagmee = {
#     {},
#     {
#         'replace': True,
#     }
# }
# sensedisambiguation = {
#     {},
#     {
#         'replace': True,
#     }
# }
# conceptnet = {
#     {},
#     {
#         'replace': True,
#     }
# }
# stem = {
#     {
#         'stemmer': KrovetzStemmer(jarfile='stemmers/kstem-3.4.jar')
#     },
#     {
#         'stemmer': LovinsStemmer()
#     },
#     {
#         'stemmer': PaiceHuskStemmer()
#     },
#     {
#         'stemmer': PorterStemmer()
#     },
#     {
#         'stemmer': Porter2Stemmer()
#     },
#     {
#         'stemmer': SRemovalStemmer()
#     },
#     {
#         'stemmer': Trunc4Stemmer()
#     },
#     {
#         'stemmer': Trunc5Stemmer()
#     }
# }
# relevancefeedback = {
#     {
#         'ranker': '',
#         'prels': '',
#         'anserini': '',
#         'index': ''
#     }
# }
# docluster = {
#     {
#         'ranker': '',
#         'prels': '',
#         'anserini': '',
#         'index': ''
#     }
# }
# termluster = {
#     {
#         'ranker': '',
#         'prels': '',
#         'anserini': '',
#         'index': ''
#     }
# }
# conceptluster = {
#     {
#         'ranker': '',
#         'prels': '',
#         'anserini': '',
#         'index': ''
#     }
# }
# onfields = {
#     {
#         'ranker': '',
#         'prels': '',
#         'anserini': '',
#         'index': '',
#         'w_t': 0,
#         'w_a': 0,
#         'corpus_size': 0
#     }
# }
# adaponfields = {
#     {
#         'ranker': '',
#         'prels': '',
#         'anserini': '',
#         'index': '',
#         'w_t': 0,
#         'w_a': 0,
#         'corpus_size': 0,
#         'collection_tokens': 0,
#         'ext': '',
#         'adap': True,
#     }
# }
#
# model2params = {
#     'thesaurus': thesaurus,
#     'wordnet': wordnet,
#     'word2vec': word2vec,
#     'glove': glove,
#     'anchor': anchor,
#     'wiki': wiki,
#     'tagmee': tagmee,
#     'sensedisambiguation': sensedisambiguation,
#     'conceptnet': conceptnet,
#     'stem': stem,
#     'relevancefeedback': relevancefeedback,
#     'docluster': docluster,
#     'termluster': termluster,
#     'conceptluster': conceptnet,
#     'onfields': onfields,
#     'adaponfields': adaponfields
# }

#
# def get_model_specific_params(model_name, field):
#     return model2params[model_name.upper()][field]
