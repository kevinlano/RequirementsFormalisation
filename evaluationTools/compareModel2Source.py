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

import argparse


def hasVerb(sq) : 
  for x in sq :
    if x[1] == 'VB' : 
      return True
  return False

def isInitialUpperCase(wd) :
  txt = wd[0]
  if len(txt) == 0 :
    return False
  return txt[0:1].isupper()

def isInitialLowerCase(wd) :
  txt = wd[0]
  if len(txt) == 0 :
    return False
  return txt[0:1].islower()



def isVerb(wd) : 
  return wd[1] == 'VB'


def isSignificantVerb(wd) : 
  if wd[0] == 'be' : 
    return False
  if wd[0] == 'have' :
    return False
  return wd[1] == 'VB'


def isConnective(wd) : 
  if wd[1] == 'CC' : 
    return True
  return False


def isModalVerb(wd) : 
  return wd[1] == 'MD'

def isNoun(wd) : 
  return wd[1] == 'NN' or wd[1] == 'NNP' or wd[1] == 'NNS' or wd[1] == 'NNPS'

def isSingularNoun(wd) : 
  return wd[1] == 'NN' or wd[1] == 'NNP'

def isPluralNoun(wd) : 
  return wd[1] == 'NNS' or wd[1] == 'NNPS'

def isAdjective(wd) : 
  return wd[1] == 'JJ' or wd[1] == 'JJR' or wd[1] == 'JJS'

def isMainPartOfSpeech(wd) : 
  return isNoun(wd) or isVerb(wd) or isAdjective(wd) 

def isDeterminer(wd) : 
  return wd[1] == 'DT'

def isPreposition(wd) : 
  if wd[1] == 'TO' :
    return True 
  if wd[1] == 'IN' :
    return True
  return False

def isAuxiliaryPartOfSpeech(wd) : 
  return isDeterminer(wd) or isPreposition(wd)


def findFirstMatchIgnoreCase(ss, strs) : 
  lcss = ss.lower()
  for s in strs : 
    sx = s.lower()
    indx = sx.find(lcss)
    if indx >= 0 : 
      return s
  return None






# Main program 

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str,
                    default='source.txt', 
                    help='Source requirements file name f.txt')
parser.add_argument('--model', type=str,
                    default='mm.km3', 
                    help='Model file name g.km3')

args = parser.parse_args()

sourcename = args.source
targetname = args.model



dataset = nltk.data.load(sourcename)

nouns = []
verbs = []

sq = sent_tokenize(dataset)
ssq = [word_tokenize(t) for t in sq]
possq = [pos_tag(st) for st in ssq]

for lst in possq :
  for wd in lst : 
    if isNoun(wd) : 
      noun = wd[0]
      if noun in nouns : 
        pass
      else : 
        nouns.append(noun)
    if isVerb(wd) :
      verb = wd[0]
      if verb in verbs : 
        pass 
      else :  
        verbs.append(verb)

totalverbs = len(verbs)
totalnouns = len(nouns)
print("There are " + str(totalnouns) + " source nouns")
print("There are " + str(totalverbs) + " source verbs")


trg = open(targetname,'r')
modeltext = trg.readlines()

nounflaws = 0
verbflaws = 0

datanames = []
usecasenames = []

for lne in modeltext : 
  ssq = word_tokenize(lne)
  possq = pos_tag(ssq)
  if "class" in ssq :   
    classIndex = ssq.index("class")
    
    taggedName = possq[classIndex+1]
    (wd,tag) = taggedName
    datanames.append(wd)

  if "attribute" in ssq :
    attIndex = ssq.index("attribute")

    taggedName = possq[attIndex+1]
    (wd,tag) = taggedName
    datanames.append(wd)
  
  if "usecase" in ssq :
    ucIndex = ssq.index("usecase")

    taggedName = possq[ucIndex+1]
    (wd,tag) = taggedName
    usecasenames.append(wd)


# print(datanames)
# print(usecasenames)

for nx in nouns : 
  # It should occur in at least one class/attribute name
  elem = findFirstMatchIgnoreCase(nx, datanames)
  if elem == None : 
    print("! Requirements noun  " + nx + "  is not used in the model data")
    nounflaws = nounflaws + 1

for vx in verbs : 
  # It should occur in at least one usecase name
  elem = findFirstMatchIgnoreCase(vx, usecasenames)
  if elem == None : 
    print("! Requirements verb  " + vx + "  is not used in the model usecases")
    verbflaws = verbflaws + 1



if totalverbs > 0 : 
  print(">>> Verb completeness score: " + str((totalverbs - verbflaws)/totalverbs))
if totalnouns > 0 : 
  print(">>> Noun completeness score: " + str((totalnouns - nounflaws)/totalnouns))

