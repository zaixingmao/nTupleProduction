#!/user/bin/env python

import os as os

fileList = [ # 'H2hh260',
#            'H2hh300',
#            'H2hh350',
           'H2hh270',
           'H2hh280',
           'H2hh290',
           'H2hh310',
           'H2hh320',
           'H2hh330',
           'H2hh340',
           'H2hh500',
           'H2hh700',
#            'tt_eff',
#            'tt_semi_eff',
#            'ZZ_eff',
#            'DY1JetsToLL_eff2',
#            'DY2JetsToLL_eff2',
#            'DY3JetsToLL_eff2',
#            'W1JetsToLNu_eff2',
#            'W2JetsToLNu_eff2',
#            'W3JetsToLNu_eff2',
#            'WZJetsTo2L2Q_eff',
#            'dataTotal',
#             'QCD_Pt-50to80',
#               'VBF_HToTauTau',
#               'GluGluToHToTauTau',
#               'WH_ZH_TTH_HToTauTau',
#               'TTJets_MSDecays',

            ]
location = '/scratch/zmao/triggerMatch/'

for iFile in fileList:
    rootCommand = "root -l -q  BJetRegressionApplication.C\(\\\"BDTG\\\",\\\"%s_all.root\\\",\\\"%s\\\"\)" %(iFile, location)
    os.system(rootCommand)    
