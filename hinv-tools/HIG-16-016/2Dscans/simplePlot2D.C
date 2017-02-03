bool isPrelim=false;

#include "TGraph2D.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TGraph.h"
#include "TFile.h"
#include "TTree.h"
#include "TAxis.h"
#include "TH2F.h"
#include "TH2D.h"
#include "TCanvas.h"
#include "TColor.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TMath.h"
#include "TLine.h"

#include <string>
#include <iostream>

const double KFMAX=1.46;
const double KVMAX=1.46;
const double MUFMAX=2.5;
const double MUVMAX=2.;
const double KFMIN=0.54;
const double KVMIN=0.52;
const double MUFMIN=0.5;
const double MUVMIN=0.6;


void printRanges(TH2D *br, TH2D * cl){
	double brmin=10;
	double brmax=-1;
	for (int bx=1;bx<=br->GetNbinsX();bx++){
	  for (int by=1;by<=br->GetNbinsX();by++){
	  	double cv = br->GetXaxis()->GetBinCenter(bx);
	  	double cf = br->GetXaxis()->GetBinCenter(by);
		double brv = br->GetBinContent(bx,by);
		int bin =  cl->FindBin(cv,cf);

		double clv =  cl->GetBinContent(bin);

		if (clv>5.99 ) continue;
		std::cout << " Look at point  cv=" << cv << ", cf=" << cf <<  ", BR=" <<  brv << ", cl=" << clv << std::endl;
		if (brv > brmax ) brmax = brv;
		if (brv < brmin ) brmin = brv;
	  }
	}
	std::cout << " Found BR(inv) limit ranges between " << brmin << " - " << brmax << " in 95% region "<< std::endl;
}

//TH2D grKappa(TTree *tr, std::string x, std::string y, double quantileExpected=0.5){
/*
TH2D grKappa(TTree *tree, double quantileExpected){

	TGraph2D *gr = new TGraph2D();
	float X, Y, qE;
	double limit;

	std::string x = "trackedParam_proc_scaling_muV";
	std::string y = "trackedParam_proc_scaling_muF";

	tree->SetBranchAddress(Form("%s",x.c_str()),&X);
	tree->SetBranchAddress(Form("%s",y.c_str()),&Y);
	tree->SetBranchAddress("quantileExpected",&qE);
	tree->SetBranchAddress("limit",&limit);

	int pt = 0;
	for (int i=0;i<tree->GetEntries();i++){
	  tree->GetEntry(i);
	  if (TMath::Abs(qE-quantileExpected)>0.01) continue;
	  gr->SetPoint(pt,TMath::Sqrt(X),TMath::Sqrt(Y),limit); pt++;
	  std::cout << " Lim " << X << ", " << Y << ", " << limit << std::endl;
	}
	gr->Draw("colz");
	TH2D * expected = (TH2D*) gr->GetHistogram();
	expected->SetTitle("");
	expected->GetZaxis()->SetTitleOffset(1.2);
	expected->GetYaxis()->SetTitle("#kappa_{F}");
	expected->GetXaxis()->SetTitle("#kappa_{V}");
	expected->GetZaxis()->SetTitle("B(H #rightarrow inv.) - 95% CL upper limit");
	return *expected;
}
*/

TH2D grKappa(TTree *tree, double quantileExpected){

	TGraph2D *gr = new TGraph2D();
	float X, Y, qE;
	double limit;

	std::string x = "trackedParam_CV";
	std::string y = "trackedParam_CF";

	tree->SetBranchAddress(Form("%s",x.c_str()),&X);
	tree->SetBranchAddress(Form("%s",y.c_str()),&Y);
	tree->SetBranchAddress("quantileExpected",&qE);
	tree->SetBranchAddress("limit",&limit);

	int pt = 0;
	for (int i=0;i<tree->GetEntries();i++){
	  tree->GetEntry(i);
	  if (TMath::Abs(qE-quantileExpected)>0.01) continue;
	  gr->SetPoint(pt,X,Y,limit); pt++;
	//  std::cout << " Lim " << X << ", " << Y << ", " << limit << std::endl;
	}
	gr->Draw("colz");
	TH2D * expected = (TH2D*) gr->GetHistogram();
	expected->SetTitle("");
	expected->GetZaxis()->SetTitleOffset(1.2);
	expected->GetYaxis()->SetTitle("#it{#kappa}_{F}");
	expected->GetXaxis()->SetTitle("#it{#kappa}_{V}");
	expected->GetXaxis()->SetRangeUser(KVMIN,KVMAX);
	expected->GetYaxis()->SetRangeUser(KFMIN,KFMAX);
	expected->GetZaxis()->SetTitle("B(H #rightarrow inv.) - 95% CL upper limit");
	//expected->GetXaxis()->SetLimits(KVMIN,KVMAX);
	//expected->GetYaxis()->SetLimits(KFMIN,KFMAX);
	expected->SetMaximum(1);
	expected->SetMinimum(0);
	return *expected;
}

