/**********************************************************************************
 * Project   : TMVA - a Root-integrated toolkit for multivariate data analysis    *
 * Package   : TMVA                                                               *
 * Exectuable: TMVARegressionApplication                                          *
 *                                                                                *
 * This macro provides a simple example on how to use the trained regression MVAs *
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

#if not defined(__CINT__) || defined(__MAKECINT__)
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#endif

using namespace TMVA;

void BJetRegressionApplication( TString myMethodList = "" , TString sampleName = "", TString sampleLocation = "") 
{
   //---------------------------------------------------------------
   // This loads the library
   TMVA::Tools::Instance();

   // Default MVA methods to be trained + tested
   std::map<std::string,int> Use;

   // --- Mutidimensional likelihood and Nearest-Neighbour methods
   Use["PDERS"]           = 0;
   Use["PDEFoam"]         = 1; 
   Use["KNN"]             = 1;
   // 
   // --- Linear Discriminant Analysis
   Use["LD"]		        = 1;
   // 
   // --- Function Discriminant analysis
   Use["FDA_GA"]          = 1;
   Use["FDA_MC"]          = 0;
   Use["FDA_MT"]          = 0;
   Use["FDA_GAMT"]        = 0;
   // 
   // --- Neural Network
   Use["MLP"]             = 1; 
   // 
   // --- Support Vector Machine 
   Use["SVM"]             = 0;
   // 
   // --- Boosted Decision Trees
   Use["BDT"]             = 0;
   Use["BDTG"]            = 1;
   // ---------------------------------------------------------------

   std::cout << std::endl;
   std::cout << "==> Start TMVARegressionApplication" << std::endl;

   // Select methods (don't look at this code - not of interest)
   if (myMethodList != "") {
      for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) it->second = 0;

      std::vector<TString> mlist = gTools().SplitString( myMethodList, ',' );
      for (UInt_t i=0; i<mlist.size(); i++) {
         std::string regMethod(mlist[i]);

         if (Use.find(regMethod) == Use.end()) {
            std::cout << "Method \"" << regMethod << "\" not known in TMVA under this name. Choose among the following:" << std::endl;
            for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) std::cout << it->first << " ";
            std::cout << std::endl;
            return;
         }
         Use[regMethod] = 1;
      }
   }

   // --------------------------------------------------------------------------------------------------

   // --- Create the Reader object

   TMVA::Reader *reader = new TMVA::Reader( "!Color:!Silent" );    

   // Create a set of variables and declare them to the reader
   // - the variable names MUST corresponds in name and type to those given in the weight file(s) used
   Float_t jetPtUncorr, jetPt, jetEt, jetMt, jetPhi,jetMass, jetEta, jetptLeadTrk, jetVtx3dL, jetNtot, jetJECUnc;
   Float_t jetVtx3deL, jetvtxMass, jetVtxPt, jetSoftLeptPtRel, jetSoftLeptPt, jetSoftLeptdR;
   Float_t CSVJ1PtReg, CSVJ2PtReg, mJJReg;
   Float_t jet1Eta,  jet1Phi, jet1Mass;
   TString trainedVar = "jet";
   reader->AddVariable( trainedVar+"PtUncorr", &jetPtUncorr );
   reader->AddVariable( trainedVar+"Pt", &jetPt );
   reader->AddVariable( trainedVar+"Et", &jetEt );
   reader->AddVariable( trainedVar+"Mt", &jetMt );
   reader->AddVariable( trainedVar+"ptLeadTrk", &jetptLeadTrk );
   reader->AddVariable( trainedVar+"Vtx3dL", &jetVtx3dL );
   reader->AddVariable( trainedVar+"Vtx3deL", &jetVtx3deL );
   reader->AddVariable( trainedVar+"vtxMass", &jetvtxMass );
   reader->AddVariable( trainedVar+"VtxPt", &jetVtxPt );
   reader->AddVariable( trainedVar+"SoftLeptPtRel", &jetSoftLeptPtRel );
   reader->AddVariable( trainedVar+"SoftLeptPt", &jetSoftLeptPt );
   reader->AddVariable( trainedVar+"SoftLeptdR", &jetSoftLeptdR );
   reader->AddVariable( trainedVar+"Ntot", &jetNtot); 
   reader->AddVariable( trainedVar+"JECUnc", &jetJECUnc); 


   // Spectator variables declared in the training have to be added to the reader, too
//    Float_t spec1,spec2;
//    reader->AddSpectator( "spec1:=var1*2",  &spec1 );
//    reader->AddSpectator( "spec2:=var1*3",  &spec2 );

   // --- Book the MVA methods

   TString dir    = "weights/";
   TString prefix = "TMVARegression";

   // Book method(s)
   for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
      if (it->second) {
         TString methodName = it->first + " method";
         TString weightfile = dir + prefix + "_" + TString(it->first) + ".weights.xml";
         reader->BookMVA( methodName, weightfile ); 
      }
   }
   
   // Book output histograms
   TH1* hists[100];
   Int_t nhists = -1;
   for (std::map<std::string,int>::iterator it = Use.begin(); it != Use.end(); it++) {
      TH1* h = new TH1F( it->first.c_str(), TString(it->first) + " method", 100, -100, 600 );
      if (it->second) hists[++nhists] = h;
   }
   nhists++;
   
   // Prepare input tree (this must be replaced by your data source)
   // in this example, there is a toy tree with signal and one with background events
   // we'll later on use only the "signal" events for the test in this example.
   
   TFile *input(0);
   TString fname = sampleLocation;
   fname += sampleName;
   if (!gSystem->AccessPathName( fname )) {
      input = TFile::Open( fname ); // check if file in local directory exists
   } 
   else { 
      input = TFile::Open( "http://root.cern.ch/files/tmva_reg_example.root" ); // if not: download from ROOT server
   }
   
   if (!input) {
      std::cout << "ERROR: could not open data file" << std::endl;
      exit(1);
   }
   std::cout << "--- TMVARegressionApp        : Using input file: " << input->GetName() << std::endl;

   // --- Event loop

   // Prepare the tree
   // - here the variable names have to corresponds to your tree
   // - you can use the same variables as above which is slightly faster,
   //   but of course you can use different ones and copy the values inside the event loop
   //
   TTree* theTree = (TTree*)input->Get("eventTree");
   std::cout << "--- Select signal sample" << std::endl;
   theTree->SetBranchAddress( "CSVJ1PtUncorr", &jetPtUncorr );
   theTree->SetBranchAddress( "CSVJ1Pt", &jetPt );
   theTree->SetBranchAddress( "CSVJ1Et", &jetEt );
   theTree->SetBranchAddress( "CSVJ1Mt", &jetMt );
   theTree->SetBranchAddress( "CSVJ1ptLeadTrk", &jetptLeadTrk );
   theTree->SetBranchAddress( "CSVJ1Vtx3dL", &jetVtx3dL );
   theTree->SetBranchAddress( "CSVJ1Vtx3deL", &jetVtx3deL );
   theTree->SetBranchAddress( "CSVJ1vtxMass", &jetvtxMass );
   theTree->SetBranchAddress( "CSVJ1VtxPt", &jetVtxPt );
   theTree->SetBranchAddress( "CSVJ1vtxMass", &jetvtxMass );
   theTree->SetBranchAddress( "CSVJ1SoftLeptPtRel", &jetSoftLeptPtRel );
   theTree->SetBranchAddress( "CSVJ1SoftLeptPt", &jetSoftLeptPt );
   theTree->SetBranchAddress( "CSVJ1SoftLeptdR", &jetSoftLeptdR );
   theTree->SetBranchAddress("CSVJ1Ntot", &jetNtot); 
   theTree->SetBranchAddress("CSVJ1JECUnc", &jetJECUnc); 

   TH1F* cutFlow = (TH1F*)input->Get("preselection");

   std::cout << "--- Processing: " << theTree->GetEntries() << " events" << std::endl;
   TStopwatch sw;
   sw.Start();
   TString ofileName = sampleLocation;
   ofileName += "TMVARegApp_"+sampleName;
   TFile *target  = new TFile( ofileName,"RECREATE" );
   TTree *newTree = theTree->CloneTree();
   TBranch *branchJ1PtReg = newTree->Branch("CSVJ1PtReg",&CSVJ1PtReg,"CSVJ1PtReg/F");
   TBranch *branchJ2PtReg = newTree->Branch("CSVJ2PtReg",&CSVJ2PtReg,"CSVJ2PtReg/F");
   TBranch *branchMJJReg = newTree->Branch("mJJReg",&mJJReg,"mJJReg/F");

   std::vector<double> csvJ1PtReg;
   for (Long64_t ievt=0; ievt<theTree->GetEntries();ievt++) {
      if (ievt%1000 == 0) {
         std::cout << "--- ... Processing event: " << ievt << std::endl;
      }
      theTree->GetEntry(ievt);
      // Retrieve the MVA target values (regression outputs) and fill into histograms
      // NOTE: EvaluateRegression(..) returns a vector for multi-target regression
      for (Int_t ih=0; ih<nhists; ih++) {
         TString title = hists[ih]->GetTitle();
         CSVJ1PtReg = (reader->EvaluateRegression( title ))[0];
         csvJ1PtReg.push_back(CSVJ1PtReg);
	 branchJ1PtReg->Fill();
      }
   }
   theTree->SetBranchAddress( "CSVJ1Eta", &jet1Eta );
   theTree->SetBranchAddress( "CSVJ1Phi", &jet1Phi );
   theTree->SetBranchAddress( "CSVJ1Mass", &jet1Mass );
   theTree->SetBranchAddress( "CSVJ2Eta", &jetEta );
   theTree->SetBranchAddress( "CSVJ2Phi", &jetPhi );
   theTree->SetBranchAddress( "CSVJ2Mass", &jetMass );

   theTree->SetBranchAddress( "CSVJ2PtUncorr", &jetPtUncorr );
   theTree->SetBranchAddress( "CSVJ2Pt", &jetPt );
   theTree->SetBranchAddress( "CSVJ2Et", &jetEt );
   theTree->SetBranchAddress( "CSVJ2Mt", &jetMt );
   theTree->SetBranchAddress( "CSVJ2ptLeadTrk", &jetptLeadTrk );
   theTree->SetBranchAddress( "CSVJ2Vtx3dL", &jetVtx3dL );
   theTree->SetBranchAddress( "CSVJ2Vtx3deL", &jetVtx3deL );
   theTree->SetBranchAddress( "CSVJ2vtxMass", &jetvtxMass );
   theTree->SetBranchAddress( "CSVJ2VtxPt", &jetVtxPt );
   theTree->SetBranchAddress( "CSVJ2vtxMass", &jetvtxMass );
   theTree->SetBranchAddress( "CSVJ2SoftLeptPtRel", &jetSoftLeptPtRel );
   theTree->SetBranchAddress( "CSVJ2SoftLeptPt", &jetSoftLeptPt );
   theTree->SetBranchAddress( "CSVJ2SoftLeptdR", &jetSoftLeptdR );
   theTree->SetBranchAddress("CSVJ2Ntot", &jetNtot); 
   theTree->SetBranchAddress("CSVJ2JECUnc", &jetJECUnc); 

   ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double>> j1, j2;

   for (Long64_t ievt=0; ievt<theTree->GetEntries();ievt++) {
      if (ievt%1000 == 0) {
         std::cout << "--- ... Processing event: " << ievt << std::endl;
      }
      theTree->GetEntry(ievt);
      // Retrieve the MVA target values (regression outputs) and fill into histograms
      // NOTE: EvaluateRegression(..) returns a vector for multi-target regression
      for (Int_t ih=0; ih<nhists; ih++) {
         TString title = hists[ih]->GetTitle();
         CSVJ2PtReg = (reader->EvaluateRegression( title ))[0];
         branchJ2PtReg->Fill();
	 j1.SetCoordinates(csvJ1PtReg[ievt], jet1Eta, jet1Phi, jet1Mass);
	 j2.SetCoordinates(CSVJ2PtReg, jetEta, jetPhi, jetMass);
	 mJJReg = (j1+j2).mass();
	 branchMJJReg->Fill();
      }
   }

   sw.Stop();
   std::cout << "--- End of event loop: "; sw.Print();

   // --- Write histograms
   //   target->cd();
   cutFlow->Write();
   newTree->Write();
//    target->Write();
   target->Close();

   std::cout << "--- Created root file: \"" << target->GetName() 
             << "\" containing the MVA output histograms" << std::endl;
  
   delete reader;
    
   std::cout << "==> TMVARegressionApplication is done!" << std::endl << std::endl;
}
