This directory contains tools for the evaluation of formalised requirements: 

(1) compareModels.bat referencemodel solutionmodel
compares a reference solution referencemodel.km3 of a requirements formalisation task, to a candidate solution derived by a formalisation
approach, in solutionmodel.km3
A measure of similarity of the classes, attributes and usecases of the two models is given, ranging from 0 to 1

(2) python compareModel2Source.py --source source.txt --model model.km3
compares the solution model in model.km3 to the original requirements source text in source.txt, and computes the fraction of source verbs and 
nouns which appear in appropriate elements of the target model. 

(3) python checkModelNames.py --model model.km3
evaluates the internal quality of the candidate solution model  model.km3
