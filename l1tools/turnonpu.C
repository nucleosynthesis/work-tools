// ROOT classes
#include "TMath.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TCanvas.h"
#include "TRandom3.h"
#include "TStyle.h"
#include "TGraph.h"
#include "TLegend.h"
#include "TVector2.h"
#include "TLatex.h"
#include "TMultiGraph.h"

//#include "files_160704_SingleMu2016.h"
#include "files_ZeroBias_r275068.h"

//gROOT->ProcessLine(".L ");
// C++ classes
#include <iostream>
#include <sstream>
#include <map>
#include <vector>
#include <algorithm>

// L1Trigger classes (data structures to be exact)
#include "L1Trigger/L1TNtuples/interface/L1AnalysisL1UpgradeDataFormat.h"
#include "L1Trigger/L1TNtuples/interface/L1AnalysisRecoMetDataFormat.h"
#include "L1Trigger/L1TNtuples/interface/L1AnalysisRecoVertexDataFormat.h"
#include "L1Trigger/L1TNtuples/interface/L1AnalysisRecoMetFilterDataFormat.h"
#include "L1Trigger/L1TNtuples/interface/L1AnalysisRecoMuon2DataFormat.h"
#include "L1Trigger/L1TNtuples/interface/L1AnalysisL1CaloTowerDataFormat.h"

bool fillReco = false ;

//TFile *fETPUS;
TRandom3 *rnd;

std::vector<std::vector<double> > aveET_;
std::vector<std::vector<double> > aveET3x3_;
std::vector<std::vector<double> > aveETX_;
std::vector<std::vector<double> > aveETY_;

double calculateMetNoMu(L1Analysis::L1AnalysisRecoMetDataFormat  *reco_,L1Analysis::L1AnalysisRecoMuon2DataFormat * muons_ ){

  double phi = reco_->metPhi;
  double x = (reco_->met)*cos(phi);
  double y = (reco_->met)*sin(phi);

  TVector2 met(x,y);

  for(unsigned int iter=0; iter<muons_->nMuons; ++iter){
    double mupt  = muons_->pt[iter];
    double muphi = muons_->phi[iter];
    TVector2 muon(mupt*cos(muphi),mupt*sin(muphi));
    met+=muon;
  }
  return met.Mod(); 
}

int calculateTowersAboveThresh(L1Analysis::L1AnalysisL1CaloTowerDataFormat * caloTowers_, int maxIEta=15, bool cap=true){

  int ntowers = 0;
  // First calculate num towers above threshold in the first +/- X rings in eta 
  for (int jTower=0; jTower<caloTowers_->nTower; ++jTower){
	if ( abs(caloTowers_->ieta[jTower])<=maxIEta ){
		ntowers++;
	}
  }

  if (cap){
   /*
    if (maxIEta == 4 ){
      // integer divide 
      ntowers/=2;
      if (ntowers>31) ntowers=31;
   */
      // Compression is a bit odd but this is +/- 15 rings above threshold !
      if (ntowers < 20  ) ntowers = 0;
      else if (ntowers >= 140 ) ntowers = 31; 
      else ntowers = ntowers/4 - 4 ; 
  }

  return ntowers; 
}

