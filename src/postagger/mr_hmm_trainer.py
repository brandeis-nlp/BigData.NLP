#######################################################################################################################
#
#  Train HMM Model <PI, Alpha, Beta>, in Map-Reduce.
#  shicq@brandeis.edu
#
#######################################################################################################################

from mrjob.job import MRJob
from mrjob.job import MRStep
from nltk.tokenize import WhitespaceTokenizer
import re, os
import mrjob

WORD_RE = re.compile(r"[\S]+")

CURR_DIR = os.path.abspath(os.path.dirname(__file__))

DUMP = {'alpha':{}, 'beta':{}, 'pi':{}, 'size':{},'tag':[], 'word':[]}

class MRCounter(MRJob):
    def mapper_words(self, _, dirname):
        subdir = os.path.join(CURR_DIR, dirname)
        fils = [ os.path.join(subdir,f) for f in os.listdir(subdir)]
        for fil in fils:
            print "FILE = ", fil
            for lin in open(fil).readlines():
                tagged_words = WORD_RE.findall(lin)
                tagged_words.append('<END>/<END>')
                last_tag = ''
                for tagged_word in tagged_words:
                    pair = tagged_word.split('/')
                    # print "tagged_word = ",tagged_word
                    word = pair[0].lower()
                    tag = pair[1].upper()
                    yield (('word', word), 1)
                    yield (('tag', tag), 1)
                    yield (('emission',tag, word), 1)
                    if last_tag != '':
                        yield(('transition', last_tag, tag), 1)
                    last_tag = tag
                # yield(('transition', last_tag, '<END>'), 1)

    def combiner_words_freq(self, tuple, counts):
        ## merge sentence
        yield (tuple, sum(counts))

    def reducer_words_freq(self, tuple, counts):
        if tuple[0] == 'transition':
            yield(('alpha', tuple[1]), (tuple[2], sum(counts)))
        elif tuple[0] == 'emission':
            yield(('beta', tuple[1]), (tuple[2], sum(counts)))
        elif tuple[0] == 'tag':
            yield(('pi', tuple[1]), sum(counts))
            DUMP['tag'].append(tuple[1])
        elif tuple[0] == 'word':
            DUMP['word'].append(tuple[1])
        yield (('size', tuple[0]), 1)

    def reducer_words_prob(self, key, values):
        if 'alpha' == key[0]:
            tag = key[1]
            tag_freq = 0
            to_tags = []
            for val in values:
                to_tags.append(val)
                tag_freq += val[1]
            for to_tag in to_tags:
                yield (('alpha', tag, to_tag[0]), float(to_tag[1])/tag_freq)
                DUMP['alpha'][str((tag, to_tag[0]))] = float(to_tag[1])/tag_freq
        elif 'beta' == key[0]:
            tag = key[1]
            tag_freq = 0
            to_words = []
            for val in values:
                tag_freq += val[1]
                to_words.append(val)
            for to_word in to_words:
                yield (('beta', tag, to_word[0]), float(to_word[1])/tag_freq)
                DUMP['beta'][str((tag, to_word[0]))] = float(to_word[1])/tag_freq
        elif 'pi' == key[0]:
            total = sum(values)
            yield(key, total)
            DUMP['pi'][str(key[1])] = total
        # count word, tag, emission, bigram, transition size
        elif 'size' == key[0]:
            total = sum(values)
            yield (key, total)
            DUMP['size'][str(key[1])] = total
            # print 'size', dict

    def steps(self):
        return [
            MRStep(mapper=self.mapper_words,
                    combiner=self.combiner_words_freq,
                    reducer=self.reducer_words_freq),
            MRStep(reducer=self.reducer_words_prob)
        ]

if __name__ == '__main__':
     MRCounter.run()
     import cPickle as pickle
     pickle.dump(DUMP,open("HMM_MODEL", 'wb'))