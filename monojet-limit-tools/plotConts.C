#include "TMath.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TROOT.h"
#include "TSystem.h"
#include "TLegend.h"
#include "TEfficiency.h"
#include "TGraphAsymmErrors.h"
#include "TGraph2D.h"
#include "TGraph.h"
#include "RooDataHist.h"
#include "RooWorkspace.h"
#include <iostream>
#include <string>
#include <vector>


int MMED(double mh,int code){
  if (code==800) return ((int)(mh-80000000000))/10000; 
  if (code==801) return ((int)(mh-80100000000))/10000; 
  if (code==805) return ((int)(mh-80500000000))/10000; 
  if (code==806) return ((int)(mh-80600000000))/10000; 
  return -1;
}

int MDM(double mh, int code){
  if (code==800) return (mh-80000000000)  - ( ((Int_t)(mh-80000000000))/10000 )*10000;
  if (code==801) return (mh-80100000000)  - ( ((Int_t)(mh-80100000000))/10000 )*10000;
  if (code==805) return (mh-80500000000)  - ( ((Int_t)(mh-80500000000))/10000 )*10000;
  if (code==806) return (mh-80600000000)  - ( ((Int_t)(mh-80600000000))/10000 )*10000;
  return -1;
}

int code(double mh){
 return (int)(mh/100000000);
}

void dress2d(TGraph2D *gr){

   int np=gr->GetN();
   for (int p=0;p<np;p++){
	double x = (gr->GetX())[p];
	double y = (gr->GetY())[p];
	double z = (gr->GetZ())[p];
	//gr->SetPoint(np+p,x,-y,z);
	//gr->SetPoint(2*np+p,x,-y,z);
   }
 
}

/*
TGraph2D* supergraph(TGraph2D* gr){
 
   TGraph2D *newGraph = new TGraph2D();
   newGraph->SetName(Form("%s_fine",gr->GetName()));
   //newGraph->GetXaxis()->SetTitle(gr->GetXaxis()->GetTitle());
   //newGraph->GetYaxis()->SetTitle(gr->GetYaxis()->GetTitle());
   newGraph->SetTitle("");

   TTree *tr = new TTree();
   float x,y,f;
   
   tr->Branch("x",&x,"x/Float_t");
   tr->Branch("y",&y,"y/Float_t");
   tr->Branch("f",&f,"f/Float_t");

   double minX = 100000;
   double minY = 100000;
   double maxX = -10;
   double maxY = -10;

   for (int pt = 0 ; pt<gr->GetN(); pt++){
	
        f = (gr->GetZ())[pt];
        x = (gr->GetX())[pt];
        y = (gr->GetY())[pt];
	tr->Fill();

	if (x<minX) minX = x;
	if (y<minY) minY = y;
	if (x>maxX) maxX = x;
	if (y>maxY) maxY = y;

	std::cout << f << ", "  << x << ", " << y << std::endl;
   }

   RooRealVar xr("x","x",0.1,minX,maxX); 
   RooRealVar yr("y","y",0.1,minY,maxY);
   RooSplineND *spline = new RooSplineND("spline","spline",RooArgList(xr,yr),tr,"f",1.,true,"");
   // now fill it 
   int ptn = 0;
   std::cout << "X --> " <<  minX << " -> " <<  maxX << std::endl;
   std::cout << "Y --> " <<  minY << " -> " <<  maxY << std::endl;

   for (double xx=minX;xx<=maxX;xx+=10){
     for (double yy=minY;yy<=maxY;yy+=5){

	xr.setVal(xx);
	yr.setVal(yy);
	double cls = spline->getVal();
	newGraph->SetPoint(ptn,xx,yy,cls);
	ptn++;
     }
   }
   return ((TGraph2D*)newGraph->Clone());
}
*/
struct Point {
  double x=0;
  double y=0;
};

bool sortPoints (Point i,Point j) { return (!(i.x > j.x)); }

