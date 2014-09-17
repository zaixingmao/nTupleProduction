#!/usr/bin/env python
# @(#)root/tmva $Id$
# ------------------------------------------------------------------------------ #
# Project      : TMVA - a Root-integrated toolkit for multivariate data analysis #
# Package      : TMVA                                                            #
# Python script: TMVAClassification.py                                           #
#                                                                                #
# This python script provides examples for the training and testing of all the   #
# TMVA classifiers through PyROOT.                                               #
#                                                                                #
# The Application works similarly, please see:                                   #
#    TMVA/macros/TMVAClassificationApplication.C                                 #
# For regression, see:                                                           #
#    TMVA/macros/TMVARegression.C                                                #
#    TMVA/macros/TMVARegressionpplication.C                                      #
# and translate to python as done here.                                          #
#                                                                                #
# As input data is used a toy-MC sample consisting of four Gaussian-distributed  #
# and linearly correlated input variables.                                       #
#                                                                                #
# The methods to be used can be switched on and off via the prompt command, for  #
# example:                                                                       #
#                                                                                #
#    python TMVAClassification.py --methods Fisher,Likelihood                    #
#                                                                                #
# The output file "TMVA.root" can be analysed with the use of dedicated          #
# macros (simply say: root -l <../macros/macro.C>), which can be conveniently    #
# invoked through a GUI that will appear at the end of the run of this macro.    #
#                                                                                #
# for help type "python TMVAClassification.py --help"                            #
# ------------------------------------------------------------------------------ #

# --------------------------------------------
# Standard python import
import sys    # exit
import time   # time accounting
import getopt # command line parser
import tool
import ROOT as r
import os
# --------------------------------------------

# Default settings for command line arguments
DEFAULT_OUTFNAME = "TMVA.root"
DEFAULT_INFNAME  = "tmva_class_example.root"
DEFAULT_TREESIG  = "TreeS"
DEFAULT_TREEBKG  = "TreeB"
DEFAULT_METHODS  = "Cuts,CutsD,CutsPCA,CutsGA,CutsSA,Likelihood,LikelihoodD,LikelihoodPCA,LikelihoodKDE,LikelihoodMIX,PDERS,PDERSD,PDERSPCA,PDEFoam,PDEFoamBoost,KNN,LD,Fisher,FisherG,BoostedFisher,HMatrix,FDA_GA,FDA_SA,FDA_MC,FDA_MT,FDA_GAMT,FDA_MCMT,MLP,MLPBFGS,MLPBNN,CFMlpANN,TMlpANN,SVM,BDT,BDTD,BDTG,BDTB,RuleFit"

# Print usage help
def usage():
    print " "
    print "Usage: python %s [options]" % sys.argv[0]
    print "  -m | --methods    : gives methods to be run (default: all methods)"
    print "  -i | --inputfile  : name of input ROOT file (default: '%s')" % DEFAULT_INFNAME
    print "  -o | --outputfile : name of output ROOT file containing results (default: '%s')" % DEFAULT_OUTFNAME
    print "  -t | --inputtrees : input ROOT Trees for signal and background (default: '%s %s')" \
          % (DEFAULT_TREESIG, DEFAULT_TREEBKG)
    print "  -v | --verbose"
    print "  -? | --usage      : print this help message"
    print "  -h | --help       : print this help message"
    print " "

