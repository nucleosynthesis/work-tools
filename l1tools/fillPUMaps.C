// ROOT classes
#include "TMath.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TGraph.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TMultiGraph.h"
#include "files_ZeroBias_r275068.h"
// C++ classes
#include <iostream>
#include <sstream>
#include <map>
#include <vector>

// L1Trigger classes (data structures to be exact)
#include "L1Trigger/L1TNtuples/interface/L1AnalysisL1UpgradeDataFormat.h"
#include "L1Trigger/L1TNtuples/interface/L1AnalysisRecoMetDataFormat.h"
#include "L1Trigger/L1TNtuples/interface/L1AnalysisRecoVertexDataFormat.h"
#include "L1Trigger/L1TNtuples/interface/L1AnalysisRecoMetFilterDataFormat.h"
#include "L1Trigger/L1TNtuples/interface/L1AnalysisRecoMuon2DataFormat.h"
#include "L1Trigger/L1TNtuples/interface/L1AnalysisL1CaloTowerDataFormat.h"

const int thresh = 0;

void main_func(std::string filename, std::vector<TH2F*> hists,  std::vector<TH2F*> histsX,  std::vector<TH2F*> histsY,  std::vector<TH2F*> histsR, TH1F *hNtowers){

  TFile * file = TFile::Open(filename.c_str());
  

  // Map for Tree Category -> Tree path
  map<string, string> treeCat_treePath_map;
  treeCat_treePath_map["TowerTree"]        = "l1CaloTowerTree/L1CaloTowerTree";
  //treeCat_treePath_map["Emu Upgrade"]      = "l1UpgradeEmuTree/L1UpgradeTree";


  // Get the Trees
  map<string, TTree*> treeCat_tree_map;
  for(auto it = treeCat_treePath_map.begin(); it != treeCat_treePath_map.end(); ++it){
    treeCat_tree_map[it->first] = (TTree*) file->Get(it->second.c_str());
    if( !treeCat_tree_map[it->first] ){
      cout << "ERROR: could not open path to " << it->first << ": " << it->second << endl;
      return;
    }
  }

  // set branch addresses
  L1Analysis::L1AnalysisL1CaloTowerDataFormat     *towers_ = new L1Analysis::L1AnalysisL1CaloTowerDataFormat;
  //L1Analysis::L1AnalysisL1UpgradeDataFormat     *upgradeEmu_ = new L1Analysis::L1AnalysisL1UpgradeDataFormat();
  
  treeCat_tree_map["TowerTree"]->SetBranchAddress("L1CaloTower"      , &towers_      );
  //treeCat_tree_map["Emu Upgrade"]->SetBranchAddress("L1Upgrade" , &upgradeEmu_);

  // get entries
  int nevents = 100000000;
  Long64_t nentries = treeCat_tree_map["TowerTree"]->GetEntriesFast();
  if( nevents > nentries) nevents=nentries;

  std::cout << "Looping over " << nevents << ", out of a total of " << nentries << std::endl;

  for (int jentry=0; jentry<nevents;jentry++){
    // Print out every 1000th event
    if(((jentry+1)%1000)==0){
      std::cout << "Done " << jentry+1  << " events...\r" << std::flush;
    }

    // Fill the trees with the jentry-th event 
    for(auto it = treeCat_tree_map.begin(); it != treeCat_tree_map.end(); ++it){
      it->second->GetEntry(jentry);
    }

    int TOTALTOWERS=0;
    for (int itow=0; itow<towers_->nTower;itow++){
      if (towers_->iet[itow] < thresh) continue;
      TOTALTOWERS++;
    }
    if ( TOTALTOWERS==0 ) continue;

    // count towers above threshold in first +/ 15 eta rings 
    int numtowProper = 0;
    for (int itow=0; itow<towers_->nTower;itow++){
      if (towers_->iet[itow] < thresh) continue;
      if (abs(towers_->ieta[itow]) > 15) continue;
      numtowProper++;
    }
    //std::cout << numtowProper << std::endl;
    //  Now just count number of towers in |ieta| < 15 
    hNtowers->Fill(numtowProper);

    /*
      // divide by 2 
      numtow/=2 ; // integer divide 
      // 5 bits ! --> should compress 
      if (numtow > 31) numtow=31;
    */

    
    int numtow;
    // Compression is a bit odd but this is +/- 15 rings above threshold !
    if (numtowProper < 20 ) numtow = 0;
    else if (numtowProper >= 140 ) numtow = 31; 
    else numtow = numtowProper/4 - 4 ; 

    // Pick an eta 
    for (int iEta=0;iEta<=41;iEta++){

      TH2F *theHist  = hists[iEta];
      TH2F *theHistX = histsX[iEta];
      TH2F *theHistY = histsY[iEta];

      float sumet = 0.; 
      float sumetx = 0.; 
      float sumety = 0.; 

      for (int itow=0; itow<towers_->nTower;itow++){
	int absieta = abs(towers_->ieta[itow]);
      	if (absieta!=iEta) continue;

	int et   = (float) towers_->iet[itow];
    	int iphi = towers_->iphi[itow];

	int nphis = 72; 
	//if (absieta>28 ) nphis = 18;
	//if (absieta>39 ) nphis = 9;

      	double phi = (Double_t)iphi * TMath::TwoPi()/nphis;

	sumet+=et;
	sumetx+=et*TMath::Cos(phi);
	sumety+=et*TMath::Sin(phi);

      }

      theHist->Fill(numtow,sumet);
      theHistX->Fill(numtow,sumetx);
      theHistY->Fill(numtow,sumety);

    }
	
    // Now do the same but in regions 

    int centrecount = 0;
    for (int iEta=2;iEta<=26;iEta+=3){

      TH2F *theHist  = histsR[centrecount];

      float sumet = 0.; 

      for (int itow=0; itow<towers_->nTower;itow++){
	int absieta = abs(towers_->ieta[itow]);
      	if (abs(absieta-iEta) > 1 ) continue;

	int et   = (float) towers_->iet[itow];
	sumet+=et;

      }

      theHist->Fill(numtow,sumet);
      centrecount++;
    }
   
    // Now fill the HF 
    TH2F *theHist  = histsR[centrecount];

    float sumet = 0.; 

    for (int itow=0; itow<towers_->nTower;itow++){
	int absieta = abs(towers_->ieta[itow]);
      	if (abs(absieta) < 27 ) continue;   // this is now last bit in HBHE+all HF 

	int et   = (float) towers_->iet[itow];
	sumet+=et;
    }

    theHist->Fill(numtow,sumet);

  }
}

