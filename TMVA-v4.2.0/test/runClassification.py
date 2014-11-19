#!/user/bin/env python

import os as os

fileList = ['H2hh260_all',
            'H2hh270_all',
            'H2hh280_all',
            'H2hh290_all',
            'H2hh300_all',
            'H2hh310_all',
            'H2hh320_all',
            'H2hh330_all',
            'H2hh340_all',
            'H2hh350_all',

            'tt_all',
            'tt_semi_all',
            'ZZ_all',
            'dataTotal_all',

            'DY1JetsToLL_all',
            'DY2JetsToLL_all',
            'DY3JetsToLL_all',
            'W1JetsToLNu_all',
            'W2JetsToLNu_all',
            'W3JetsToLNu_all',
            'WZJetsTo2L2Q_all',
#             'QCD_Pt-50to80',
#               'VBF_HToTauTau',
#               'GluGluToHToTauTau',
#               'WH_ZH_TTH_HToTauTau',
#               'TTJets_MSDecays',

            ]
# massPoints = ['260', '300', '350']

massPoints = ['260', '270','280','290','300','310','320','330','340', '350']
nVars = [7]

outputLocation = '/scratch/zmao/BDTStudy/7_mJJ/'

for iNVars in nVars:
    for massPoint in massPoints:
        location = '/scratch/zmao/v3/'
        oLocation = '%s%s/' %(outputLocation, massPoint)
        if not os.path.isdir(oLocation):
            os.makedirs(oLocation)
        for iFile in fileList:
        #     rootCommand = "root -l -q  BJetRegressionApplication.C\(\\\"BDTG\\\",\\\"%s_all.root\\\",\\\"%s\\\"\)" %(iFile, location)
        #     os.system(rootCommand)    
        #     rootCommand = "root -l -q  TMVAClassificationApplication_new.C\(\\\"BDT\\\",\\\"TMVARegApp_%s_all.root\\\",\\\"EWK\\\",\\\"%s\\\",\\\"%s\\\"\)" %(iFile, location, massPoint)
        #     os.system(rootCommand)
        #     rootCommand = "root -l -q  TMVAClassificationApplication_new.C\(\\\"BDT\\\",\\\"ClassApp_EWK_TMVARegApp_%s_all.root\\\",\\\"QCD\\\",\\\"%s\\\",\\\"%s\\\"\)" %(iFile, location, massPoint)
        #     os.system(rootCommand)
            rootCommand = "root -l -q  TMVAClassificationApplication_new.C\(\\\"BDT\\\",\\\"TMVARegApp_%s.root\\\",\\\"both\\\",\\\"%s\\\",\\\"%s\\\",\\\"%s\\\"\)" %(iFile, location, massPoint, oLocation)
            os.system(rootCommand)
