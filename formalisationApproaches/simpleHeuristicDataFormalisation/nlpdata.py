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


def isAdjective(wd) : 
  return wd[1] == 'JJ' or wd[1] == 'JJR' or wd[1] == 'JJS'

def isDeterminer(wd) : 
  return wd[1] == 'DT'

def isPreposition(wd) : 
  if wd[1] == 'TO' :
    return True 
  if wd[1] == 'IN' :
    return True
  return False

def entities(sq) :
  # noun phrases <DT>?<JJ>*<NN>+
  res = []
  chunk = []
  for wd in sq : 
    if chunk == [] :
      if isDeterminer(wd) or isAdjective(wd) or isNoun(wd) : 
        chunk.append(wd)
    else : 
      lst = chunk[-1]
      if isAdjective(wd) or isNoun(wd) : 
        if isAdjective(lst) or isDeterminer(lst) : 
          chunk.append(wd) 
        else :
          if isNoun(lst) and isNoun(wd) : 
            chunk.append(wd) 
          else : 
            res.append(chunk)
            chunk = []
      else : 
        if isNoun(lst) : 
          res.append(chunk)
        chunk = []
  if chunk != [] : 
    if isNoun(chunk[-1]) :
      res.append(chunk)
  return res

def hasClassNoun(sq) : 
  for wd in sq : 
    if wd[0] in classnouns : 
      return True
  return False

def classType(sq) : 
  for wd in sq : 
    if wd[0] in classnouns : 
      return wd[0].capitalize()
  return "OclAny"

def hasAttributeNoun(sq) : 
  for wd in sq : 
    if wd[0] in attributenouns : 
      return True
  return False


def npvpremChunk(sq) :
  # splits into NP, VP, + remainder
  # [^<VB>]* <MD>... <VB>[?]*
 
  np = []
  vp = []
  rem = []
  for wd in sq :
    if vp == [] and rem == [] :
      if isModalVerb(wd) :
        vp = [wd]
      elif isNoun(wd) or isAdjective(wd) or isDeterminer(wd) : 
        np.append(wd)
      elif isSignificantVerb(wd) :
        rem.append(wd)
      else : 
        np.append(wd)
    elif rem == [] :
      if isSignificantVerb(wd) : 
        rem.append(wd)
      else :
        vp.append(wd)
    else : 
      rem.append(wd)
  return (np,vp,rem)


def actor(sq) :
  res = ""
  for wd in sq :
    (txt,pos) = wd
    if isNoun(wd) or isAdjective(wd) or isConnective(wd) :
      if len(res) == 0 : 
        res = txt 
      else :
        res = res + "_" + txt
  return res


def underscoreWordConcatenation(sq) :
  res = ""
  for wd in sq :
    (txt,pos) = wd
    if txt.isalnum() : 
      if len(res) == 0 : 
        res = txt 
      else :
        res = res + "_" + txt
  return res


def verbCategory(wd,vbs) : 
  rverbs = vbs["read"]
  cverbs = vbs["create"]
  dverbs = vbs["delete"]
  everbs = vbs["edit"]
  if wd in rverbs : 
    return "read"
  if wd in dverbs : 
    return "delete"
  if wd in cverbs : 
    return "create"
  if wd in everbs : 
    return "edit"
  return "other"


def nounCategory(wd,nouns) : 
  cnouns = nouns["classes"]
  anouns = nouns["attributes"]
  if wd in cnouns : 
    return "class"
  if wd in anouns : 
    return "attribute"
  return "other"


def allOptional(occurs) : 
  if occurs == [] : 
    return True
  if occurs[0] == "1" : 
    return False
  return allOptional(occurs[1:])


def satisfiesRegex(sq,actions,occurs) : 
  if sq == [] : 
    if actions == [] : 
      return True
    if allOptional(occurs) : 
      return True
    return False
  return False


def usecaseName(vbp,rem) : 
  if len(rem) <= 0 : 
    return underscoreWordConcatenation(vbp[1:])
  return underscoreWordConcatenation(rem)

def className(np) : 
  if len(np) > 0 and isDeterminer(np[0]) :
    return className(np[1:])
  clsnme = underscoreWordConcatenation(np)
  return clsnme.capitalize()
  

# verbs = nltk.data.load('verbs.pickle')
# print(verbs)


# Main program

parser = argparse.ArgumentParser()
parser.add_argument('--source', type=str,
                    default='source.txt', 
                    help='Source file name source.txt')

args = parser.parse_args()

filename = args.source

nouns1 = nltk.data.load('classes.txt')
classnouns = word_tokenize(nouns1)
# print(classnouns)

nouns2 = nltk.data.load('attributes.txt')
attributenouns = word_tokenize(nouns2)

# dataset = nltk.data.load('inputData.txt')

# dataset = nltk.data.load('k3data.txt')
# print(dataset)

dataset = nltk.data.load(filename)

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

cnames = []
attributes = dict({})
references = dict({})


for sq in possq : 
  ents = entities(sq)
  # print(">> Entities of " + str(sq) + " are " + str(ents))
  # print("") 
  for e in ents :
    if hasClassNoun(e) and not(hasAttributeNoun(e)) :
      enme = className(e)
      if enme in cnames : 
        attrs = attributes[enme]
        refs = references[enme]
      else : 
        attrs = []
        attributes[enme] = attrs
        refs = []
        references[enme] = refs
        cnames.append(enme)
      for s in ents : 
        if s != e and hasClassNoun(s) : 
          refnme = className(s)
          if len(refnme) <= 1 or (refnme in refs) or (refnme == enme): 
            pass 
          else : 
            refs.append(refnme)
        else :
          if s != e :
            attnme = className(s)
            if len(attnme) <= 1 or (attnme in attrs) or (attnme == enme): 
              pass 
            else : 
              attrs.append(attnme)
          

print("package app {")

for cls in cnames : 
  print("class " + cls + " { ")
  atts = attributes[cls]
  for att in atts :
    print("  attribute " + att.lower() + " : String;")
  refs = references[cls]
  for ref in refs :
    if ref in cnames : 
      print("  reference " + ref.lower() + " : " + ref + ";")
    else :
      print("  reference " + ref.lower() + " : OclAny;")
  print("}") 
  print("")
  
print("}")

  # print(hasVerb(sq))

# vbsq = [sq for sq in possq if hasVerb(sq)]
# print(vbsq)

# for sq in vbsq :
#   (np,vp,rem) = npvpremChunk(sq)
  # print((np,vp,rem))
#  actr = actor(np)
#  ucname = usecaseName(vp,rem)
#  category = "other"
#  if len(rem) > 0 : 
#    tple = rem[0]
#    category = verbCategory(tple[0],verbs)
#  print("usecase " + ucname + " { actor = " + actr + "; stereotype = \"" + category + "\"}")
#  print("")




# chunking: "<DT>?<JJ>*<NN.*>"

# rrss = ['Each', 'retail', 'unit', 'has', 'an', 'area', 
#         ',', 'location', ',', 'and', 'price']

# ss = pos_tag(rrss)

# print(ss)

# print(entities(ss))

def string_distance(s1,s2) : 
  if len(s1) == 0 and len(s2) == 0 : 
    return 0
  sumlengths = len(s1) + len(s2)
  dx = edit_distance(s1, s2)
  return dx/sumlengths

# print(string_distance("play", "plays"))

