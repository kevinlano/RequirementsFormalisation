import nltk
import nltk.tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk.data
from nltk.tag import PerceptronTagger
from nltk.tag import pos_tag
from nltk.parse import RecursiveDescentParser
from nltk.parse.corenlp import GenericCoreNLPParser
from nltk.tree import *
from nltk.metrics import edit_distance


def hasVerb(sq) : 
  for x in sq :
    if x[1] == 'VB' : 
      return True
  return False



dataset = nltk.data.load('k3ucs.txt')
# print(dataset)

sq = sent_tokenize(dataset)
# print(sq)

# grammar = nltk.data.load('grammars/book_grammars/discourse.fcfg')

# parser = nltk.parse.RecursiveDescentParser(grammar)
# parser = GenericCoreNLPParser()
# psents = GenericCoreNLPParser.parse_all(parser,ss)

ssq = [word_tokenize(t) for t in sq]
# print(ssq)

# sentence1 = 'a person barks'.split()

# for t in parser.parse(ssq[0]):
#   print(t)


possq = [pos_tag(st) for st in ssq]
# print(possq)


actors = []

vbsq = [sq for sq in possq if hasVerb(sq)]

for sq in vbsq :
  isFirst = True
  isThere = False
  verbe = ""
  currentActor = ""
  for wd in sq :
    pos = wd[1]
    if (pos == 'NN' or pos == 'NNP' or pos == 'NNP' or pos == 'NNPS') and isFirst :
      currentActor = wd[0]
      if currentActor in actors : 
        pass
      else : 
        actors.append(currentActor)
      isFirst = False
    else :
      if pos == 'VB' or pos == 'VBG' or pos == 'VBP' or pos == 'VBN' or pos == 'VBZ' : 
        verbe = verbe + wd[0]  
      if pos == 'NN' or pos == 'NNP' or pos == 'NNP' or pos == 'NNPS' :
        verbe = verbe + wd[0]
  print("usecase " + verbe + " { actor = " + currentActor + "; }")
  print("")


for act in actors : 
  print("class " + act + " { }")
  print()



