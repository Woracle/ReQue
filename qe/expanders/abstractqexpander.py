import traceback
import pandas as pd
import sys
sys.path.extend(['../qe'])

from cmn import utils
class AbstractQExpander:
    def __init__(self, replace=False, topn=None):
        self.replace = replace
        self.topn = topn

    def get_expanded_query(self, q, args=None):
        return q

    def get_model_name(self):
        if self.__class__.__name__ == 'AbstractQExpander':
            return 'AbstractQueryExpansion'.lower() #this is for backward compatibility for renaming this class
        return '{}{}{}'.format(self.__class__.__name__.lower(),
                         '.topn{}'.format(self.topn) if self.topn else '',
                         '.replace' if self.replace else '')

    def write_expanded_queries(self, Qfilename, Q_filename, clean=True):
        # prevent to clean the original query
        if self.__class__.__name__ == 'AbstractQExpander':
            clean = False

        model_name = self.get_model_name().lower()

        Q_ = pd.DataFrame()

        with open(Qfilename, 'r') as Qfile:
            with open(Q_filename, 'w') as Q_file:
                print('INFO: MAIN: {}: Expanding queries in {} ...'.format(self.get_model_name(), Qfilename))
                for line in Qfile:
                    if '<num>' in line:
                        qid = int(line[line.index(':') + 1:])
                        Q_file.write(line)
                    elif line[:7] == '<title>':#for robust & gov2
                        q = line[8:].strip()
                        if not q:
                            q = next(Qfile).strip()

                        try:
                            q_ = self.get_expanded_query(q, [qid])
                            q_ = utils.clean(q_) if clean else q_
                        except:
                            print('WARNING: MAIN: {}: Expanding query [{}:{}] failed!'.format(self.get_model_name(), qid, q))
                            print(traceback.format_exc())
                            q_ = q

                        Q_ = Q_.append({model_name: q_}, ignore_index=True)
                        print('INFO: MAIN: {}: {}: {} -> {}'.format(self.get_model_name(), qid, q, q_))
                        Q_file.write('<title> ' + str(q_) + '\n')

                    elif '<topic' in line:
                        s = line.index('\"') + 1
                        e = line.index('\"', s + 1)
                        qid = int(line[s:e])
                        Q_file.write(line)
                    elif line[2:9] == '<query>':#for clueweb09b & clueweb12b13
                            q = line[9:-9]
                            try:
                                q_ = self.get_expanded_query(q, [qid])
                                q_ = utils.clean(q_) if clean else q_
                            except:
                                print('WARNING: MAIN: {}: Expanding query [{}:{}] failed!'.format(self.get_model_name(), qid, q))
                                print(traceback.format_exc())
                                q_ = q

                            Q_ = Q_.append({model_name: q_}, ignore_index=True)
                            print('INFO: MAIN: {}: {}: {} -> {}'.format(self.get_model_name(), qid, q, q_))
                            Q_file.write('  <query>' + str(q_) + '</query>' + '\n')
                    elif len(line.split('\t')) > 2: #for tsv files
                        qid = int(line.split('\t')[0].rstrip())
                        q=line.split('\t')[1].rstrip()
                        try:
                            q_ = self.get_expanded_query(q, [qid])
                            q_ = utils.clean(q_) if clean else q_
                        except:
                            print('WARNING: MAIN: {}: Expanding query [{}:{}] failed!'.format(self.get_model_name(), qid, q))
                            print(traceback.format_exc())
                            q_ = q
                        Q_ = Q_.append({model_name: q_}, ignore_index=True)
                        print('INFO: MAIN: {}: {}: {} -> {}'.format(self.get_model_name(), qid, q, q_))
                        Q_file.write(str(qid)+'\t'+ str(q_) + '\n')
                    else:
                        Q_file.write(line)
        return Q_

    def read_expanded_queries(self, Q_filename):
        model_name = self.get_model_name().lower()
        Q_ = pd.DataFrame(columns=['qid'], dtype=int)
        with open(Q_filename, 'r') as Q_file:
            print('INFO: MAIN: {}: Reading expanded queries in {} ...'.format(self.get_model_name(), Q_filename))
            for line in Q_file:
                q_ = None
                if '<num>' in line:
                    qid = line[line.index(':') + 1:].strip()
                elif line[:7] == '<title>':#for robust & gov2
                    q_ = line[8:].strip() + ' '
                elif '<topic' in line:
                    s = line.index('\"') + 1
                    e = line.index('\"', s + 1)
                    qid = line[s:e].strip()
                elif line[2:9] == '<query>':  # for clueweb09b & clueweb12b13
                    q_ = line[9:-9] + ' '
                elif len(line.split('\t')) > 2:
                    qid = line.split('\t')[0].rstrip()
                    q_= line.split('\t')[1].rstrip()
                else:
                    continue
                if q_:
                    Q_ = Q_.append({'qid': qid, model_name: q_}, ignore_index=True)
        return Q_.astype({'qid': 'str'})

