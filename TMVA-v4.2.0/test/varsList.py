#!/usr/bin/env python

# varList = ['svMass', 'dRTauTau', 'dRJJ', 'svPt', 'dRhh', 'met', 'mJJReg', 'metTau1DPhi', 'metTau2DPhi', 
#                 'metJ1DPhi', 'metJ2DPhi', 'metTauPairDPhi', 'metSvTauPairDPhi', 'metJetPairDPhi','CSVJ1', 'CSVJ2', 'fMassKinFit', 'chi2KinFit']

# varList = ['svMass', 'dRJJ', 'metSvTauPairDPhi', 'mJJReg', 'met', 'metJetPairDPhi', 'fMassKinFit', 'svPt']

# varList = ['svMass', 'dRTauTau', 'dRJJ', 'met', 'mJJReg', 'metJ2DPhi', 'fMassKinFit', 'chi2KinFit']
varList = ['svMass1', 'dRTauTau', 'dRJJ', 'met1', 'mJJReg', 'metJ2DPhi', 'fMassKinFit', 'chi2KinFit2']
# varList = ['svMass', 'dRTauTau', 'dRJJ', 'met', 'mJJ', 'fMassKinFit', 'chi2KinFit2']

# varList = ['svMass','met', 'mJJReg','chi2KinFit2']

# varList = ['svMass', 'mJJ']


# varList = ['svMass', 'dRTauTau', 'dRJJ', 'svPt', 'mJJReg', 'ptJJ']

# varList = ['svMass', 'dRTauTau', 'dRJJ', 'mJJReg', 'ptJJ']
# 
# varList = ['svMass', 'dRTauTau', 'dRJJ', 'mJJReg', 'svPt']
# 
# varList = ['svMass', 'dRTauTau', 'dRJJ', 'mJJReg', 'fMass']
# 
# varList = ['svMass', 'mJJ', 'chi2KinFit']

scaleFactors = {'bTag': 0.051,
                '1M1NonM': 0.0498,
                '2M': 0.0507,
                '1M': 0.0499*0.9902}

Lumi = 19.7
region = '1M'
location = "/scratch/zmao/v3/"
bkg = []
preFix = location + 'TMVARegApp_'
postFix = '_tightopposite%s3rdLepVeto' %region

bkg = [('ZZ', 'ZZ_all%s.root' %postFix),
        ('WZ', 'WZJetsTo2L2Q_all%s.root' %postFix),
        ('W1', 'W1JetsToLNu_all%s.root' %postFix),
        ('W2', 'W2JetsToLNu_all%s.root' %postFix),
        ('W3', 'W3JetsToLNu_all%s.root' %postFix),
        ('DY1', 'DY1JetsToLL_all%s.root' %postFix),
        ('DY2', 'DY2JetsToLL_all%s.root' %postFix),
        ('DY3', 'DY3JetsToLL_all%s.root' %postFix),
        ('tt_full','tt_all%s.root' %postFix),
        ('tt_semi','tt_semi_all%s.root' %postFix),
        ('QCD','dataTotal_all_relaxedopposite%s3rdLepVeto.root' %region)]