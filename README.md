# Diploma Thesis
- Author: Domnik Kouba
- Used template: [here](https://github.com/macekond/k336_sablona)
- Used VS code and https://github.com/James-Yu/LaTeX-Workshop
- https://arxiv.org/pdf/1612.04888.pdf
- https://academia.stackexchange.com/questions/112111/how-to-improve-the-language-of-my-master-thesis-by-myself
- LATEX
  - https://github.com/dspinellis/latex-advice
  - https://rvprasad.medium.com/a-git-workflow-for-writing-papers-in-latex-4cfb31be4b06
  - /citet, /citep, /citeathor, \cite[p.~8]{LR89}
  - https://www.doi2bib.org/



# Writing notes
- Passive or we talking about what wehave done or seen... (checked in Madlik, Pevny)

# Plan
- DEADLINE: 21.5. 2021 -> have to be handed in printed on Department
- 22.3. week
  - Close up (code) - Single label and multilabel, have to have results or everything to retrieve them (as much as possible!!) - different kinds of signatures
    - if multilabel will suck, skip it and just mention experiments and code
  - Research for chapters
    - classification, hmill, explain_theory
    - find sources and ideally read through
  - Explaining - code
- 29.3. week
  - End up explaining part
  - Write chapters - data, classification, hmill, explain_theory
- 5.4. week
  - Chapters - data, model, explain_experiments
- 12.4. week
  - Final discussion about results from 3 chapters
  - Try to finalize everything so far having
    - ML stuff
- 19.4. week
  - Final adjustment in ML par
  - Research Malware analysis, start writing this chapter
- 26.4 week
  - Malware analysis chapter and infrastructure
  - Try to end it up
- 3.5. week
  - order printing!
  - introduction, conclusions, discussion (see one note sheet)
  - code completion - attachement
  - final adjustments
- 10.5. week
  - final adjustments
- 17.5. week
  - English last adjustments, send to print it
  - 21.5. 2021 - FRIDAY, LAST DAY



# TODO
- Division into parts I do not have to have later, this is just convenient to use
- mention all atempts!! even not succesful, like slow convergence in case of some classifier, report even results
- Are there another datasets?? It woiuld be great to compare my results and another
  - https://scholar.google.com/scholar?hl=cs&as_sdt=0%2C5&q=malware+classification+&btnG=
- Write even about unsuccesful attempts, for example data were too complex and we are not able to learn single classifier, so we have to prune the data more
- Use resources stated in thesis assignment
- Metrics in multiclass classification and even in multilabel multiclass example
- Cross validation?
- Thanks to Mr Mandlik

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
------------ 
- (rather more chapters than two big parts, just remove the top levels if there are only 2)
- (Each problem - theory, prior, my usecase/application)
- Malware analysis, infrastructure and data analysis (maybe more chapters, add what ever to appendices, used technology stack...)
- Malware classification
- Hmill

- Dataset structure, features and hiden states

- (I would like to draw the theory at the beginning of each part and then say what practically was done)
- Modelling
  
- Explaining

- Evaluation and discussion
  - GOAL - Evaluate the results of the experiment. ("Vyhodnoťte", ne "ověřte"!!)
 

-----------

2. Conclusion





# Resources
- Malware classification using hmill and its comparison to another approaches
  - https://pdf.sciencedirectassets.com/271506/1-s2.0-S0957417417X00213/1-s2.0-S0957417417307170/main.pdf?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEJD%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJIMEYCIQDyBj8Se%2FpspGjTRG7wTNb3MNwKD9vXXIB3CjmLvPzmNwIhAN%2Fk6IUDRJcqpbW%2FLyaUZ0eHS8yk5G8j1mW4h5YkEP%2BYKr0DCKj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQAxoMMDU5MDAzNTQ2ODY1Igxqz%2B2GxANt4v%2FuUj8qkQM6ZMY1DTOw7yxSDw7RhlVqc%2BqfbaQZ9H0e0JLicueV1d96WcCmRzQwAfGSS2GTPlW%2BMFJyYs1DAtABhE3tnwI99ZeA95tCV9CxjPFGCJc8V8M6%2F8R2Q6fH0hWyZ%2B4pCbVtjcr%2F6ft84EszEiQmHj6DyLy%2F7cCTXhB3OiTPFEWx%2FPfUq0zwlgSgoRiE3i3WtJFlhP%2B%2FJELmmseb10vB37ci1qGMWvVOBO5kZVAZMcvVhSDaeudc%2Fw2Fn5VOiCbvfTExUwxqJb6nxsKAxc57fkntGdDVl7iRiM9xOexuvKpDU8BuKLleyEkUp8yVx6FKLtnC85V1TW7nHYEh0cO5Y1TkuHE78l8r%2B%2FDm5iooma%2yyB66SNFT%2BE55AKj4D%2Beu%2FNnEBn1VaY54oilIk1UxuoZIJJ9OoOr1i1usMKukzWoabJFata4%2FHPWEhlKCA97BrzLQ56hA5BobzqDB%2BhGZUR4kiEnQiEqKIs0Wbc1eWLY4WNbCmlLg2ZJGjohgisoXI4cPouTTstHCVxWlvzyE718TGQZWTCJrfmBBjrqAfPsH%2BgWSfzZsvUJ%2Bv85WCHI2MfmQ%2FQARLEVRXK%2F2BrpdFOcIkripQfssYFEeIGOz%2F246oBQA3mPc0NYT%2FvRoWNS4ZW7WazhlG%2FygE6nGbtFfil%2BLnekh9tyZ5BCG1c4iOPrjMZaAOCBGTexg%2FNVrMpy%2F4t7IqOslYIAmDOljHIf4HzgW7BbgmC%2FUjlghTlOH271PVDcx9WWr7hnbBVfRILPm2LsyV89v4jP2RADHCKiTVafcjclo5TQUs4EZD6uO6i%2Bhjbule%2F1AC9jhb0aJKvGBYHsONa3ZLx2db8jyecl81V2%2FjvADzvJEA%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210302T161641Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIAQ3PHCVTYQAWIGSX2%2F20210302%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=d2c570eb37501f94b12d4d31b3200f766df83d297453bb67175424bda2c0aacb&hash=e26708acf069241c8a25ff5e1d9818b0253735fd0e51d99a91f0933465f25015&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S0957417417307170&tid=spdf-28109fdb-8953-4a32-adec-d4301b2a369a&sid=eac2c51846482343fa3bfdc5f6bd5f797c65gxrqb&type=client

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
- https://www.researchgate.net/profile/Mohammad-Hossin/publication/275224157_A_Review_on_Evaluation_Metrics_for_Data_Classification_Evaluations/links/57b2c95008ae95f9d8f6154f/A-Review-on-Evaluation-Metrics-for-Data-Classification-Evaluations.pdf
  - nice table, but mistake in definition of Recall
  - Accuracy/error rate - do not respect unbalanced datasets, 90% accuracy in case of the data set where 90% of samples is in one class could be classifier which classifies only one clas for all (but what mistakes in the other classes are much worse than in the first one...)
  - sensitivity/specificity - fraction of positive/negative examples correctly classfied - this can be indicator of those disbalances between false negative or false positive...
  - Precision - positive patterns that are correctly predicted from all that are predicted positive - (1 => all classes predicted positively are positive, 0 => no class predicted positively is positive) - how many apples are among that what I labeled as apple during prediction; add TP - increase of precision, add FP - decrease precision
    - high precision => we more worry about False positives, we do not want to say cancer if there is change that there is not cancer
  - Recall - fraction of positive patterns that are corectly predicted from all positives - (1 => all positive classes are predicted correctly (no FN), 0 => all positive classes are predicted as false negatives) - how many apples I labeled as apples from all apples in dataset; add TP - increase of recall, add FN - decrease of recall
    - high recall => we more worry about False negatives, we do not want to risk skipping treatment of potentiall cancer
- Precision-recall curve
  - "if the curve is "above" the other, it has better performance" - we can talk about area under the PR curve
  - what we change is treshold of classification (normally classifier returns probabilities) and count recall and precision for different values of treshold
  - https://www.youtube.com/watch?v=W5meQnGACGo (great!!)
- F-score
  - combining recall and precision and stating one real number for classifier comparison - quality (0, 1)
- For evaluation classifier (and maybe ever for choosing optimal treshold for our situation) we can use:
  - PR curve, F-score
  - ROC, AUC curves
  - considerably much more...
- ROC, AUC
  - again we iterating over treshold values and plot points, now for true positive and false positive rate, it is summary of confusion matrices for different value of treshold
  - https://www.youtube.com/watch?v=4jRBRDbJemM&t=503s
  - AUC - something like F-score, again we can compare one ROC to another using one number, the bigger AUC the better
- different metrics are suitable in defferent cases
  - Precision-recall curve does not use True negatives, so it is suitable for unbalanced datasets with huge number of true negatives, or where we just do not care about true negatives
  - ...
- Balanced accuracy
  - https://statisticaloddsandends.wordpress.com/2020/01/23/what-is-balanced-accuracy/
  - TNR + TPR / 2
- Number of samples and FPR and FNR - https://www.sciencedirect.com/science/article/pii/S0957417417307170?casa_token=K3yjPO3fKhoAAAAA:nHk2zyxfKHkVF4z9HL5t0iZD91ma_0pxi18iI2sI3HSy15x36FVLWF7X64TmAt054-dX-ksw1g#fig0003
## What to watch during learning process
- Loss through epochs?
- Training X testing/validation accuracies and other metrics