# Main routine
def main():

    try:
        # retrive command line options
        shortopts  = "m:i:t:o:vh?"
        longopts   = ["methods=", "inputfile=", "inputtrees=", "outputfile=", "verbose", "help", "usage"]
        opts, args = getopt.getopt( sys.argv[1:], shortopts, longopts )

    except getopt.GetoptError:
        # print help information and exit:
        print "ERROR: unknown options in argument %s" % sys.argv[1:]
        usage()
        sys.exit(1)

    infname     = DEFAULT_INFNAME
    treeNameSig = DEFAULT_TREESIG
    treeNameBkg = DEFAULT_TREEBKG
    outfname    = DEFAULT_OUTFNAME
    methods     = DEFAULT_METHODS
    verbose     = False
    for o, a in opts:
        if o in ("-?", "-h", "--help", "--usage"):
            usage()
            sys.exit(0)
        elif o in ("-m", "--methods"):
            methods = a
        elif o in ("-i", "--inputfile"):
            infname = a
        elif o in ("-o", "--outputfile"):
            outfname = a
        elif o in ("-t", "--inputtrees"):
            a.strip()
            trees = a.rsplit( ' ' )
            trees.sort()
            trees.reverse()
            if len(trees)-trees.count('') != 2:
                print "ERROR: need to give two trees (each one for signal and background)"
                print trees
                sys.exit(1)
            treeNameSig = trees[0]
            treeNameBkg = trees[1]
        elif o in ("-v", "--verbose"):
            verbose = True

    # Print methods
    mlist = methods.replace(' ',',').split(',')
    print "=== TMVAClassification: use method(s)..."
    for m in mlist:
        if m.strip() != '':
            print "=== - <%s>" % m.strip()

    # Import ROOT classes
    from ROOT import gSystem, gROOT, gApplication, TFile, TTree, TCut
    
    # check ROOT version, give alarm if 5.18 
    if gROOT.GetVersionCode() >= 332288 and gROOT.GetVersionCode() < 332544:
        print "*** You are running ROOT version 5.18, which has problems in PyROOT such that TMVA"
        print "*** does not run properly (function calls with enums in the argument are ignored)."
        print "*** Solution: either use CINT or a C++ compiled version (see TMVA/macros or TMVA/examples),"
        print "*** or use another ROOT version (e.g., ROOT 5.19)."
        sys.exit(1)
    
    # Logon not automatically loaded through PyROOT (logon loads TMVA library) load also GUI
    gROOT.SetMacroPath( "./" )
    gROOT.Macro       ( "./TMVAlogon.C" )    
    gROOT.LoadMacro   ( "./TMVAGui.C" )
    
    # Import TMVA classes from ROOT
    from ROOT import TMVA

    # Output file
    outputFile = TFile( outfname, 'RECREATE' )
    
    # Create instance of TMVA factory (see TMVA/macros/TMVAClassification.C for more factory options)
    # All TMVA output can be suppressed by removing the "!" (not) in 
    # front of the "Silent" argument in the option string
    factory = TMVA.Factory( "TMVAClassification", outputFile, 
                            "!V:!Silent:Color:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Classification" )

    # Set verbosity
    factory.SetVerbose( verbose )
    
    # If you wish to modify default settings 
    # (please check "src/Config.h" to see all available global options)
    #    gConfig().GetVariablePlotting()).fTimesRMS = 8.0
    #    gConfig().GetIONames()).fWeightFileDir = "myWeightDirectory"

    # Define the input variables that shall be used for the classifier training
    # note that you may also use variable expressions, such as: "3*var1/var2*abs(var3)"
    # [all types of expressions that can also be parsed by TTree::Draw( "expression" )]
    #varList = ['svMass', 'mJJ', 'met/fMass','pZ - pZV']
#     varList = ['svMass', 'fMass', 'dRTauTau', 'dRJJ', 'svPt', 'dRhh', 'met', 'mJJReg',
#                'metTau1DPhi', 'metTau2DPhi', 'metJ1DPhi', 'metJ2DPhi', 'metTauPairDPhi', 'metSvTauPairDPhi', 'metJetPairDPhi','CSVJ1', 'CSVJ2']
    varList = ['svMass', 'dRTauTau', 'dRJJ', 'svPt', 'dRhh', 'met', 'mJJReg', 'metTau1DPhi', 'metTau2DPhi', 
                'metJ1DPhi', 'metJ2DPhi', 'metTauPairDPhi', 'metSvTauPairDPhi', 'metJetPairDPhi','CSVJ1', 'CSVJ2']
