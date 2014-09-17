/**********************************************************************************
 * Project   : TMVA - a Root-integrated toolkit for multivariate data analysis    *
 * Package   : TMVA                                                               *
 * Exectuable: TMVAClassificationApplication                                      *
 *                                                                                *
 * This macro provides a simple example on how to use the trained classifiers     *
 * within an analysis module                                                      *
 **********************************************************************************/

#include <cstdlib>
#include <vector>
#include <iostream>
#include <map>
#include <string>

#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TSystem.h"
#include "TROOT.h"
#include "TStopwatch.h"

#include "TMVAGui.C"

#if not defined(__CINT__) || defined(__MAKECINT__)
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"
#endif

using namespace TMVA;

void TMVAClassificationApplication_new(TString myMethodList = "" , TString iFileName = "") 
{   
#ifdef __CINT__
   gROOT->ProcessLine( ".O0" ); // turn off optimization in CINT
#endif

   //---------------------------------------------------------------

   // This loads the library
   TMVA::Tools::Instance();

   // Default MVA methods to be trained + tested
   std::map<std::string,int> Use;

   // --- Cut optimisation
   Use["Cuts"]            = 0;
   Use["CutsD"]           = 0;
   Use["CutsPCA"]         = 0;
   Use["CutsGA"]          = 0;
   Use["CutsSA"]          = 0;
   // 
   // 
   // --- Boosted Decision Trees
   Use["BDT"]             = 1; // uses Adaptive Boost
   std::cout << std::endl;
   std::cout << "==> Start TMVAClassificationApplication" << std::endl;

   // Select methods (don't look at this code - not of interest)
   if (myMethodList != "") {
      for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;

      std::vector<TString> mlist = gTools().SplitString( myMethodList, ',' );
      for (UInt_t i=0; i<mlist.size(); i++) {
         std::string regMethod(mlist[i]);

         if (Use.find(regMethod) == Use.end()) {
            std::cout << "Method \"" << regMethod 
                      << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
            for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
               std::cout << it->first << " ";
            }
            std::cout << std::endl;
            return;
         }
         Use[regMethod] = 1;
      }
   }

   // --------------------------------------------------------------------------------------------------

   // --- Create the Reader object

   TMVA::Reader *reader = new TMVA::Reader("!Color:!Silent" );    
   // Create a set of variables and declare them to the reader
   // - the variable names MUST corresponds in name and type to those given in the weight file(s) used
   Float_t var1, var2, var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14, var15;
   reader->AddVariable( "svMass", &var1);
   reader->AddVariable( "fMass", &var2 );
   reader->AddVariable( "dRTauTau", &var3 );
   reader->AddVariable( "dRJJ", &var4 );
   reader->AddVariable( "svPt", &var5 );
   reader->AddVariable( "dRhh", &var6 );
   reader->AddVariable( "met", &var7 );
   reader->AddVariable( "mJJReg", &var8 );
   reader->AddVariable( "metTau1DPhi", &var9 );
   reader->AddVariable( "metTau2DPhi", &var10);
   reader->AddVariable( "metJ1DPhi", &var11);
   reader->AddVariable( "metJ2DPhi", &var12 );
   reader->AddVariable( "metTauPairDPhi", &var13 );
   reader->AddVariable( "metSvTauPairDPhi", &var14 );
   reader->AddVariable( "metJetPairDPhi", &var15 );
//     


   // Spectator variables declared in the training have to be added to the reader, too
//    Float_t spec1,spec2;
//    reader->AddSpectator( "spec1 := var1*2",   &spec1 );
//    reader->AddSpectator( "spec2 := var1*3",   &spec2 );

