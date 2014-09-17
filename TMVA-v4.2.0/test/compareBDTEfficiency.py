#!/usr/bin/env python
import ROOT as r
from operator import itemgetter
import tool
import math
import optparse
import os
from array import array



effList_2D = []
effList_both = []

iFileList = [('BDTEfficiency.root',r.kBlue), ('BDTEfficiency_8.root', r.kRed)]

for i in range(len(iFileList)):
    iFile = iFileList[i][0]
    ifile = r.TFile(iFile)
    iTree = ifile.Get("eventTree")
    effList_2D.append(ifile.Get("eff_2D"))
    effList_both.append(ifile.Get("eff_both"))
    effList_2D[i].SetLineColor(iFileList[i][1])
    effList_both[i].SetLineColor(iFileList[i][1])

psfile = 'BDT_Eff_diff.pdf'
c = r.TCanvas("c","Test", 800, 600)
effList_2D[0].Draw()
for j in range(1, len(iFileList)):
    effList_2D[j].Draw('same')
c.Update()
c.Print('%s(' %psfile)
c.Clear()

effList_both[0].Draw()
for j in range(1, len(iFileList)):
    effList_both[j].Draw('same')
c.Update()
c.Print('%s)' %psfile)

print 'plot saved at: %s' %psfile