void fillPUMaps(){

  // Make 41 histograms to fill 
  TFile *fout = new TFile("output_average_sums.root","RECREATE");
  std::vector<TH2F *> hists;
  std::vector<TH2F *> histsX;
  std::vector<TH2F *> histsY;
  std::vector<TH2F *> histsR;

  for (int iEta=0;iEta<=41;iEta++){
  	std::string ietaname = iEta>0 ? "pos" : "neg";
	int absieta = abs(iEta);
	hists.push_back(new TH2F(Form("sumET_h2_ieta_%s_%d",ietaname.c_str(),absieta)  ,Form("Num towers vs iet, ieta = %d",iEta),31,0,31,200,0,200));
	histsX.push_back(new TH2F(Form("sumXET_h2_ieta_%s_%d",ietaname.c_str(),absieta),Form("Num towers vs iet, ieta = %d",iEta),31,0,31,200,-100,100));
	histsY.push_back(new TH2F(Form("sumYET_h2_ieta_%s_%d",ietaname.c_str(),absieta),Form("Num towers vs iet, ieta = %d",iEta),31,0,31,200,-100,100));
  }
  for (int iEta=2;iEta<=26;iEta+=3){
  	std::string ietaname = iEta>0 ? "pos" : "neg";
	int absieta = abs(iEta);
	histsR.push_back(new TH2F(Form("Region_sumET_h2_ieta_%s_%d",ietaname.c_str(),absieta),Form("Num towers vs iet, ieta (central ieta of 3x72 region) = %d",iEta),31,0,31,300,0,300));
  }
  histsR.push_back(new TH2F(Form("Region_sumET_h2_ieta_pos_HF"),Form("Num towers vs iet, HF"),31,0,31,600,0,600));
  TH1F *towerNdistribution = new TH1F("Num_towers_15", "Number of towers with iet > 0 in |ieta| < 15",199,1,200);

  /* now a whole bunch of files ... */


  //for (int fi=0;fi<120;fi++){
  for (int fi=0;fi<nFiles;fi++){
    main_func(filesZeroBias[fi],hists,histsX,histsY,histsR, towerNdistribution);
  }

  fout->cd();
  for(auto ith = hists.begin(); ith != hists.end(); ++ith){
  	(*ith)->Write();
  }
  for(auto ith = histsX.begin(); ith != histsX.end(); ++ith){
  	(*ith)->Write();
  }
  for(auto ith = histsY.begin(); ith != histsY.end(); ++ith){
  	(*ith)->Write();
  }
  for(auto ith = histsR.begin(); ith != histsR.end(); ++ith){
  	(*ith)->Write();
  }
  towerNdistribution->Write();
  std::cout << "Maps saved to " << fout->GetName() << std::endl;
}
