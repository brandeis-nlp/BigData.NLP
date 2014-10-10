MRJob Local Map Reduce Example

'''sh
$ cd BigData.NLP/src/mrjob
$ python mrjob_example1.py ComputationalSemantics.txt
'''

Training HHM Model

'''sh
$ cd BigData.NLP/src/postagger
$ python mr_hmm_trainer.py train.txt
no configs found; falling back on auto-configuration
no configs found; falling back on auto-configuration
creating tmp directory c:\cygwin\tmp\mr_hmm_trainer.lapps.20141010.075419.969000
'''

Testing HMM Tagger
'''sh
$ cd BigData.NLP/src/postagger
$ python hmm_tagger.py "Where are you ?"
Decode Start.
[u'WRB', u'VBN', u'PPO', u'.', u'<END>']
Decode End.
'''