# Diploma Thesis
- Author: Domnik Kouba
- Used template: [here](https://github.com/macekond/k336_sablona)
- Used VS code and https://github.com/James-Yu/LaTeX-Workshop
- LATEX
  - https://github.com/dspinellis/latex-advice
  - https://rvprasad.medium.com/a-git-workflow-for-writing-papers-in-latex-4cfb31be4b06
  - /citet, /citep, /citeathor, \cite[p.~8]{LR89}
  - https://www.doi2bib.org/

# TODO

# Table of contents
- Write even about unsuccesful attempts, for example data were too complex and we are not able to learn single classifier, so we have to prune the data more
- write about sandboxing theory and everything around
  - https://cybersecurity.att.com/blogs/labs-research/malware-exploring-mutex-objects
  -  https://bazaar.abuse.ch/sample/58b16ea474c6ae74987e0704c6af2468b463ef0c8c652777b227900d182655c4/ 
      - some metadata from here?
     -  https://bazaar.abuse.ch/api/#upload - API
     - There is even origin of the file
- Learning - each part - Hmill, model, experiments, evaluation...
- minibatches why are they randomly sampled from training set?
   - https://machinelearningmastery.com/gentle-introduction-mini-batch-gradient-descent-configure-batch-size/


# Thesis assignment
The thesis aims to capture and analyze artifacts of malware execution in a protected environment and assess if these artifacts can be used to predict malware functionalities and capabilities. 

## Goals:
1. Run several instances of CapeV2 sandbox and solve their orchestration for this experiment
2. Capture behavior of selected malware samples in CapeV2 sandbox and store results
3. Learn the hierarchical multiple instance learning framework (HMill)
4. Analyze captured data. Report basic statistics and choose appropriate features and hidden states for further modeling. 
5. Using HMill, create models, and identify the artifacts corresponding to different malware behavior. Report results. 
6. Investigate which parts of the CapeV2 log are important to different malware behavior. 
   - Explainer project (?) 
   - Ask Thorsten to try to explain some patterns and domain specific subjects 
   - Důležité: predikce signatures a jejich vysvětlení, feedback od Thosrten k vysvětlitelnosti, jestli to jako souhlasí s realitou 
7. Evaluate the results of the experiment. ("Vyhodnoťte", ne "ověřte"!!)


# Table of contents
**What, Why, How, Who, When**

1. Introduction - **What** are we trying to do and **Why**. How we are going to describe it.
   - motivation - ??
   - goals
   - structure of the thesis
------------ 
- (rather more chapters than two big parts, just remove the top levels if there are only 2)
- (Each problem - theory, prior, my usecase/application)
- Malware analysis, infrastructure and data analysis (maybe more chapters, add what ever to appendices, used technology stack...)
  - Introduction
  - GOALS
    - Run several instances of CapeV2 sandbox and solve their orchestration for this experiment
    - Capture behavior of selected malware samples in CapeV2 sandbox and store results
  - Theory part - types, conditions, bias...
  - Sandboxing
  - Previous experiments
  - Our goal in this part
  - Data collection for ML purposes in general
  - Realization
    - our infrastructure - distribution, other types of analyses, network infrastructure (marginally, I am not going to use those data, I think)
    - used tools
    - pipeline
    - run
    - results
  - Conclusions, comming-outs, summary, discussion
- Malware classification
  - Classification problems
    - Theory
    - Single label, multilabel
    - evaluation of classifiers
  - General approaches to malware classfication - theory
    - based on dynamic/static anysis results...
    - (one of them should be using neural nets - describe deeply usage of loss function in both cases - single label, multi label...)
      - hyper parameters...
      - minibatch gradient descent, gradient descent itself

  - Prior work
- Hmill
  - GOALS 
    - Learn the hierarchical multiple instance learning framework (HMill)
  - describe theory, connect it to classical approach
  - Usual usage of this type of learning - classification, regression...
  - Our usecase and experiments with this kind of learning in malware classification field (prior)
- Dataset structure, features and hiden states
  - (theory for basic statistcs, but maybe not)
  - GOALS
    - Analyze captured data. Report basic statistics and choose appropriate features and hidden states for further modelling
  - dataset structure
  - basic statistics - histogram...
  - On Hmill usage - features, hidden states (Section for each, description)
  - Signatures - hidden states
  - Features  desription
  - Maybe try to extract more candidates (But I would have to perform several more experiments, but data pruning should not be problem)
- (I would like to draw the theory at the beginning of each part and then say what practically was done)
- Modelling
  - Used technologies, several experiments, pseudocode, hyper parameters, report evaluation metrics,types of classifiers used (motivation for that) COMPARISON WITH PRIOR ALTERNATIVES?
  - Modelling - single label classifier
    - GOAL: Using HMill, create models. Report results.
  - Modelling - multi label classifier
    - GOAL: Using HMill, create models. Report results.
  - Performance, early stopping, hyper parameters...
- Explaining
  - Goal 
    - identify the artifacts corresponding to different malware behavior. Report results.
    - Investigate which parts of the CapeV2 log are important to different malware behavior. 
  - theory to model explaining and feature extraction
  - Approaches:
    - Existing solutions - avast explainer, other?
    - Signatures and their implementation, what they identify (Yara and others, used by sandbox...)
    - Maybe I can try some alternative approach - simple diff on jsons?
    - Expert view
      - Ask Thorsten to try to explain some patterns and domain specific subjects 
      - Důležité: predikce signatures a jejich vysvětlení, feedback od Thosrten k vysvětlitelnosti, jestli to jako souhlasí s realitou 
- Evaluation and discussion
  - GOAL - Evaluate the results of the experiment. ("Vyhodnoťte", ne "ověřte"!!)
 

-----------

2. Conclusion
  - goals and their achivement, results, outputs
  - future work
  - thanks to

## Theory:
- Maware analysis in general
  - Sandboxing itself
- Classification problems
  - single label, multi label
- Neural nets
- Hmill
- Modelling
  - Training, Testing
  - Early stopping....
- Model Evaluation - metrics,...
- Model Explanation

## Infrastructure
- Distribution part of Cape Sandbox

# Notes:
- Another experiments with all the stuff - dynamic analyses collection, malware/signatures classification, e. g. Mandlik's work 
- Bias in practical data like this - security data, what are the influences
- I should discuss the results
- Couple of words about
- Other used sorces like virus total and so on
- Original signature in python, intution behind the inteerpretation of results
- Balanced dataset - in term of accuracy metric performance
- Alternative approaches to classification
- Malware types, signatures...
- Previoius work on classification - prior
- Sample structure
- It could be great to have even cleanware samples... (https://researchoutput.csu.edu.au/en/publications/differentiating-malware-from-cleanware-based-on-behavioural-analy)

	- Experiments:
		-  Single signature
		-  Multi signature (multilabel)
			§ Try extract labels, then I can choose only some of signatures
			§ Use binary cross entrophy, change implemententation of accuracy
  - Explainning
		
	- Evaluation
		- https://www.kdnuggets.com/2017/04/must-know-evaluate-binary-classifier.html
		- https://medium.com/analytics-vidhya/accuracy-vs-f1-score-6258237beca2
		- https://sites.icmc.usp.br/gbatista/files/laptec2003.pdf
		- https://towardsdatascience.com/metrics-to-evaluate-your-machine-learning-algorithm-f10ba6e38234
		- Single label
			- F-score, train accuracy, test accuracy, loss function, plots
			- AUC, ROC?
		- When to stop learning?
			- Check ovefitting
	- Is it number of epochs or number of iterations?
		-  Report it and even time
		-  Use @epochs?
	- Early stopping
		-  https://machinelearningmastery.com/early-stopping-to-avoid-overtraining-neural-network-models/
		-  Hyper parametrs?
			§ Epochs, iterations,…
	- Validation set
		-  Train hyperparameters
		-  Validate model performace 9early stopping…)
https://medium.com/@yixinsun_56102/understanding-generalization-error-in-machine-learning-e6c03b203036

## Evaluation
- Confusion matrix


