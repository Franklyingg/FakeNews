'''
情感分析 积极 消极 中性
'''

from flair.data import Sentence
from flair.nn import Classifier

# make a sentence
sentence = Sentence('i eat a dinner.')

# load the NER tagger
tagger = Classifier.load('sentiment')

# run NER over sentence
tagger.predict(sentence)

# print the sentence with all annotations
print(sentence)