void loadAverageRings(int iEtaMax, TFile *fETPUS){

   for (int absieta=1;absieta<=iEtaMax;absieta++){
	TH2F *thehistE  = (TH2F*) fETPUS->Get(Form("sumET_h2_ieta_pos_%d",absieta));
	//TH2F *thehistEX = (TH2F*) fETPUS->Get(Form("sumXET_h2_ieta_pos_%d",absieta));
	//TH2F *thehistEY = (TH2F*) fETPUS->Get(Form("sumYET_h2_ieta_pos_%d",absieta));

	//double *vecE = new double[31];
	//double *vecX = new double[31];
	//double *vecY = new double[31];
	std::vector<double> vecE;

	std::cout << " Loaded (+/-ieta=) " << absieta << ", " <<  thehistE->GetName() << std::endl;
        for (int nt=1;nt<=31;nt++){
	 if (absieta==29) {
	  vecE.push_back(0);
	  //vecX[nt]=0;
	  //vecY[nt]=0;
	 } else {
          TH1D *prj  =(TH1D*)  thehistE->ProjectionY(Form("%g",rnd->Uniform()),nt,nt);
          //TH1D *prjX =(TH1D*) thehistEX->ProjectionY(Form("%g",rnd->Uniform()),nt,nt);
          //TH1D *prjY =(TH1D*) thehistEY->ProjectionY(Form("%g",rnd->Uniform()),nt,nt); 
	  // Scale by 0.5 as energy taken from 2 rings (+/- eta )
//	  vecE[nt]=0.5*prj->GetMean();
	  vecE.push_back(0.5*prj->GetMean());
	  std::cout << " nTT=" << nt << ", " <<  0.5*prj->GetMean() << std::endl;
	  //vecX[nt]=0.5*prjX->GetMean();
	  //vecY[nt]=0.5*prjY->GetMean();
	 }
        }
        aveET_.push_back(vecE);
        //aveETX_.push_back(vecX);
        //aveETY_.push_back(vecY);

   }
   std::cout << " Loaded Ring Averages " << std::endl;

}

void loadAverageRings3x3(TFile *fETPUS){

   TH2F *thehistE  ;//= (TH2F*) fETPUS->Get(Form("sumET_h2_ieta_pos_%d",absieta));
   for (int absieta=2;absieta<=29;absieta+=3){

	std::cout << " Loading (+/-ieta=) " << absieta << std::endl;
	if (absieta>26){
	  thehistE = (TH2F*) fETPUS->Get(Form("Region_sumET_h2_ieta_pos_HF"));
        } else {
	  thehistE = (TH2F*) fETPUS->Get(Form("Region_sumET_h2_ieta_pos_%d",absieta));
	}

	//double *vecE = new double[31];
	std::vector<double> vecE;
	std::cout << " ... Loaded (+/-ieta=) " << absieta << ", " <<  thehistE->GetName() << std::endl;
        for (int nt=1;nt<=31;nt++){
          TH1D *prj =(TH1D*)  thehistE->ProjectionY(Form("%g",rnd->Uniform()),nt,nt);
	  //vecE[nt]=0.5*prj->GetMean();   // 0.5 here is because sum was over 2 halfs!
	  vecE.push_back(0.5*prj->GetMean());
	  std::cout << " nTT = " << nt << ", " << vecE[nt];
        }
	std::cout << std::endl;
        aveET3x3_.push_back(vecE);
   } 

   std::cout << " Loaded 3xRing Averages " << std::endl;
}

double getAverageEnergyRing(int absieta, int nt, int xy_orsum){  // 0 = ETsum, -1 = ETX, 1 = ETY

   if (absieta==0) return 0.; 

   if (xy_orsum==0){
      return aveET_[absieta-1][nt];
   } else if (xy_orsum==-1){
      return aveETX_[absieta-1][nt];
   } else if (xy_orsum==1){
      return aveETY_[absieta-1][nt];
   } 

   return 0.;
}


double getAverageEnergyRegion(int absieta, int nt){    // return average for single ring

   if (absieta==0) return 0.; 
   // get compression for absieta to bin 
   //int bin = absieta-1;
   int bin = ((absieta)-1)/3;  // integer division!
   if ( absieta>27 ) bin = 9 ;

   double ave = aveET3x3_[bin][nt];
   int totalHFRings = 14;  // 29->41 
   if ( absieta>27)   return ave/totalHFRings;  // sum was over 14 rings 
   else return ave/3;  // sum was over 3 rings 

   //return 0.;
}

double getAverageEnergyRegion3x3(int absieta, int nt){   // return average for 3*3 block or (28+HF)*3 block

   if (absieta==0) return 0.; 
   // get compression for absieta to bin 

   int bin = ((absieta)-1)/3;  // integer division!
   if ( absieta>27 ) bin = 9 ;

   double ave = aveET3x3_[bin][nt];  // average is already divided by 2 for the 2 halfs
   //int totalHFtowers = 936;  // 29->41 * 72
   if ( absieta>27)   return ave/(72/3); // return the full 28+HF sum but only the 3 stips in phi?
   else return ave/(72/3);   // return the 3Rings / 72/3 for the 3x3 region
}

