###
#  $ python mr_tokenizer.py doc_list.txt
###

"""
"""
from mrjob.job import MRJob
from nltk.corpus import brown
import re, os

## sentence detection
SENT_RE = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)

class MRHMMPOSTagger(MRJob):
    def mapper_init():
        wsj = nltk.corpus.treebank.tagged_words(tagset='universal')
        tag_fd = nltk.FreqDist(tag for (word, tag) in wsj)
        thelta = Initialization(tag_fd, wsj)

    def mapper(self, _, tag_sequences): ## E-Step
        ## Forward-Backward algorithm
        alphas = Forward(tag_sequences, thelta)
        betas = Backward(tag_sequences, thelta)
        ## Observation probability
        observation_probability = CalculateObservationProb(alphas, betas)
        ##
        epsilons =  CalculateEpsilons(alphas, betas, observation_probability)
        lambdas =  CalculateLambdas(alphas, betas, observation_probability)
        for tag_sequence in tag_sequences:
            yield ((tag_sequence, 'lambda'), lambdas)
            yield ((tag_sequence, 'epsilon'), epsilons)
			

    def combiner(self, tag_sequence, values):
        yield (tag_sequence, sum(values))

    def reducer(self, tag_sequence, values): ##M-Step
        normalized = Normalization()
        yield (', '.join(docnames)+': '+sentence+' --> ', tokens)

if __name__ == '__main__':
     MRHMMPOSTagger.run()