//    Float_t Category_cat1, Category_cat2, Category_cat3;
//    if (Use["Category"]){
//       // Add artificial spectators for distinguishing categories
//       reader->AddSpectator( "Category_cat1 := var3<=0",             &Category_cat1 );
//       reader->AddSpectator( "Category_cat2 := (var3>0)&&(var4<0)",  &Category_cat2 );
//       reader->AddSpectator( "Category_cat3 := (var3>0)&&(var4>=0)", &Category_cat3 );
//    }

   // --- Book the MVA methods

   TString dir    = "weights/";
   TString prefix = "TMVAClassification";

   // Book method(s)
   for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
      if (it->second) {
         TString methodName = TString(it->first) + TString(" method");
         TString weightfile = dir + prefix + TString("_") + TString(it->first) + TString(".weights.xml");
         reader->BookMVA( methodName, weightfile ); 
      }
   }
   
   // Book output histograms
   UInt_t nbin = 100;
   TH1F   *histBdt(0);
   histBdt = new TH1F( "MVA_BDT",  "MVA_BDT", nbin, -1.0, 1.0);

   // Prepare input tree (this must be replaced by your data source)
   // in this example, there is a toy tree with signal and one with background events
   // we'll later on use only the "signal" events for the test in this example.
   //   
   TFile *input(0);
   TString fileName = iFileName;
   TString fname = "/scratch/zmao/relaxed_regression/"+fileName;
   TString oFileName = "/scratch/zmao/relaxed_regression/TMVAClassApp_" + fileName;

   if (!gSystem->AccessPathName( fname )) 
      input = TFile::Open(fname); // check if file in local directory exists
   if (!input) {
      std::cout << "ERROR: could not open data file" << std::endl;
      exit(1);
   }
   std::cout << "--- TMVAClassificationApp    : Using input file: " << input->GetName() << std::endl;

   // --- Event loop

   // Prepare the event tree
   // - here the variable names have to corresponds to your tree
   // - you can use the same variables as above which is slightly faster,
   //   but of course you can use different ones and copy the values inside the event loop
   //
   std::cout << "--- Select signal sample" << std::endl;
   TTree* theTree = (TTree*)input->Get("eventTree");
   TFile *target  = new TFile( oFileName,"RECREATE" );
   TTree *newTree = theTree->CloneTree();
   Float_t BDT;
   TBranch *branchBDT = newTree->Branch("BDT2",&BDT,"BDT/F");
   std::vector<Double_t> *vecVar1;
   std::vector<Double_t> *vecVar5;
   std::vector<Double_t> *vecVar7;
   theTree->SetBranchAddress( "svMass", &vecVar1);
   theTree->SetBranchAddress( "fMass", &var2);
   theTree->SetBranchAddress( "dRTauTau", &var3);
   theTree->SetBranchAddress( "dRJJ", &var4 );
   theTree->SetBranchAddress( "svPt", &vecVar5 );
   theTree->SetBranchAddress( "dRhh", &var6 );
   theTree->SetBranchAddress( "met", &vecVar7 );
   theTree->SetBranchAddress( "mJJReg", &var8 );
   theTree->SetBranchAddress( "metTau1DPhi", &var9 );
   theTree->SetBranchAddress( "metTau2DPhi", &var10);
   theTree->SetBranchAddress( "metJ1DPhi", &var11);
   theTree->SetBranchAddress( "metJ2DPhi", &var12 );
   theTree->SetBranchAddress( "metTauPairDPhi", &var13 );
   theTree->SetBranchAddress( "metSvTauPairDPhi", &var14 );
   theTree->SetBranchAddress( "metJetPairDPhi", &var15 );


   //to get initial pre-processed events
   TH1F* cutFlow = (TH1F*)input->Get("preselection");

   // Efficiency calculator for cut method
   Int_t    nSelCutsGA = 0;
   Double_t effS       = 0.7;

   std::vector<Float_t> vecVar(4); // vector for EvaluateMVA tests

   std::cout << "--- Processing: " << theTree->GetEntries() << " events" << std::endl;
   TStopwatch sw;
   sw.Start();
   for (Long64_t ievt=0; ievt<theTree->GetEntries();ievt++) {

      if (ievt%1000 == 0) std::cout << "--- ... Processing event: " << ievt << std::endl;
      theTree->GetEntry(ievt);
      var1 = vecVar1->at(0);
      var5 = vecVar5->at(0);
      var7 = vecVar7->at(0);
      if (var2 < 50) continue; 
      // --- Return the MVA outputs and fill into histograms

      if (Use["CutsGA"]) {
         // Cuts is a special case: give the desired signal efficienciy
         Bool_t passed = reader->EvaluateMVA( "CutsGA method", effS );
         if (passed) nSelCutsGA++;
      }
      BDT = reader->EvaluateMVA( "BDT method");
      histBdt->Fill(BDT);
      branchBDT->Fill();
   }

   // Get elapsed time
   sw.Stop();
   std::cout << "--- End of event loop: "; sw.Print();

   // Get efficiency for cuts classifier
   if (Use["CutsGA"]) std::cout << "--- Efficiency for CutsGA method: " << double(nSelCutsGA)/theTree->GetEntries()
                                << " (for a required signal efficiency of " << effS << ")" << std::endl;

   if (Use["CutsGA"]) {

      // test: retrieve cuts for particular signal efficiency
      // CINT ignores dynamic_casts so we have to use a cuts-secific Reader function to acces the pointer  
      TMVA::MethodCuts* mcuts = reader->FindCutsMVA( "CutsGA method" ) ;

      if (mcuts) {      
         std::vector<Double_t> cutsMin;
         std::vector<Double_t> cutsMax;
         mcuts->GetCuts( 0.7, cutsMin, cutsMax );
         std::cout << "--- -------------------------------------------------------------" << std::endl;
         std::cout << "--- Retrieve cut values for signal efficiency of 0.7 from Reader" << std::endl;
         for (UInt_t ivar=0; ivar<cutsMin.size(); ivar++) {
            std::cout << "... Cut: " 
                      << cutsMin[ivar] 
                      << " < \"" 
                      << mcuts->GetInputVar(ivar)
                      << "\" <= " 
                      << cutsMax[ivar] << std::endl;
         }
         std::cout << "--- -------------------------------------------------------------" << std::endl;
      }
   }

   // --- Write histograms

   histBdt->Write();
   cutFlow->Write();
   newTree->Write();
   target->Close();

   std::cout << "--- Created root file: \""<<oFileName<<"\" containing the MVA output histograms" << std::endl;
  
   delete reader;
    
   std::cout << "==> TMVAClassificationApplication is done!" << endl << std::endl;
} 