void reorderFuckingUselessGraph(TGraph *gr){

   std::vector<Point> points;
   for (int p=0;p<gr->GetN();p++){
	Point pt;
	pt.x = (gr->GetX())[p];
	pt.y = (gr->GetY())[p];
	points.push_back(pt);
   }
   std::sort (points.begin(), points.end(), sortPoints);
   int np = points.size();
   for (int p=0;p<np;p++){
   	std::cout << gr->GetName() << ", "<< p<<", " << points[p].x << ", " << points[p].y <<std::endl;
   	gr->SetPoint(p,points[p].x,points[p].y);
   }
}
void plotContsSingle(TFile *fOUT, std::string dirname, std::string fin, float X, int keepMDM=10){

   //gSystem->Load("libHiggsAnalysisCombinedLimit.so");
   gROOT->SetBatch(1);

   TFile *fiSignals = TFile::Open("signalsVA.root");
   RooWorkspace *workspace = (RooWorkspace*)fiSignals->Get("combinedws");
   TFile *fiSignalsPS = TFile::Open("signalsPS.root");
   RooWorkspace *workspacePS = (RooWorkspace*)fiSignalsPS->Get("combinedws");

   //TFile *fi = TFile::Open("limits-output.root");
   //TFile *fi = TFile::Open("signal-scans.root");
   TFile *fi = TFile::Open(fin.c_str());
   TTree *tree = (TTree*)fi->Get("limit");

   double mh;
   double limit;
   float quantile;
   tree->SetBranchAddress("mh",&mh);
   tree->SetBranchAddress("limit",&limit);
   tree->SetBranchAddress("quantileExpected",&quantile);

   int nvt = tree->GetEntries();
   
   TGraph2D *grV = new TGraph2D(); grV->SetName("vector");
   TGraph2D *grA = new TGraph2D(); grA->SetName("axial");
   TGraph2D *grS = new TGraph2D(); grS->SetName("scalar");
   TGraph2D *grP = new TGraph2D(); grP->SetName("pseudoscalar");


   TGraph2D *grVs = new TGraph2D(); grVs->SetName("vector_signal");
   TGraph2D *grAs = new TGraph2D(); grAs->SetName("axial_signal");
   TGraph2D *grSs = new TGraph2D(); grSs->SetName("scalar_signal");
   TGraph2D *grPs = new TGraph2D(); grPs->SetName("pseudoscalar_signal");

   int ptV=0;
   int ptA=0;
   int ptS=0;
   int ptP=0;

   TGraph *grV_mMED = new TGraph(); grV_mMED->SetName(Form("vector_mMED_mDM%d",keepMDM));
   TGraph *grA_mMED = new TGraph(); grA_mMED->SetName(Form("axial_mMED_mDM%d",keepMDM));
   TGraph *grS_mMED = new TGraph(); grS_mMED->SetName(Form("scalar_mMED_mDM%d",keepMDM));
   TGraph *grP_mMED = new TGraph(); grP_mMED->SetName(Form("pseudoscalar_mMED_mDM%d",keepMDM));
   int ptVm=0;
   int ptAm=0;
   int ptSm=0;
   int ptPm=0;

   grV_mMED->SetLineWidth(2); grV_mMED->SetMarkerSize(1.0);
   grA_mMED->SetLineWidth(2); grA_mMED->SetMarkerSize(1.0);
   grS_mMED->SetLineWidth(2); grS_mMED->SetMarkerSize(1.0);
   grP_mMED->SetLineWidth(2); grP_mMED->SetMarkerSize(1.0);

   for (int i=0; i<nvt;i++){
     //if ( ! ( i%6==X ) ) continue; // 2 or 5
     tree->GetEntry(i);
     if (quantile!=X) continue;
      
     int cd = code(mh);

     float mmed = MMED(mh,cd);
     float mdm  = MDM(mh,cd);

     // onshell crazyness?
     if ((int)mmed==2*( (int)mdm) ) continue;
     //
     //std::cout << " int X = " << i << std::endl;
     //std::cout << mh << ", " << cd << ", " << mmed << ", " << mdm <<  ", " << limit << std::endl;  
     //std::cout << mh << ", " << Form("monojet_signal_signal_%3d%04d%04d",cd,(int)mmed,(int)mdm) << std::endl; 
     //exit();
     
     //std::vector<std::pair<double,double>> pointsV_mMED;
     //std::vector<std::pair<double,double>> pointsA_mMED;
     //std::vector<std::pair<double,double>> pointsS_mMED;
     //std::vector<std::pair<double,double>> pointsP_mMED;

     RooDataHist *dh; 
     if      (cd==801 || cd==800) dh = (RooDataHist*) workspace->data(Form("monojet_signal_signal_%3d%04d%04d",cd,(int)mmed,(int)mdm));
     else if (cd==805 || cd==806) dh = (RooDataHist*) workspacePS->data(Form("monojet_signal_signal_%3d%04d%04d",cd,(int)mmed,(int)mdm));
     double nsignal = 0;
     if (dh) {
     	nsignal = dh->sumEntries();
     }
     if (cd==800) {
	grVs->SetPoint(ptV,mmed,mdm,nsignal);
     	grV->SetPoint(ptV,mmed,mdm,limit);
	ptV++;
	if ( (int)mdm == keepMDM ) { 
		grV_mMED->SetPoint(ptVm,mmed,limit);
		//pointsV_mMED.push_back(std::mk_pair<double,double>(mmed,limit));
		ptVm++;
	}
     } else if (cd==801){
	grAs->SetPoint(ptA,mmed,mdm,nsignal);
     	grA->SetPoint(ptA,mmed,mdm,limit);
	ptA++;
	if ( (int)mdm == keepMDM ) { 
		grA_mMED->SetPoint(ptAm,mmed,limit);
		ptAm++;
	}
     } else if (cd==805){
	grSs->SetPoint(ptS,mmed,mdm,nsignal);
     	grS->SetPoint(ptS,mmed,mdm,limit);
	ptS++;
	if ( (int)mdm == keepMDM ) { 
		grS_mMED->SetPoint(ptSm,mmed,limit);
		ptSm++;
	}
     } else if (cd==806){
	grPs->SetPoint(ptP,mmed,mdm,nsignal);
     	grP->SetPoint(ptP,mmed,mdm,limit);
	ptP++;
	if ( (int)mdm == keepMDM ) { 
     		//std::cout << mh << ", " << cd << ", " << mmed << ", " << mdm <<  ", " << limit <<std::endl;  
		grP_mMED->SetPoint(ptPm,mmed,limit);
		ptPm++;
	}
     }
   }

   // Add a strip of points to the edges of the graphs as contours suck?
   //
   /*
   dress2d(grV);
   dress2d(grA);
   dress2d(grS);
   dress2d(grP);
   */

   TDirectory *fout = fOUT->mkdir(dirname.c_str());
   //TFile *fout = new TDirectory(); 
   // TFile(Form("fout-%s.root",fin.c_str()),"RECREATE");
   fout->WriteTObject(grV);
   fout->WriteTObject(grA);
   fout->WriteTObject(grS);
   fout->WriteTObject(grP);

   reorderFuckingUselessGraph(grV_mMED);
   reorderFuckingUselessGraph(grA_mMED);
   reorderFuckingUselessGraph(grS_mMED);
   reorderFuckingUselessGraph(grP_mMED);

   fout->WriteTObject(grV_mMED);
   fout->WriteTObject(grA_mMED);
   fout->WriteTObject(grS_mMED);
   fout->WriteTObject(grP_mMED);

   fout->WriteTObject(grVs);
   fout->WriteTObject(grAs);
   fout->WriteTObject(grSs);
   fout->WriteTObject(grPs);
   
   //TGraph2D *grVf = (TGraph2D*) supergraph(grV);
   //TGraph2D *grAf = (TGraph2D*) supergraph(grA);
//   TGraph2D *grSf = (TGraph2D*) supergraph(grS);
//   TGraph2D *grPf = (TGraph2D*) supergraph(grP);

   //fout->WriteTObject(grVf);
   //fout->WriteTObject(grAf);
//   fout->WriteTObject(grSf);
//   fout->WriteTObject(grPf);

 //  limit->Draw("limit: ((Int_t)(mh-80100000000))/10000 : (mh-80100000000)  - ( ((Int_t)(mh-80100000000))/10000 )*10000 ","Entry$%6==2")

}

void plotConts(){

        gSystem->Load("libHiggsAnalysisCombinedLimit.so");
   	TFile *fout = new TFile(Form("fout-limits.root"),"RECREATE");

	plotContsSingle(fout, "CentralExpected","limits-all.root",0.5,1);
	plotContsSingle(fout, "CentralObs","limits-all.root",-1,1);
	plotContsSingle(fout, "UpObs","limits-all-up.root",-1,1);
	plotContsSingle(fout, "DnObs","limits-all-dn.root",-1,1);

	//plotContsSingle(fout, "CentralExpected1","limits-all-mu.root",0.5,1);
	//plotContsSingle(fout, "CentralExpected10","limits-all-mu.root",0.5,10);
	//plotContsSingle(fout, "CentralExpected25","limits-all-mu.root",0.5,25);
	//plotContsSingle(fout, "CentralExpected50","limits-all-mu.root",0.5,50);

   	std::cout << " Created File - " << fout->GetName() << std::endl;
   	fout->Close();
}
