#######################################################################################################################
#
#  HMM based tagger.
#
#
#######################################################################################################################

"""
x m m m m m m m m m m m m
n                       n
n          (i,j)        n
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


class HMMTagger(object):
    """ Supervised Hidden Markov model POS tagger."""

    def __init__(self, tags_size=0,words_size=0):
        self.N = tags_size
        self.T = words_size
        self.states = [0 for x in range(tags_size)]
        self.A = Matrix(self.N, self.N)  # """ transition matrix """
        self.B = Matrix(self.N, self.T)  # """ emission(observation) matrix """
        self.PI = [0 for x in range(self.N)]  # """ Initialization matrix """
        self.Alpha = Matrix(self.N, self.T)  # """ Forward parameter matrix """
        self.Beta = Matrix(self.N, self.T)  # """ Backward parameter """

    def ForwardInit(self):
        print "Forward Init Start."
        for i in range(0, self.N):
            for t in range(0, self.T):
                alpha = self.PI[i] * self.B.get(i,t)
                self.Alpha.set(i, t, alpha)
        print "Forward Init End."

    def Forward(self):
        print "Forward Start."
        for t in range(0, self.T-1):
            for j in range(0, self.N):
                sum_of_alphas = 0     # sum of previous product of previous alpha and transition
                for i in range(0, self.N):
                    sum_of_alphas += self.Alpha.get(i, t) * self.A.get(i, j)
                alpha = sum_of_alphas * self.B.get(j, t+1)
                self.Alpha.set(j, t+1, alpha)
        print "Forward End."

    def BackwardInit(self):
        print "Backward Init Start."
        for t in range(0, self.T):
            for i in range(0, self.N):
                self.Beta.set(i, t, 1)
        print "Backward Init End."

    def Backward(self):
        print "Backward Start."
        for t in range(self.T-1, 0, -1):
            for j in range(0, self.N):
                sum_of_beta = 0
                for i in range(0, self.N):
                    sum_of_beta += self.Beta.get(i, t+1) * self.A.get(j, i) * self.B.get(j, t+1)
                self.Beta.set(j, t, sum_of_beta)
        print "Backward End."

    def SupervisedTrain(self):
        """
        Directly calculate the transition matrix (A), emission matrix (B), and
        initialization matrix (PI). using maximal likelihood estimation.
        """
        print "Supervised Train Start."

        print "Supervised Train End."

    def UnsupervisedTrain(self):
        """
        Expectation Maximization algorithm for unsupervised train. 
        """
        print "Unsupervised Train Start."
        self.BaumWelchInit();
        self.BaumWelch()
        print "Unsupervised Train End."

    def BaumWelchInit(self):
        print "Baum Welch Init Start."

        print "Baum Welch Init End."

    def BaumWelch(self):
        print "Baum Welch Start."

        print "Baum Welch End."

    def ViterbiInit(self):
        print "Viterbi Init Start."

        print "Viterbi Init End."

    def Viterbi(self):
        print "Viterbi Start."

        print "Viterbi End."


    def TrainInduction(self):
        print "Train Induction Start."
        print "Train Induction End."

    def Train(self):
        """Baum-Welch algorithm (EM algorithm) for training HMM POS tagger."""
        print "Train Start."

        print "Train End."

    def Evaluate(self):
        print "Init Start."
        print "Init End."

    def Decode(self):
        print "Decode Start."
        print "Decode End."