// Recalculate ET using Calo Towers
Double_t recalculateET(L1Analysis::L1AnalysisL1CaloTowerDataFormat * caloTowers_, int iEtaMax, bool pus){

  Double_t ET = 0.0;

  int nTT = calculateTowersAboveThresh(caloTowers_,15,true);

  // Do the crazy Hardware version of ET --> Super slow, but necessary to check logic 
  for (int sign=-1;sign<=1;sign+=2){

    for (int absieta=1;absieta<=iEtaMax;absieta++){
      double etring = 0;

      for(int jTower=0; jTower<caloTowers_->nTower; ++jTower){
        
	int ieta = absieta*sign;
	if (caloTowers_->ieta[jTower] != ieta ) continue;
    	int iet = caloTowers_->iet[jTower];

        etring += (double)iet;
      }

      if (pus){
        double aveE = getAverageEnergyRing(absieta,nTT,0);
	//std::cout << " ieta " << absieta << ", nTT " << nTT << ", region Et "<< etring << ", aveE " << aveE << std::endl;
        etring = etring-aveE > 0 ? etring-aveE : 0 ;
	etring =  etring-aveE;
      }

      ET+=0.5*etring;
    }
  }
  return ET;
}


// ----------------------------------------


Double_t recalculateMETRegional3x3(L1Analysis::L1AnalysisL1CaloTowerDataFormat * caloTowers_, int iEtaMax, bool pus, bool zerosuppress=false){


  Double_t metX = 0.0;
  Double_t metY = 0.0;

  int nTT = calculateTowersAboveThresh(caloTowers_);
 
  for (int sign=-1;sign<=1;sign+=2){

    for (int absieta=2;absieta<=41;absieta+=3){
 
	if (absieta>iEtaMax) continue;
	int ieta = absieta*sign;

	for (int iphi=1;iphi<=71;iphi+=3){

	   double regionet = 0;

           for(int jTower=0; jTower<caloTowers_->nTower; ++jTower){
	     if (abs(caloTowers_->ieta[jTower] - ieta)>1 ) continue;
	     if (abs(caloTowers_->iphi[jTower] - iphi)>1 ) continue;
		
	     regionet+=(double)caloTowers_->iet[jTower];
	   }

	   // subtract
	   if (pus){
  		double aveE = getAverageEnergyRegion3x3(absieta,nTT);  // average Energy in a region 
//		std::cout << " ieta " << absieta << " region Et "<< regionet << ", aveE " << aveE << std::endl;
		if (absieta>26){ // this is from 28 to HF land, should divide by number of rings used
			int nRings = (iEtaMax-27);
			aveE/=(14/nRings);
		}
		//std::cout << " ieta " << absieta << ", phi " << iphi << ", region Et "<< regionet << ", nTT " << nTT << " nTT (true) " << calculateTowersAboveThresh(caloTowers_,15,false) << ", aveE " << aveE << std::endl;
  		regionet -=  aveE;
	  	if (zerosuppress){
		   if ( regionet < 0 ) regionet=0; // dow we need to supress this, might be the only thing to make any difference
		}
	   }
	
      	   double phi = (Double_t)iphi * TMath::TwoPi()/72;

	   double ex = regionet*TMath::Sin(phi);
	   double ey = regionet*TMath::Cos(phi);

	   metX += 0.5*ex;
	   metY += 0.5*ey;
	}
	
    } 

  }

  return TMath::Sqrt(metX*metX + metY*metY);
}