if __name__ == "__main__":
    qe = AbstractQExpander()
    print(qe.get_model_name())
    print(qe.get_expanded_query('International Crime Organization'))

    # from expanders.abstractqexpander import AbstractQExpander
    # from expanders.sensedisambiguation import SenseDisambiguation
    # from expanders.thesaurus import Thesaurus
    # from expanders.wordnet import Wordnet
    # from expanders.word2vec import Word2Vec
    from expanders.anchor import Anchor
    # from expanders.glove import Glove
    # from expanders.conceptnet import Conceptnet
    # from expanders.relevancefeedback import RelevanceFeedback
    # from expanders.stem import Stem  # Stem expander is the wrapper for all stemmers as an expnader :)
    # from stemmers.krovetz import KrovetzStemmer
    # from stemmers.lovins import LovinsStemmer
    # from stemmers.paicehusk import PaiceHuskStemmer
    # from stemmers.porter import PorterStemmer
    # from stemmers.porter2 import Porter2Stemmer
    # from stemmers.sstemmer import SRemovalStemmer
    # from stemmers.trunc4 import Trunc4Stemmer
    # from stemmers.trunc5 import Trunc5Stemmer
    from expanders.docluster import Docluster
    from expanders.termluster import Termluster
    from expanders.conceptluster import Conceptluster


    expanders = [AbstractQExpander(),
    #              Thesaurus(),
    #              Wordnet(),
    #              Word2Vec('../pre/wiki-news-300d-1M.vec', topn=3),
    #              Glove('../pre/glove.6B.300d', topn=3),
    #              SenseDisambiguation(),
    #              Conceptnet(),
    #              Thesaurus(replace=True),
                  #Wordnet(replace=True),
    #              Word2Vec('../pre/wiki-news-300d-1M.vec', topn=3, replace=True),
    #              Glove('../pre/glove.6B.300d', topn=3, replace=True),
    #              SenseDisambiguation(replace=True),
    #              Conceptnet(replace=True),
    #              Stem(KrovetzStemmer(jarfile='stemmers/kstem-3.4.jar')),
    #              Stem(LovinsStemmer()),
    #              Stem(PaiceHuskStemmer()),
    #              Stem(PorterStemmer()),
    #              Stem(Porter2Stemmer()),
    #              Stem(SRemovalStemmer()),
    #              Stem(Trunc4Stemmer()),
    #              Stem(Trunc5Stemmer()),
    #              RelevanceFeedback(ranker='bm25', prels='./output/robust04/topics.robust04.abstractqueryexpansion.bm25.txt',anserini='../anserini/',index='../ds/robust04/index-robust04-20191213'),
    #              Docluster(ranker='bm25', prels='./output/robust04/topics.robust04.abstractqueryexpansion.bm25.txt',anserini='../anserini/', index='../ds/robust04/index-robust04-20191213'),
    #              Termluster(ranker='bm25', prels='./output/robust04/topics.robust04.abstractqueryexpansion.bm25.txt',anserini='../anserini/', index='../ds/robust04/index-robust04-20191213'),
    #              Conceptluster(ranker='bm25', prels='./output/robust04/topics.robust04.abstractqueryexpansion.bm25.txt', anserini='../anserini/', index='../ds/robust04/index-robust04-20191213'),
                #Anchor(anchorfile='../pre/anchor_text_en_sample.ttl', vectorfile='../pre/wiki-anchor-text-en-ttl-300d-sample.vec', topn=3),
                 #Anchor(anchorfile='../pre/anchor_text_en_sample.ttl', vectorfile='../pre/wiki-anchor-text-en-ttl-300d-sample.vec', topn=3, replace=True)
                 ]
    for expander in expanders:
        expander.write_expanded_queries(
            '../ds/robust04/topics.robust04.txt',
            'dummy.txt')
        # expanders.write_expanded_queries('../ds/gov2/topics.terabyte05.751-800.txt', 'dummy')
        # expanders.write_expanded_queries('../ds/clueweb09b/topics.web.101-150.txt', 'dummy')
        # expanders.write_expanded_queries('../ds/clueweb12b13/topics.web.201-250.txt', 'dummy')
