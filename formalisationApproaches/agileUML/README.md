This directory contains the AgileUML tools for RF of behavioural models. 
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



