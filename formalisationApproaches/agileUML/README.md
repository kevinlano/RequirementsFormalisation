This directory contains the AgileUML tools for RF of behavioural and data models. This is described in the paper

"Automated Requirements Formalisation for Agile MDE", K. Lano et al, at MDEIntelligence 2021, MODELS 2021. 
https://www.researchgate.net/publication/357212983_Automated_Requirements_Formalisation_for_Agile_MDE


The tool is opened as 
java -jar umlrsds.jar

The "File" menu option "Formalise behaviour requirements" takes as input a POS-tagged file 
output/tagged.txt with the format of one sentence per user story, separated by at least one blank line. 

Eg: 
As_IN a_DT DevOps_NNP engineer_NN ,_, 
I_PRP want_VBP New_NNP Relic_NNP to_TO provide_VB useful_JJ data_NNS across_IN all_DT applications_NNS ._.

As_IN ....

The output is written to output/mm.km3
(this can be viewed by the File menu option "Load metamodel => Load km3")

The POS-tagged file can be produced by Stanford NLP or Apache NLP, eg:

java -mx300m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -model models/english-bidirectional-distsim.tagger -textFile infile.txt > outfile.txt




The "File" menu option "Formalise data requirements" takes as input a tagged and parsed file output/nlpout.txt with the format produced by Stanford NLP parsing: 

java -Xms1800m -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLP -annotators tokenize,ssplit,pos,lemma,ner,parse -file input.txt

The output/background.txt glossary is also needed. The resulting model is written to output/mm.km3


