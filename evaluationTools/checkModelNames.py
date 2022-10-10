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





# Main program 

parser = argparse.ArgumentParser()
parser.add_argument('--model', type=str,
                    default='mm.km3', 
                    help='Model file name f.km3')

args = parser.parse_args()

filename = args.model

src = open(filename,'r')
modeltext = src.readlines()

validClasses = 0
totalClasses = 0

validAttributes = 0
totalAttributes = 0

validUsecases = 0
totalUsecases = 0

flaws = 0

for lne in modeltext : 
  ssq = word_tokenize(lne)
  possq = pos_tag(ssq)
  if "class" in ssq :   
    totalClasses = totalClasses + 1
    classIndex = ssq.index("class")
    
    taggedName = possq[classIndex+1]
    (wd,tag) = taggedName
    if isSingularNoun(taggedName) and isInitialUpperCase(taggedName) : 
      validClasses = validClasses + 1
    else : 
      print("!! Class name " + wd + " " + tag + " should be singular noun with initial capital")
      flaws = flaws + 1

  if "attribute" in ssq :
    totalAttributes = totalAttributes + 1
    attIndex = ssq.index("attribute")

    taggedName = possq[attIndex+1]
    (wd,tag) = taggedName
    if isInitialLowerCase(taggedName) : 
      validAttributes = validAttributes + 1
    else : 
      print("!! Attribute name " + wd + " should have initial lower case letter")
      flaws = flaws + 1
  
  if "usecase" in ssq :
    totalUsecases = totalUsecases + 1
    ucIndex = ssq.index("usecase")

    taggedName = possq[ucIndex+1]
    (wd,tag) = taggedName
    if isInitialLowerCase(taggedName) : 
      validUsecases = validUsecases + 1
    else : 
      print("!! Use case name " + wd + " should have initial lower case letter")
      flaws = flaws + 1


if totalClasses > 0 : 
  print(">>> Class validity score: " + str(validClasses/totalClasses))
if totalAttributes > 0 : 
  print(">>> Attribute validity score: " + str(validAttributes/totalAttributes))
if totalUsecases > 0 : 
  print(">>> Usecase validity score: " + str(validUsecases/totalUsecases))
print(">>> Total number of flaws = " + str(flaws))