Double_t recalculateMET(L1Analysis::L1AnalysisL1CaloTowerDataFormat * caloTowers_, int iEtaMax, bool pus, bool zerosuppress=false){

  Double_t metX = 0.0;
  Double_t metY = 0.0;

  int nTT = calculateTowersAboveThresh(caloTowers_);

  for (int sign=-1;sign<=1;sign+=2){

    for (int absieta=1;absieta<=iEtaMax;absieta++){
      double metXring=0;
      double metYring=0;
      // really slow to get the info here :( // how will this even work?
      for(int jTower=0; jTower<caloTowers_->nTower; ++jTower){

	int ieta = absieta*sign;
	if (caloTowers_->ieta[jTower] != ieta ) continue;
    	int iphi = caloTowers_->iphi[jTower];
    	int iet  = caloTowers_->iet[jTower];
	
	int nphis = 72;

      	double phi = (Double_t)iphi * TMath::TwoPi()/nphis;
	double corriet = (double)iet;

        if (pus){
          double aveE = getAverageEnergyRing(absieta,nTT,0)/72;
	  //std::cout << " ieta " << ieta << ", phi " << iphi << ", iEt "<< iet << ", nTT " << nTT << " nTT (true) " << calculateTowersAboveThresh(caloTowers_,15,false) << ", aveE " << aveE << std::endl;
	  corriet = (double(iet) - aveE);
	  if (zerosuppress){
	  	if (corriet < 0)  corriet = 0;
	  }
	}

	double ex = corriet*TMath::Sin(phi);
	double ey = corriet*TMath::Cos(phi);

        metXring += ex ;
        metYring += ey ;

      }

      metX+=0.5*metXring;
      metY+=0.5*metYring;
    }
  }

  return TMath::Sqrt(metX*metX + metY*metY);
}

// Recalculate MET using Calo Towers
Double_t recalculateMETFinitePrecision(L1Analysis::L1AnalysisL1CaloTowerDataFormat * caloTowers_, int iEtaMax, bool pus){

  assert(0); // don't call this guy , was just for a quick test 
  Double_t metX = 0.0;
  Double_t metY = 0.0;

  int nTT = calculateTowersAboveThresh(caloTowers_);

  // Do the crazy Hardware version of MET --> Super slow, but necessary to check logic 
  for (int sign=-1;sign<=1;sign+=2){

    for (int absieta=1;absieta<=iEtaMax;absieta++){

      double metXring=0;
      double metYring=0;

      for(int jTower=0; jTower<caloTowers_->nTower; ++jTower){

	int ieta = absieta*sign;
	if (caloTowers_->ieta[jTower] != ieta ) continue;
    	int iphi = caloTowers_->iphi[jTower];
    	int iet  = caloTowers_->iet[jTower];
	
	int nphis = 72;

	//if (absieta>28 ) nphis = 18;
	//if (absieta>39 ) nphis = 9;

      	double phi = (Double_t)iphi * TMath::TwoPi()/nphis;

	// Emulate bitwise buggery 
	int corriet = iet;
        if (pus){
          double aveE = getAverageEnergyRing(absieta,nTT, 0);
	  corriet = (int) (iet -aveE/nphis);
	  if (corriet < 0)  corriet = 0;
	}

	int ex = (int32_t) (corriet * std::trunc ( 511. * TMath::Cos(2*TMath::Pi() * (nphis - (iphi-1)) / nphis ) )) >> 9;
	int ey = (int32_t) (corriet * std::trunc ( 511. * TMath::Sin(2*TMath::Pi() * ( (iphi-1)) / nphis ) )) >> 9;

	// now assume we're safe to convert to double?
	//
	
        metXring += (double)ex ;
        metYring += (double)ey ;

      }

      metX+=0.5*metXring;
      metY+=0.5*metYring;
    }
  }

  return TMath::Sqrt(metX*metX + metY*metY);
}

