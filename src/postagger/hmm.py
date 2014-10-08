import numpy
import numpy.random
class hmm:
    def epsilon(self,observations,alpha,beta):
        """ epsilon: the slow part of learning a hidden markov model """
        hidden_symbols = self.hidden_symbols
        T = len(observations)
        a = self.a
        b = self.b
        result = numpy.zeros((hidden_symbols,hidden_symbols,T))
        """ O(n^4) or thereabouts """
        for i in range(0,hidden_symbols):
            for j in range(0,hidden_symbols):
                for t in range(0,T-1):
                    s = 0
                    ks = alpha[0:hidden_symbols,t]
                    ls = beta[0:hidden_symbols,t+1] * b[0:hidden_symbols,observations[t+1]]
                    kls = ks.T * ls # generate a square matrix
                    klas = numpy.dot(kls,a) # dot product with a
                    s = klas.sum() # sum of your square matrix's cells
                    ait = alpha[i,t] * a[i,j] * beta[j,t+1] * b[j,observations[t+1]]
                    result[i,j,t] = ait/s
                    pass
                pass
            pass
        return result
    def alpha(self,observations=[]):
        """ forward step: generate alpha matrix """
        T = len(observations)
        hidden_symbols = self.hidden_symbols
        result = numpy.zeros((hidden_symbols,T))
        pi = self.pi
        a = self.a
        b = self.b
        result[0:hidden_symbols,0] = pi * b[0:hidden_symbols,observations[0]]
        for t in range(1,T):
            for j in range(0,hidden_symbols):
                bs = b[j,observations[t]]
                s = 0
                for i in range(0,hidden_symbols):
                    ait = result[i,t-1]
                    aij = a[i,j]
                    s = s + ait*aij
                    pass
                result[j,t] = bs*s
                pass
            pass
        return result
    def _new_b(self,observations,gamma):
        """ generate a new b matrix """
        hidden_symbols = self.hidden_symbols
        visible_symbols = self.visible_symbols
        T = len(observations)
        result = numpy.zeros((hidden_symbols,visible_symbols))
        for i in range(0,hidden_symbols):
            for j in range(0,visible_symbols):
                s0 = 0
                s1 = 0
                for t in range(1,T-1):
                    vk = gamma[i,t]
                    if(observations[t] != j):
                        vk = 0
                        pass
                    s0 = s0 + vk
                    s1 = s1 + gamma[i,t]
                    pass
                result[i,j] = s0 / s1
                pass
            pass
        return result
    def train(self,observations = []):
        """ uses the baum-welch algorithm """
        """ perform an update on the a,b,pi matrices so they conform more with observations """
        """ forward step """
        alpha = self.alpha(observations)
        """ backward step """
        beta = self.beta(observations,alpha)
        """ iteration """
        gamma = self.gamma(observations,alpha,beta)
        epsilon = self.epsilon(observations,alpha,beta)
        hidden_symbols = self.hidden_symbols
        self.pi[0:hidden_symbols] = gamma[0:hidden_symbols,1]
        self.a = self._new_a(observations,epsilon,gamma)
        self.b = self._new_b(observations,gamma)
        """ you now more-closely match the observations, probably """
        pass
    def beta(self,observations,alpha):
        """ generate beta in the "backward" procedure """
        T = len(observations)
        hidden_symbols = self.hidden_symbols
        result = numpy.zeros((hidden_symbols,T+1))
        """ the "final" symbols all have probability 1 """
        result[0:hidden_symbols,T] = result[0:hidden_symbols,T] + 1
        a = self.a 
        b = self.b
        """ go backward in time """
        for t in range(T-1,0,-1):
            for i in range(0,hidden_symbols):
                """ sum the "probabilities" to get the odds of being symbol i at time t? """
                s=0
                for j in range(0,hidden_symbols):
                    s = s + result[j,t+1] * a[i,j] * b[j,observations[t]]
                    pass
                result[i,t] = s
                pass
            pass
        return result
    def _new_a(self,observations,epsilon,gamma):
        """ generate a new a matrix as part of the iteration step """
        hidden_symbols = self.hidden_symbols
        result = numpy.zeros((hidden_symbols,hidden_symbols))
        T = len(observations)
        for i in range(0,hidden_symbols):
            for j in range(0,hidden_symbols):
                s0 = 0
                s1 = 0
                """ sum up the "odds" across the observations """
                for t in range(1,T-1):
                    s0 = s0 + epsilon[i,j,t]
                    s1 = s1 + gamma[i,t]
                    pass
                result[i,j] = s0 / s1
                pass
            pass
        return result
    def gamma(self,observations,alpha,beta):
        """ generate gamma as part of your update step """
        T = len(observations)
        hidden_symbols = self.hidden_symbols
        result = numpy.zeros((hidden_symbols,T))
        """ use forward and backward data to get gamma """
        for t in range(0,T):
            for i in range(0,hidden_symbols):
                abit = alpha[i,t] * beta[i,t]
                s = 0
                for j in range(0,hidden_symbols):
                    s = s + (alpha[j,t] * beta[j,t])
                    pass
                result[i,t] = abit/s
                pass
            pass
        return result
    def __init__(self,visible_symbols,hidden_symbols):
        """ init the class with a random transition function """
        self.visible_symbols = visible_symbols
        self.hidden_symbols = hidden_symbols
        """ state-state transitions (hidden symbols) """
        self.a = self.normalize_rows(numpy.random.rand(hidden_symbols,hidden_symbols))
        """ state-observation transitions (visible symbols) """
        self.b = self.normalize_rows(numpy.random.rand(hidden_symbols,visible_symbols))
        """ initial state probabilities (hidden symbols) """
        self.pi = numpy.random.rand(hidden_symbols)
        self.pi = self.pi / self.pi.sum()
        pass
    def normalize_rows(self,mat):
        """ utility function to make the second parameter sum to 1.  there must be a better way to do this """
        shape = mat.shape
        result = numpy.zeros(shape)
        for i in range(0,shape[0]):
            s = mat[i,0:shape[1]].sum()
            result[i,0:shape[1]] = mat[i,0:shape[1]] / s
            pass
        return result
    pass




if __name__ == '__main__':
    import random
    import numpy
    import numpy.random

    visible_symbols = 2
    hidden_symbols = 16

    model = hmm(visible_symbols,hidden_symbols)

    T = 100

    """ generate some random observations to work from  """
    observations = []
    for t in range(0,T):
        observations.append(random.randint(0,visible_symbols-1))
        pass

    model.train(observations)