TH2D grMu(TTree *tree, double quantileExpected){

	TGraph2D *gr = new TGraph2D();
	float X, Y, qE;
	double limit;

	std::string x = "trackedParam_proc_scaling_muV";
	std::string y = "trackedParam_proc_scaling_muF";

	tree->SetBranchAddress(Form("%s",x.c_str()),&X);
	tree->SetBranchAddress(Form("%s",y.c_str()),&Y);
	tree->SetBranchAddress("quantileExpected",&qE);
	tree->SetBranchAddress("limit",&limit);

	int pt = 0;
	for (int i=0;i<tree->GetEntries();i++){
	  tree->GetEntry(i);
	  if (TMath::Abs(qE-quantileExpected)>0.001) continue;
	  gr->SetPoint(pt,X,Y,limit); pt++;
	  //std::cout << " Lim " << X << ", " << Y << ", " << limit << std::endl;
	}
	gr->Draw("colz");
	TH2D * expected = (TH2D*) gr->GetHistogram();
	expected->SetTitle("");
	expected->GetZaxis()->SetTitleOffset(1.2);
	expected->GetYaxis()->SetTitle("#it{#mu}_{ggH}");
	expected->GetXaxis()->SetTitle("#it{#mu}_{qqH,VH}");
	expected->GetZaxis()->SetTitle("B(H #rightarrow inv.) - 95% CL upper limit");
	expected->GetXaxis()->SetRangeUser(MUVMIN,MUVMAX);
	expected->GetYaxis()->SetRangeUser(MUFMIN,MUFMAX);
	//expected->GetXaxis()->SetLimits(MUVMIN,MUVMAX);
	//expected->GetYaxis()->SetLimits(MUFMIN,MUFMAX);

	expected->SetMaximum(0.6);
	expected->SetMinimum(0.05);
	return *expected;
}
void decorate(TCanvas *can,TH2D &h, bool addLHC=true){

	TLatex * tex = new TLatex();
	tex->SetNDC();
	tex->SetTextFont(42);
	tex->SetLineWidth(2);
	tex->SetTextSize(0.03);
	tex->DrawLatex(0.32,0.93,"4.9 fb^{-1} (7 TeV) + 19.7 fb^{-1} (8 TeV) + 2.3 fb^{-1} (13 TeV)");
  	tex->SetTextFont(42);
	tex->SetTextSize(0.06);
	//if (!addLHC){
	//        tex->SetTextSize(0.04);
	//	tex->SetTextColor(kWhite);
  //		if (isPrelim)	tex->DrawLatex(0.155, 0.85, "#bf{CMS} #it{Preliminary}");
  //		else	tex->DrawLatex(0.155, 0.85, "#bf{CMS}");
	//} else {
		if (isPrelim)	{ 
	        	tex->SetTextSize(0.04);
			tex->DrawLatex(0.155, 0.85, "#bf{CMS} #it{Preliminary}");
		}
		else	tex->DrawLatex(0.14, 0.93, "#bf{CMS}");
	//}


	TGraph *SM = new TGraph();
	SM->SetPoint(0,1,1);
	SM->SetMarkerColor(kOrange);
	SM->SetMarkerStyle(33);
	SM->SetMarkerSize(4);
	SM->Draw("Psame");	

	TLegend *leg;
	if (addLHC) {
	  if (isPrelim) leg = new TLegend(0.14,0.56,0.4,0.83);
	  else leg = new TLegend(0.14,0.62,0.4,0.89);
	}
	else leg = new TLegend(0.52,0.84,0.78,0.89);
	leg->SetTextSize(0.042);
	leg->SetFillStyle(0);
	leg->SetTextColor(kWhite);
	leg->SetBorderSize(0);
	TGraph *gr = new TGraph(); gr->SetLineWidth(2); gr->SetMarkerStyle(34); gr->SetLineColor(kWhite); gr->SetMarkerColor(kWhite);
	TGraph *gr2 = new TGraph(); gr2->SetLineWidth(2); gr2->SetLineColor(kWhite); gr2->SetLineStyle(2); 
	gr->SetMarkerSize(2);
	if (addLHC){
	  leg->AddEntry(SM,"SM production","P");
	  leg->AddEntry(gr,"LHC best fit","P");
	  leg->AddEntry(gr, "68% CL","L");
	  leg->AddEntry(gr2,"95% CL","L");
	  leg->Draw();
	} else {
	  TLatex *lat = new TLatex();
	  lat->SetTextSize(0.04);
	  lat->SetTextColor(kWhite);
	  lat->DrawLatex(1.05,1.05,"SM production");
	}
	can->SetTicky();
	can->SetTickx();
	can->RedrawAxis();
}
void simplePlot2D(){
	
	///gROOT->ProcessLine(".x paperStyle.C");
	
	gStyle->SetCanvasDefH(600); //Height of canvas
	gStyle->SetCanvasDefW(640); //Width of canvas
	gStyle->SetCanvasDefX(0);   //POsition on screen
	gStyle->SetCanvasDefY(0);

	gStyle->SetPadLeftMargin(0.125);//0.16);
	gStyle->SetPadRightMargin(0.165);//0.02);
	gStyle->SetPadTopMargin(0.085);//0.02);
	gStyle->SetPadBottomMargin(0.12);//0.02);

	  // For g axis titles:
	gStyle->SetTitleColor(1, "XYZ");
	gStyle->SetTitleFont(42, "XYZ");
	gStyle->SetTitleSize(0.045, "Z");
	gStyle->SetTitleSize(0.055, "XY");
	gStyle->SetTitleXOffset(1.0);//0.9);
	gStyle->SetTitleYOffset(1.12); // => 1.15 if exponents

	// For g axis labels:
	gStyle->SetLabelColor(1, "XYZ");
	gStyle->SetLabelFont(42, "XYZ");
	gStyle->SetLabelOffset(0.007, "XYZ");
	gStyle->SetLabelSize(0.04, "XYZ");

	// Legends
	gStyle->SetLegendBorderSize(0);
	gStyle->SetLegendFillColor(kWhite);
	gStyle->SetLegendFont(42);

	gStyle->SetOptStat(0);
	//gStyle->SetPalette(51);

        /* 
	// Fewer colors, one band per 0.1 
	// *************************************************************
	 int ncontours = 10; 
	 double stops[6]   = {0.0 , .2,   .4,   .6,    .8,    1};  
	 double blue[6]    = {1.0 ,  1,    1,    1,     1,    1}; 
	 double green[6]   = {0.1,  0.3,  0.5,  0.72,   0.82, 1}; 
	 double red [6]    = {0.1,  0.2,  0.24, 0.45,   0.7,  1}; 
	 
	 int npoints = 6; 
	 TColor::CreateGradientColorTable(npoints, stops, red, green, blue, ncontours); 
	 gStyle->SetNumberContours(ncontours); 
	//gStyle->SetPalette(kCherry);
	// *************************************************************
	*/

	// *************************************************************
	 int ncontours = 15; 
	 double stops[5]   = {0.0 ,  .1,   .25    , .5     , 1    };  
	 double blue[5]    = {1.0 ,  1.  , 1  , 1     , 1.00   }; 
	 double green[5]   = {0.25 , 0.3 ,   0.5  , 0.75    , 1.00   }; 
	 double red [5]    = {0.1,  0.15 ,   0.4 , 0.6     , 1.00   }; 
	 
	 int npoints = 5; 
	 TColor::CreateGradientColorTable(npoints, stops, red, green, blue, ncontours); 
	 gStyle->SetNumberContours(ncontours); 
	// *************************************************************

	TFile *fi = TFile::Open("allpoints.root");
	TTree *tree = (TTree*)fi->Get("limit");



	TH2D expected(grKappa(tree,-1));
	TH2D dummyK("dummyK","dummy",1,KVMIN,KVMAX,1,KFMIN,KFMAX);
	dummyK.SetTitle("");
	dummyK.GetZaxis()->SetTitleOffset(1.2);
	dummyK.GetYaxis()->SetTitle("#it{#kappa}_{F}");
	dummyK.GetXaxis()->SetTitle("#it{#kappa}_{V}");
	//dummyK.GetXaxis()->SetRangeUser(KVMIN,KVMAX);
	//dummyK.GetYaxis()->SetRangeUser(KFMIN,KFMAX);
	dummyK.GetZaxis()->SetTitle("B(H #rightarrow inv.) - 95% CL upper limit");
	//dummyK.GetXaxis()->SetLimits(KVMIN,KVMAX);
	//dummyK.GetYaxis()->SetLimits(KFMIN,KFMAX);
	//dummyK.SetMaximum(0.8);
	//dummyK.SetMinimum(0.1);
	
	TCanvas *can = new TCanvas("cc","c",800,720);
	can->cd();
	
	//expected.GetXaxis()->SetRangeUser(KVMIN,KVMAX);
	//expected.GetYaxis()->SetRangeUser(KFMIN,KFMAX);

	TFile *flhc = TFile::Open("scan2d_kappa_V_kappa_F_exp.root");
	TGraph *grlhc_68 = (TGraph*) flhc->Get("graph68_comb_0");
	TGraph *grlhc_95 = (TGraph*) flhc->Get("graph95_comb_0");
	TGraph *grlhc_bf = (TGraph*) flhc->Get("comb_best");
	grlhc_68->SetLineColor(kWhite);
        grlhc_95->SetLineColor(kWhite);
	grlhc_bf->SetMarkerStyle(34);
	grlhc_bf->SetMarkerSize(1.8);
	grlhc_bf->SetMarkerColor(kWhite);

	grlhc_68->SetLineWidth(2);
        grlhc_95->SetLineWidth(2);
        grlhc_95->SetLineStyle(2);

	TH2D *histocomb = (TH2D*)flhc->Get("comb_hist_processed");
	
	double xmin =expected.GetXaxis()->GetXmin();
	double xmax =expected.GetXaxis()->GetXmax();
	double ymin =expected.GetYaxis()->GetXmin();
	double ymax =expected.GetYaxis()->GetXmax();
	TLine SMH(KVMIN,1,KVMAX,1);
	TLine SMV(1,KFMIN,1,KFMAX);
//	TLine SMH(xmin,1,xmax,1);
//	TLine SMV(1,ymin,1,ymax);
	SMH.SetLineColor(2);
	SMH.SetLineStyle(2);
	SMV.SetLineColor(2);
	SMV.SetLineStyle(2);

	//dummyK.Draw("AXIS");
	expected.Draw("colz");
	grlhc_68->Draw("Lsame");
        grlhc_95->Draw("Lsame");
        grlhc_bf->Draw("Psame");

	SMH.Draw("L");
	SMV.Draw("L");
	decorate(can,expected);

	printRanges(&expected,histocomb);

	can->SaveAs("couplings_limits.pdf");
	TFile *fiMU = TFile::Open("allpoints_mu.root");
	TTree *treeMU = (TTree*)fiMU->Get("limit");
	TH2D expectedmu(grMu(treeMU,-1));
	TH2D dummyMu("dummyMu","dummy",1,MUVMIN,MUVMAX,1,MUFMIN,MUFMAX);
	dummyMu.SetTitle("");
	dummyMu.GetZaxis()->SetTitleOffset(1.2);
	dummyMu.GetYaxis()->SetTitle("#it{#mu}_{ggH}");
	dummyMu.GetXaxis()->SetTitle("#it{#mu}_{qqH,VH}");
	dummyMu.GetZaxis()->SetTitle("B(H #rightarrow inv.) - 95% CL upper limit");
	//dummyMu.GetXaxis()->SetRangeUser(MUVMIN,MUVMAX);
	//dummyMu.GetYaxis()->SetRangeUser(MUFMIN,MUFMAX);
	//dummyMu.GetXaxis()->SetLimits(MUVMIN,MUVMAX);
	//dummyMu.GetYaxis()->SetLimits(MUFMIN,MUFMAX);
	//dummyMu.SetMaximum(0.8);
	//dummyMu.SetMinimum(0.1);
	//expectedmu.GetXaxis()->SetRangeUser(KVMIN,KVMAX);
	//expectedmu.GetYaxis()->SetRangeUser(KFMIN,KFMAX);

	xmin =expectedmu.GetXaxis()->GetXmin();
	xmax =expectedmu.GetXaxis()->GetXmax();
	ymin =expectedmu.GetYaxis()->GetXmin();
	ymax =expectedmu.GetYaxis()->GetXmax();

	TLine SM2H(MUVMIN,1,MUVMAX,1);
	TLine SM2V(1,MUFMIN,1,MUFMAX);
	//TLine SM2H(xmin,1,xmax,1);
	//TLine SM2V(1,ymin,1,ymax);
	SM2H.SetLineColor(2);
	SM2H.SetLineStyle(2);
	SM2V.SetLineColor(2);
	SM2V.SetLineStyle(2);

	//dummyMu.Draw("axis");
	expectedmu.Draw("colz");

	TH2D *expectedmuCont = (TH2D*)expectedmu.Clone(); 
	//expectedmuCont->SetName("contours");
	//expectedmuCont->SetContour(15);
	//expectedmuCont->Draw("cont2 same");
	SM2H.Draw("L");
	SM2V.Draw("L");
	decorate(can,expectedmu,false);

	can->SaveAs("mu_limits.pdf");
}