void main_func(std::string filename, TTree *tree, double *vmet, double *vet, int *nvtx){

  TFile * file = TFile::Open(filename.c_str());
  int thresh = 0;

  // Map for Tree Category -> Tree path
  map<string, string> treeCat_treePath_map;

  treeCat_treePath_map["TowerTree"]       = "l1CaloTowerEmuTree/L1CaloTowerTree";
  treeCat_treePath_map["Emu Upgrade"]     = "l1UpgradeEmuTree/L1UpgradeTree";
  if (fillReco){
    treeCat_treePath_map["Reco Jet"]        = "l1JetRecoTree/JetRecoTree";
    treeCat_treePath_map["Reco MET Filter"] = "l1MetFilterRecoTree/MetFilterRecoTree";
    treeCat_treePath_map["Reco"]            = "l1RecoTree/RecoTree";
  }


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
  L1Analysis::L1AnalysisL1UpgradeDataFormat     *upgradeEmu_ = new L1Analysis::L1AnalysisL1UpgradeDataFormat();
  L1Analysis::L1AnalysisL1CaloTowerDataFormat   *towers_     = new L1Analysis::L1AnalysisL1CaloTowerDataFormat;
  

    L1Analysis::L1AnalysisRecoMetDataFormat       *reco_       = new L1Analysis::L1AnalysisRecoMetDataFormat();
    L1Analysis::L1AnalysisRecoVertexDataFormat    *vertex_     = new L1Analysis::L1AnalysisRecoVertexDataFormat();
    L1Analysis::L1AnalysisRecoMetFilterDataFormat *metFilters_ = new L1Analysis::L1AnalysisRecoMetFilterDataFormat();

  treeCat_tree_map["TowerTree"]->SetBranchAddress("L1CaloTower"     , &towers_      );
  treeCat_tree_map["Emu Upgrade"    ]->SetBranchAddress("L1Upgrade" , &upgradeEmu_);

  if (fillReco){
    treeCat_tree_map["Reco"           ]->SetBranchAddress("Vertex"    , &vertex_    );
    treeCat_tree_map["Reco MET Filter"]->SetBranchAddress("MetFilters", &metFilters_);
    treeCat_tree_map["Reco Jet"       ]->SetBranchAddress("Sums"      , &reco_      );
  }

  // get entries
  int nevents = 100000000; 
  Long64_t nentries = treeCat_tree_map["TowerTree"]->GetEntriesFast();
  if( nevents > nentries) nevents=nentries;

  std::cout << "File - " << filename << ", Looping over " << nevents << ", out of a total of " << nentries << std::endl;

  for (int jentry=0; jentry<nevents;jentry++){
    // Print out every 1000th event
    if(((jentry+1)%1000)==0){
      std::cout << "Done " << jentry+1  << " events...\r" << std::flush;
    }

    // Fill the trees with the jentry-th event 
    for(auto it = treeCat_tree_map.begin(); it != treeCat_tree_map.end(); ++it){
      it->second->GetEntry(jentry);
    }
    // MET Filters 
    if ( fillReco && metFilters_->hbheNoiseFilter != 1.0 ) continue;
    
    // skip entries with no towers 
    if (! ( calculateTowersAboveThresh(towers_,100,0) >0 ) ) continue;


    vmet[0] = recalculateMET(towers_,28,0);
    vmet[1] = recalculateMET(towers_,28,1);
    vmet[2] = recalculateMET(towers_,28,1,1);
    if (fillReco) vmet[3] = (double)reco_->caloMet;  // Compare to CaloMET
    vmet[4] = recalculateMET(towers_,41,0);
    vmet[5] = recalculateMET(towers_,41,1);
    vmet[6] = recalculateMET(towers_,41,1,1);
    // Now do MET regional and with PUS 
    vmet[7] = recalculateMETRegional3x3(towers_,28,0);
    vmet[8] = recalculateMETRegional3x3(towers_,28,1);
    vmet[9] = recalculateMETRegional3x3(towers_,28,1,1);

    vmet[10] = recalculateMETRegional3x3(towers_,41,0);
    vmet[11] = recalculateMETRegional3x3(towers_,41,1);
    vmet[12] = recalculateMETRegional3x3(towers_,41,1,1);

    vmet[13] = (double)upgradeEmu_->sumEt[2]; // met Sum from L1


    vet[0] = recalculateET(towers_,28,0);
    vet[1] = recalculateET(towers_,28,1);
    vet[2] = recalculateET(towers_,41,0);
    vet[3] = recalculateET(towers_,41,1);
    if (fillReco)  vet[4] = (double)reco_->caloSumEt;
    vet[5] = (double)upgradeEmu_->sumEt[0]; // et sum from L1 
     
    if (fillReco) nvtx[0] = vertex_->nVtx; // different definitions of nTT stored
    nvtx[1] = calculateTowersAboveThresh(towers_,4,false);
    nvtx[2] = calculateTowersAboveThresh(towers_,10,false);
    nvtx[3] = calculateTowersAboveThresh(towers_,15,false);
    nvtx[4] = calculateTowersAboveThresh(towers_,28,false);
    nvtx[5] = calculateTowersAboveThresh(towers_,41,false);

    tree->Fill();
  }
}

