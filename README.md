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
- Are there another datasets?? It woiuld be great to compare my results and another
- Write even about unsuccesful attempts, for example data were too complex and we are not able to learn single classifier, so we have to prune the data more
- Use resources stated in thesis assignment


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
   - motivation
    - Motivation behind the modelling itself (classifying itself)
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
  - Theory part - types, conditions, bias, Malware types, signatures....
  - Sandboxing
  - Previous experiments
  - Our goal in this part
  - Data collection for ML purposes in general
  - Realization
    - our infrastructure - distribution, other types of analyses, network infrastructure (marginally, I am not going to use those data, I think, but I performed it and I can write about the risks and so on...)
    - used tools
    - distrbution
    - pipeline
    - run
    - results
  - Conclusions, comming-outs, summary, discussion
- Malware classification
  - Classification problems
    - Theory
    - Single label, multilabel
    - evaluation of classifiers
      - Confusion matrix
      - F-score, train accuracy, test accuracy, loss function, plots
			- AUC, ROC?
      - What is important metric during malware classification and why
    - (Overfitting, early stopping)
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
  - What kind of data we have - mention all parts of cuckoo log, mention even virus total reports
  - (theory for basic statistcs, but maybe not)
  - GOALS
    - Analyze captured data. Report basic statistics and choose appropriate features and hidden states for further modelling
  - dataset structure
    - Bias in practical data like this - security data, what are the influences
    - Balanced dataset - in term of accuracy metric performance
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
    - Signatures and their implementation (python), what they identify (Yara and others, used by sandbox...)
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

# Resources
- Sandbox
  - Cuckoo Sandbox Overview and Demo
  - https://github.com/volatilityfoundation/volatility
  - The Malware CAPE: Automated Extraction of Configuration and Payloads from Sophisticated Malware
  - https://medium.com/@soji256/build-a-cape-sandbox-to-analyze-emotet-3d507599dda6
  - https://en.wikipedia.org/wiki/Portable_Executable
  - https://github.com/kevoreilly/community
- Mandlik's work 
- Pevny's work
- Multilabel
  	- https://en.wikipedia.org/wiki/Multi-label_classification
		- https://stats.stackexchange.com/questions/12702/what-are-the-measure-for-accuracy-of-multilabel-data
		- https://fluxml.ai/Flux.jl/stable/models/losses/
		  -  Classical crossentrophy is design to have onehot encoded target, penalty is counted only for true label position
		  -  Binary crossentrophy https://stackoverflow.com/questions/59336899/which-loss-function-and-metrics-to-use-for-multi-label-classification-with-very

- Evaluation
  - https://www.kdnuggets.com/2017/04/must-know-evaluate-binary-classifier.html
  - https://medium.com/analytics-vidhya/accuracy-vs-f1-score-6258237beca2
  - https://sites.icmc.usp.br/gbatista/files/laptec2003.pdf
  - https://towardsdatascience.com/metrics-to-evaluate-your-machine-learning-algorithm-f10ba6e38234
- Early stopping and ovefitting
  -  https://machinelearningmastery.com/early-stopping-to-avoid-overtraining-neural-network-models/
  - https://medium.com/@yixinsun_56102/understanding-generalization-error-in-machine-learning-e6c03b203036
- write about sandboxing theory and everything around
  - https://cybersecurity.att.com/blogs/labs-research/malware-exploring-mutex-objects
  -  https://bazaar.abuse.ch/sample/58b16ea474c6ae74987e0704c6af2468b463ef0c8c652777b227900d182655c4/ 
      - some metadata from here?
     -  https://bazaar.abuse.ch/api/#upload - API
     - There is even origin of the file
- minibatches why are they randomly sampled from training set?
   - https://machinelearningmastery.com/gentle-introduction-mini-batch-gradient-descent-configure-batch-size/
- Original sources
  1. Jan Stiborek, Tomáš Pevný, and Martin Rehák. „Multiple instance learning for
  malware classification“ Expert Syst. Appl. 93, C (March 2018), 346–357, 2018.
  2. Digit Oktavianto and Iqbal Muhardianto. „Cuckoo Malware Analysis“. Packt
  Publishing, 2013.
  3. T. Pevnýand P. Somol, „Using neural network formalism to solve multipleinstance
  problems,” in International Symposium on Neural Networks, pp.
  135–142, Springer, 2017.
  4. S. Mandlik, „Mapping the Internet — Modelling Entity Interactions in Complex
  Heterogeneous Networks (diploma thesis)“, 2020.
  5. Wang C., Ding J., Guo T., Cui B. „A Malware Detection Method Based on
  Sandbox, Binary Instrumentation and Multidimensional Feature Extraction“. In:
  Barolli L., Xhafa F., Conesa J. (eds) Advances on Broad-Band Wireless
  Computing, Communication and Applications. BWCCA 2017. Lecture Notes on
  Data Engineering and Communications Technologies, vol 12. Springer, Cham., 2018.
- Web sources
  	- Summary of potential sorces of metadata
		- Abuse.ch - https://bazaar.abuse.ch/api/#api_key
		- VirusTotal - https://developers.virustotal.com/v3.0/reference#file-info
		- Metadefender - https://onlinehelp.opswat.com/mdcloud/3.1_Retrieving_scan_reports_using_a_data_hash.html
	- Interesting
		- https://app.any.run/
		- https://virusscan.jotti.org/
		- https://virscan.org/
		- https://mzrst.com/
		- https://github.com/maliceio/malice
    - https://www.hybrid-analysis.com/
    - https://www.shodan.io/
    - https://www.av-comparatives.org/
    - https://www.av-test.org/

# Remains:
- It could be great to have even cleanware samples... (https://researchoutput.csu.edu.au/en/publications/differentiating-malware-from-cleanware-based-on-behavioural-analy)


# Concrete NOTES
## Model evaluation
- 