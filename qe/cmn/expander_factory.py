import sys
sys.path.extend(['../qe'])
sys.path.extend(['../qe/cmn'])

#TODO: ServiceFactory: dynamically load the class files in expanders folder and create an instance object
from expanders.abstractqexpander import AbstractQExpander
from expanders.sensedisambiguation import SenseDisambiguation
from expanders.thesaurus import Thesaurus
from expanders.wordnet import Wordnet
from expanders.word2vec import Word2Vec
from expanders.glove import Glove
from expanders.conceptnet import Conceptnet
from expanders.relevancefeedback import RelevanceFeedback
from expanders.docluster import Docluster
from expanders.termluster import Termluster
from expanders.conceptluster import Conceptluster
from expanders.anchor import Anchor
from expanders.tagmee import Tagmee
from expanders.wiki import Wiki
from expanders.onfields import OnFields
from expanders.adaponfields import AdapOnFields
from expanders.bertqe import BertQE

#TODO: ServiceFactory: dynamically load the class files in stemmers folder and create an instance object
from stemmers.krovetz import KrovetzStemmer
from stemmers.lovins import LovinsStemmer
from stemmers.paicehusk import PaiceHuskStemmer
from stemmers.porter import PorterStemmer
from stemmers.porter2 import Porter2Stemmer
from stemmers.sstemmer import SRemovalStemmer
from stemmers.trunc4 import Trunc4Stemmer
from stemmers.trunc5 import Trunc5Stemmer
from expanders.stem import Stem # Stem expander is the wrapper for all stemmers as an expnader :)

import param
#global analysis
def get_nrf_expanders():
    expanders = [AbstractQExpander(),
                 Thesaurus(),
                 Wordnet(),
                 Word2Vec('../pre/wiki-news-300d-1M.vec'),
                 Glove('../pre/glove.6B.300d'),
                 Anchor(anchorfile='../pre/anchor_text_en.ttl', vectorfile='../pre/wiki-anchor-text-en-ttl-300d.vec'),
                 Wiki('../pre/temp_model_Wiki'),
                 Tagmee(),
                 SenseDisambiguation(),
                 Conceptnet(),
                 Thesaurus(replace=True),
                 Wordnet(replace=True),
                 Word2Vec('../pre/wiki-news-300d-1M.vec', replace=True),
                 Glove('../pre/glove.6B.300d', replace=True),
                 Anchor(anchorfile='../pre/anchor_text_en.ttl', vectorfile='../pre/wiki-anchor-text-en-ttl-300d.vec', replace=True),
                 Wiki('../pre/temp_model_Wiki', replace=True),
                 Tagmee(replace=True),
                 SenseDisambiguation(replace=True),
                 Conceptnet(replace=True),
                 Stem(KrovetzStemmer(jarfile='stemmers/kstem-3.4.jar')),
                 Stem(LovinsStemmer()),
                 Stem(PaiceHuskStemmer()),
                 Stem(PorterStemmer()),
                 Stem(Porter2Stemmer()),
                 Stem(SRemovalStemmer()),
                 Stem(Trunc4Stemmer()),
                 Stem(Trunc5Stemmer()),
                 # since RF needs index and search output which depends on ir method and topics database, we cannot add this here. Instead, we run it individually
                 # RF assumes that there exist abstractqueryexpansion files
                 ]

    return expanders

#local analysis
def get_rf_expanders(rankers, corpus, output, ext_corpus=None, ext_prels=None):
    expanders = []
    for ranker in rankers:
        ranker_name = get_ranker_name(ranker)
        expanders.append(RelevanceFeedback(ranker=ranker_name,
                                           prels='{}.abstractqueryexpansion.{}.txt'.format(output, ranker_name),
                                           anserini=param.anserini['path'],
                                           index=param.database[corpus]['index']))
        expanders.append(Docluster(ranker=ranker_name,
                                   prels='{}.abstractqueryexpansion.{}.txt'.format(output, ranker_name),
                                   anserini=param.anserini['path'],
                                   index=param.database[corpus]['index'])),
        expanders.append(Termluster(ranker=ranker_name,
                                    prels='{}.abstractqueryexpansion.{}.txt'.format(output, ranker_name),
                                    anserini=param.anserini['path'],
                                    index=param.database[corpus]['index']))
        expanders.append(Conceptluster(ranker=ranker_name,
                                       prels='{}.abstractqueryexpansion.{}.txt'.format(output, ranker_name),
                                       anserini=param.anserini['path'],
                                       index=param.database[corpus]['index']))
        expanders.append(OnFields(ranker=ranker_name,
                                  prels='{}.abstractqueryexpansion.{}.txt'.format(output, ranker_name),
                                  anserini=param.anserini['path'],
                                  index=param.database[corpus]['index'],
                                  w_t=param.database[corpus]['w_t'],
                                  w_a=param.database[corpus]['w_a'],
                                  corpus_size=param.database[corpus]['size']))
        expanders.append(AdapOnFields(ranker=ranker_name,
                                      prels='{}.abstractqueryexpansion.{}.txt'.format(output, ranker_name),
                                      anserini=param.anserini['path'],
                                      index=param.database[corpus]['index'],
                                      w_t=param.database[corpus]['w_t'],
                                      w_a=param.database[corpus]['w_a'],
                                      corpus_size=param.database[corpus]['size'],
                                      collection_tokens=param.database[corpus]['tokens'],
                                      ext_corpus=ext_corpus,
                                      ext_index=param.database[ext_corpus]['index'],
                                      ext_prels=ext_prels,
                                      ext_collection_tokens=param.database[ext_corpus]['tokens'],
                                      ext_w_t=param.database[ext_corpus]['w_t'],
                                      ext_w_a=param.database[ext_corpus]['w_a'],
                                      ext_corpus_size=param.database[ext_corpus]['size'],
                                      adap=True))
        expanders.append(BertQE(ranker=ranker_name,
                          prels='{}.abstractqueryexpansion.{}.txt'.format(output, ranker_name),
                          index=param.database[corpus]['index'],
                           anserini=param.anserini['path']))

    return expanders

def get_expanders_names(rankers):
    expanders = get_nrf_expanders() + get_rf_expanders(rankers, None, None)
    return [e.get_model_name() for e in expanders]

def get_ranker_name(ranker):
    return ranker.replace('-', '').replace(' ', '.')

if __name__ == "__main__":
    print(get_expanders_names(['-bm25', '-bm25 -rm3', '-qld', '-qld -rm3']))
