#######################################################################################################################
#
#  HMM based tagger.
#  shicq@brandeis.edu
#
#######################################################################################################################
import re, os, sys

WORD_RE = re.compile(r"[\S]+")
"""
x m m m m m m j m m m m x
n                       n
i          (i*m+j)      n
n                       n
x m m m m m m m m m m m x
"""
class Matrix(object):
    def __init__(self, m=0, n=0):
        self.m = m
        self.n = n
        self.data = [0 for x in range(m*n)]

    def get(self, i, j):
        return self.data[i*self.m+j]

    def set(self, i, j, val):
        self.data[i*self.m+j] = val

    def __str__(self):
        return str(self.data)

class HMMTagger(object):
    """
    Supervised Hidden Markov model POS tagger.
    """
    def __init__(self, model_dump_fil):
        import cPickle as pickle
        model_dump = pickle.load(open(model_dump_fil))
        self.N = model_dump['size']['tag']
        self.T = model_dump['size']['word']
        self.Tags = model_dump['tag']  # """ all the tags """
        self.Words = model_dump['word']   # """ all the words """
        self.A = Matrix(self.N, self.N)  # """ transition matrix """
        self.WordIndex = {}
        self.TagIndex = {}
        # print self.Tags, self.Words
        for i in range(0, self.N):
            self.TagIndex[self.Tags[i]] = i
        for i in range(0, self.T):
            self.WordIndex[self.Words[i]] = i
        for i in range(0, self.N):
            for j in range(0, self.N):
                self.A.set(i,j, model_dump['alpha'].get(str((self.Tags[i],self.Tags[j])),  0.000000001))
        self.B = Matrix(self.T, self.N)  # """ emission(observation) matrix """
        for i in range(0, self.N):
            for j in range(0, self.T):
                self.B.set(i,j, model_dump['beta'].get(str((self.Tags[i], self.Words[j])), 0.00000001))
        self.PI = []  # """ Initialization matrix """
        for i in range(0, self.N):
            self.PI.append(model_dump['pi'][self.Tags[i]])

    ###########################################################
    def Decode(self, words):
        """
        Decode will use Viterbi algorithm to calculate best sequence.
        """
        print "Decode Start."
        idx = []
        words.append(unicode('<end>'))
        for word in words:
            idx.append(self.WordIndex.get(word.lower(), -1))
        print idx, 'idx'

        V = [{}]
        path = {}

        # Initialize base cases (t == 0)
        for y in range(0, self.N):
            V[0][y] = self.PI[y] * self.B.get(y,idx[0])
            path[y] = [y]

        # Run Viterbi for t > 0
        for t in range(1, len(words)):
            V.append({})
            newpath = {}

            for y in range(0, self.N):
                (prob, state) = max((V[t-1][y0] * self.A.get(y0,y) * self.B.get(y, idx[t]), y0) for y0 in range(0, self.N))
                V[t][y] = prob
                newpath[y] = path[state] + [y]

            # Don't need to remember the old paths
            path = newpath
        n = 0           # if only one element is observed max is sought in the initialization values
        if len(words)!=1:
            n = t
        # self.print_dptable(V)
        (prob, state) = max((V[n][y], y) for y in range(0, self.N))
        tags = []
        for t in path[state]:
            tags.append(self.Tags[t])
        print tags
        print "Decode End."
        return (prob, tags)

if __name__ == '__main__':
     tagger = HMMTagger('HMM_MODEL')
     tagger.Decode(WORD_RE.findall(sys.argv[1]))