#!/usr/bin/env python
import os as os
import varsList
def reWriteRankFile(inputFile):

    lines = open(inputFile, "r").readlines()
    ofile = "%s_fix.txt" %inputFile[0: inputFile.rfind(".txt")]
    output = open(ofile, "w")
    output.writelines(" massPoint: %s            nVars %s\n" %(massPoint, nVars))
    output.writelines(" --------------------------------------------------\n")
    for i in range(0, len(lines)):
        current_line = lines[i]
        cutPosition = current_line.find(":")
        BDT = current_line.find("--- BDT                      :")
        if BDT == -1:
            output.close()
            print "file saved at: %s" %ofile

            return 1
        current_line = current_line[cutPosition+1:len(current_line)]
        output.writelines(current_line)
    

varList = varsList.varList

nVars = str(len(varList))
nVars += ""

massPoints = ["260", "300", "350"]
# massPoints = ["260", "270", "280", "290", "300", "310", "320", "330", "340","350", "500","700"]
appendName = '_n150_1M'

for massPoint in massPoints:

    command1 = "python TMVAClassification_both.py -i %s | grep \"Variable Importance\" -A 20 > /scratch/zmao/TMVA/new3/varsRank%s_%s%s.txt" %(massPoint, massPoint, nVars, appendName)
    command2 = "mv TMVA.root /scratch/zmao/TMVA/new3/TMVA%s_%s%s.root" %(massPoint, nVars, appendName)

    os.system(command1)
    os.system(command2)
    reWriteRankFile("/scratch/zmao/TMVA/new3/varsRank%s_%s%s.txt" %(massPoint, nVars, appendName))
    print 

