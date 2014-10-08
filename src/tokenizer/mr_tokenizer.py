###
#  $ python mr_tokenizer.py doc_list.txt
###

"""
"""
from mrjob.job import MRJob
from nltk.tokenize import WhitespaceTokenizer
import re, os

## sentence detection
SENT_RE = re.compile(r'([A-Z][^\.!?]*[\.!?])', re.M)
DOC_DIR = os.path.abspath(os.path.dirname(__file__))

class MRTokenizer(MRJob):
    def mapper(self, _, docname):
        doc = ''.join(open(os.path.join(DOC_DIR, docname)).readlines()) 
        ## read document into sentences.			
        sentences = SENT_RE.findall(doc)
        for sentence in sentences:
            yield (sentence, docname)

    def combiner(self, sentence, docnames):
        ## merge sentence
        yield (sentence, ', '.join(docnames))

    def reducer(self, sentence, docnames):
        tokens = WhitespaceTokenizer().tokenize(sentence)
        yield (', '.join(docnames)+': '+sentence+' --> ', tokens)

if __name__ == '__main__':
     MRTokenizer.run()