#     varList = ['svMass', 'dRTauTau', 'svPt', 'dRhh', 'met', 'mJJReg',
#                 'metTau1DPhi', 'metTau2DPhi', 'metJ2DPhi', 'metJetPairDPhi','CSVJ1', 'CSVJ2']

    for iVar in varList:
        factory.AddVariable(iVar, 'F' )

    iFileSig = TFile.Open("/scratch/zmao/relaxed_regression2/%s" %(infname))
    iFileBkg1 = TFile.Open("/scratch/zmao/relaxed_regression2/TMVARegApp_tt_eff_all.root")
    iFileBkg2 = TFile.Open("/scratch/zmao/relaxed_regression2/TMVARegApp_ZZ_eff_all.root")
    iFileBkg3 = TFile.Open("/scratch/zmao/relaxed_regression2/TMVARegApp_tt_semi_eff_all.root")
    iFileBkg4 = TFile.Open("/scratch/zmao/relaxed_regression2/TMVARegApp_DY2JetsToLL_eff_all.root")
    iFileBkg5 = TFile.Open("/scratch/zmao/relaxed_regression2/TMVARegApp_DY3JetsToLL_eff_all.root")
    iFileBkg6 = TFile.Open("/scratch/zmao/relaxed_regression2/TMVARegApp_W1JetsToLNu_eff_all.root")
    iFileBkg7 = TFile.Open("/scratch/zmao/relaxed_regression2/TMVARegApp_W2JetsToLNu_eff_all.root")
    iFileBkg8 = TFile.Open("/scratch/zmao/relaxed_regression2/TMVARegApp_W3JetsToLNu_eff_all.root")


    sigChain = iFileSig.Get("eventTree")
    bkg1Chain = iFileBkg1.Get("eventTree")
    bkg2Chain = iFileBkg2.Get("eventTree")
    bkg3Chain = iFileBkg3.Get("eventTree")
    bkg4Chain = iFileBkg4.Get("eventTree")
    bkg5Chain = iFileBkg5.Get("eventTree")
    bkg6Chain = iFileBkg6.Get("eventTree")
    bkg7Chain = iFileBkg7.Get("eventTree")
    bkg8Chain = iFileBkg8.Get("eventTree")

    # Global event weights (see below for setting event-wise weights)
    signalWeight     = 1 #0.0159/sigChain.GetEntries() #xs (pb)

    tmpHist = iFileBkg1.Get('preselection')
    ttWeight = 26.2/tmpHist.GetBinContent(1)
    tmpHist = iFileBkg2.Get('preselection')
    ZZWeight = 2.5/tmpHist.GetBinContent(1)
    tmpHist = iFileBkg3.Get('preselection')
    tt_semiWeight = 109.3/tmpHist.GetBinContent(1)
    tmpHist = iFileBkg4.Get('preselection')
    DY2JetsWeight = 181/tmpHist.GetBinContent(1)
    tmpHist = iFileBkg5.Get('preselection')
    DY3JetsWeight = 51.1/tmpHist.GetBinContent(1)
    tmpHist = iFileBkg6.Get('preselection')
    W1JetsToLNu = 5400/tmpHist.GetBinContent(1)
    tmpHist = iFileBkg7.Get('preselection')
    W2JetsToLNu = 1750/tmpHist.GetBinContent(1)
    tmpHist = iFileBkg8.Get('preselection')
    W3JetsToLNu = 519/tmpHist.GetBinContent(1)

    # ====== register trees ====================================================
    #
    # the following method is the prefered one:
    # you can add an arbitrary number of signal or background trees
    factory.AddSignalTree(sigChain, signalWeight)
    factory.AddBackgroundTree( bkg1Chain, ttWeight )
    factory.AddBackgroundTree( bkg2Chain, ZZWeight )
    factory.AddBackgroundTree( bkg3Chain, tt_semiWeight )
    factory.AddBackgroundTree( bkg4Chain, DY2JetsWeight )
    factory.AddBackgroundTree( bkg5Chain, DY3JetsWeight )
    factory.AddBackgroundTree( bkg6Chain, W1JetsToLNu )
    factory.AddBackgroundTree( bkg7Chain, W2JetsToLNu )
    factory.AddBackgroundTree( bkg8Chain, W3JetsToLNu )
    factory.SetSignalWeightExpression('triggerEff')
    factory.SetBackgroundWeightExpression('triggerEff')

    # To give different trees for training and testing, do as follows:
    #    factory.AddSignalTree( signalTrainingTree, signalTrainWeight, "Training" )
    #    factory.AddSignalTree( signalTestTree,     signalTestWeight,  "Test" )
    
    # Use the following code instead of the above two or four lines to add signal and background 
    # training and test events "by hand"
    # NOTE that in this case one should not give expressions (such as "var1+var2") in the input 
    #      variable definition, but simply compute the expression before adding the event
    #
    #    # --- begin ----------------------------------------------------------
    #    
    # ... *** please lookup code in TMVA/macros/TMVAClassification.C ***
    #    
    #    # --- end ------------------------------------------------------------
    #
    # ====== end of register trees ==============================================    
            
    # Set individual event weights (the variables must exist in the original TTree)
    #    for signal    : factory.SetSignalWeightExpression    ("weight1*weight2");
    #    for background: factory.SetBackgroundWeightExpression("weight1*weight2");
    #factory.SetBackgroundWeightExpression( "weight" )

    # Apply additional cuts on the signal and background sample. 
    # example for cut: mycut = TCut( "abs(var1)<0.5 && abs(var2-0.5)<1" )
    mycutSig = TCut( "iso1<1.5 && iso2<1.5 && CSVJ1 > 0.679 && CSVJ2 > 0.244 && abs(eta1)<2.1 && abs(eta2)<2.1 && charge1 + charge2 == 0" ) 
    mycutBkg = TCut( "iso1<1.5 && iso2<1.5 && CSVJ1 > 0.679 && CSVJ2 > 0.244 && abs(eta1)<2.1 && abs(eta2)<2.1 && charge1 + charge2 == 0" ) 
    
    # Here, the relevant variables are copied over in new, slim trees that are
    # used for TMVA training and testing
    # "SplitMode=Random" means that the input events are randomly shuffled before
    # splitting them into training and test samples
    factory.PrepareTrainingAndTestTree( mycutSig, mycutBkg,
                                        "nTrain_Signal=0:nTrain_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )

    # --------------------------------------------------------------------------------------------------

    # ---- Book MVA methods
    #
    # please lookup the various method configuration options in the corresponding cxx files, eg:
    # src/MethoCuts.cxx, etc, or here: http://tmva.sourceforge.net/optionRef.html
    # it is possible to preset ranges in the option string in which the cut optimisation should be done:
    # "...:CutRangeMin[2]=-1:CutRangeMax[2]=1"...", where [2] is the third input variable

    # Cut optimisation

    # Fisher discriminant (same as LD)
#    if "Fisher" in mlist:
        #factory.BookMethod( TMVA.Types.kFisher, "Fisher", "H:!V:Fisher:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )
 #       factory.BookMethod( TMVA.Types.kFisher, "Fisher")

    if "BDT" in mlist:
         factory.BookMethod( TMVA.Types.kBDT, "BDT",
                       "!H:!V:NTrees=150:MinNodeSize=2.5%:MaxDepth=3:BoostType=AdaBoost:AdaBoostBeta=0.5:UseBaggedBoost:BaggedSampleFraction=0.5:SeparationType=GiniIndex:nCuts=-1" )


    # --------------------------------------------------------------------------------------------------
            
    # ---- Now you can tell the factory to train, test, and evaluate the MVAs. 

    # Train MVAs
    factory.TrainAllMethods()

    # Test MVAs
    factory.TestAllMethods()
    
    # Evaluate MVAs
    factory.EvaluateAllMethods()    
    
    # Save the output.
    outputFile.Close()
    
    print "=== wrote root file %s\n" % outfname
    print "=== TMVAClassification is done!\n"
    
    # open the GUI for the result macros    
    #gROOT.ProcessLine( "TMVAGui(\"%s\")" % outfname )
    
    # keep the ROOT thread running
    #gApplication.Run() 

    ChangeWeightName = 'mv /afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/weights/TMVAClassification_BDT.weights.xml /afs/hep.wisc.edu/home/zmao/CMSSW_5_3_15/src/TMVA-v4.2.0/test/weights/TMVAClassification_BDT.weights_EWK_%i.xml' %len(varList)
    os.system(ChangeWeightName)

# ----------------------------------------------------------

if __name__ == "__main__":
    main()