void turnonpu(){

  TFile *fETPUS = TFile::Open("output_average_sums.root");  // file with PU maps 
  rnd = new TRandom3();
  loadAverageRings3x3(fETPUS);
  loadAverageRings(41,fETPUS);
  std::cout <<"PILUP MAP FILE LOADED --  " << fETPUS->GetName () << std::endl;
  fETPUS->Close();

  TFile *fout = new TFile("flat_met_trees_ZB.root","RECREATE");
  TTree *treeout = new TTree("entries","entries");
  
  // store differnt algorithms for different things
  
  double met[14] = {0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.};    // met, metpus, recomet, hfmet, hfmetpus, met3x3, met3x3pus,emulator met
  double et[6]   = {0.,0.,0.,0.,0.,0.};
  int    nvtx[6] = {0,0,0,0,0,0};		// nvtx, ntt 4, ntt 10, ntt 15, 


  treeout->Branch("met",         &met[0],"met/double");
  treeout->Branch("metpus",      &met[1],"metpus/double");
  treeout->Branch("metpus0",     &met[2],"metpus0/double");
  treeout->Branch("recomet",     &met[3],"recomet/double");
  treeout->Branch("hfmet",       &met[4],"hfmet/double");
  treeout->Branch("hfmetpus",    &met[5],"hfmetpus/double");
  treeout->Branch("hfmetpus0",   &met[6],"hfmetpus0/double");
  treeout->Branch("met3x3",      &met[7],"met3x3/double");
  treeout->Branch("met3x3pus",   &met[8],"met3x3pus/double");
  treeout->Branch("met3x3pus0",  &met[9],"met3x3pus0/double");
  treeout->Branch("hfmet3x3",    &met[10],"hfmet3x3/double");
  treeout->Branch("hfmet3x3pus", &met[11],"hfmet3x3pus/double");
  treeout->Branch("hfmet3x3pus0",&met[12],"hfmet3x3pus0/double");
  treeout->Branch("emulator_met",&met[13],"emulator_met/double");

  treeout->Branch("et",         &et[0],"et/double");
  treeout->Branch("etpus",      &et[1],"etpus/double");
  treeout->Branch("hfet",       &et[2],"hfet/double");
  treeout->Branch("hfetpus",    &et[3],"hfetpus/double");
  treeout->Branch("recoet",     &et[4],"recoet/double");
  treeout->Branch("emulator_et",&et[5],"emulator_et/double");

  treeout->Branch("nvtx", &nvtx[0],"nvtx/int" );
  treeout->Branch("ntt",  &nvtx[1],"ntt/int"  );    // default is +/-5
  treeout->Branch("ntt4", &nvtx[1],"ntt4/int" );	
  treeout->Branch("ntt10",&nvtx[2],"ntt10/int");
  treeout->Branch("ntt15",&nvtx[3],"ntt15/int");
  treeout->Branch("ntt28",&nvtx[4],"ntt28/int");
  treeout->Branch("ntt41",&nvtx[5],"ntt41/int");

  //nFiles = 5;
  /*
  for (int fi=0;fi<nFiles;fi++){
	 main_func(filesSingleMu[fi],treeout,met,et,nvtx);
  }
  */
  for (int fi=0;fi<nFiles;fi++){
	 main_func(filesZeroBias[fi],treeout,met,et,nvtx);
  }

  fout->cd();
  treeout->Write();

  std::cout << " Trees saved to " << fout->GetName() << std::endl;
}
