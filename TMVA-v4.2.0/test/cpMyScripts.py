#!/user/bin/env python
import os as os

myScripts = ["cpMyScripts.py",
             "BJetRegressionApplication.C",
             "TMVAClassification_new.py",
             "compareBDTEfficiency.py",
             "TMVAClassification_EWK.py",
             "TMVAClassification_QCD.py",
             "TMVAClassificationApplication_new.C",
             "runClassification.py",
             "TMVAClassification_both.py",
             "BDTInputVarsList.py",
             "runBDTClassification.py",
             "runRegression.py",
]

for iScript in myScripts:
    command = "cp %s /afs/hep.wisc.edu/home/zmao/myScripts/H2hh2bbTauTau/TMVA" %iScript
    os.system(command)
