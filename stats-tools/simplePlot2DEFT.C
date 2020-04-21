bool isPrelim=true;

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

const double KFMAX=1.4;
const double KVMAX=1.4;
const double KLMAX=24;
const double KFMIN=0.6;
const double KVMIN=0.8;
const double KLMIN=-10;


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
		std::cout << " Look at point  x=" << cv << ", y=" << cf <<  ", deltaNLL=" <<  brv << ", cl=" << clv << std::endl;
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

void getBestFit(TTree* tree,std::string x, std::string y,double &bx,double &by){

	float X, Y, qE;
	float limit;

	tree->SetBranchAddress(Form("%s",x.c_str()),&X);
	tree->SetBranchAddress(Form("%s",y.c_str()),&Y);
	tree->SetBranchAddress("quantileExpected",&qE);
	tree->SetBranchAddress("deltaNLL",&limit);

	int pt = 0;
	for (int i=0;i<tree->GetEntries();i++){
	  tree->GetEntry(i);
	  if ( qE < 0 ) { 
	  	bx=X ;
		by=Y ;
		std::cout << "Best fit = " << bx << " ,  " << by <<std::endl;; 
	  }
	  break;
	}

}

TH2D grKappa(TTree *tree, std::string x, std::string y){

	TGraph2D *gr = new TGraph2D();
	float X, Y, qE;
	float limit;

	//std::string x = "kappa_lambda";
	//std::string y = "trackedParam_;

	tree->SetBranchAddress(Form("%s",x.c_str()),&X);
	tree->SetBranchAddress(Form("%s",y.c_str()),&Y);
	tree->SetBranchAddress("quantileExpected",&qE);
	tree->SetBranchAddress("deltaNLL",&limit);

	int pt = 0;
	for (int i=0;i<tree->GetEntries();i++){
	  tree->GetEntry(i);
	  if (TMath::Abs(2*limit>120) ) continue;
	  if ( qE < 0 ) continue; 
	  gr->SetPoint(pt,X,Y,2*limit); pt++;
	  std::cout << " X " << X << ", Y " << Y << ", 2*deltaNLL " << 2*limit << std::endl;
	}
	gr->Draw("colz");
	gr->SetName(y.c_str());
	TH2D * expected = (TH2D*) gr->GetHistogram();
	expected->SetName(y.c_str());
	expected->SetTitle("");
	expected->GetZaxis()->SetTitleOffset(1.2);
	//expected->GetYaxis()->SetTitle("#it{#kappa}_{F}");
	//expected->GetXaxis()->SetTitle("#it{#kappa}_{V}");
	//expected->GetXaxis()->SetRangeUser(KVMIN,KVMAX);
	//expected->GetYaxis()->SetRangeUser(KFMIN,KFMAX);
	//expected->GetZaxis()->SetTitle("B(H #rightarrow inv.) - 95% CL upper limit");
	//expected->GetXaxis()->SetLimits(KVMIN,KVMAX);
	//expected->GetYaxis()->SetLimits(KFMIN,KFMAX);
	//expected->SetMaximum(1);
	//expected->SetMinimum(0);
	std::cout << " Done, now returning Graph" << std::endl; 
	return *expected;
}

void decorate(TCanvas *can,TH2D &h, std::string ext_text="",double bfx=1., double bfy=1.){

	TLatex * tex = new TLatex();
	tex->SetNDC();
	tex->SetTextFont(42);
	tex->SetLineWidth(2);
	tex->SetTextSize(0.03);
	tex->DrawLatex(0.14,0.93,"L #leq 137 fb^{-1} (13 TeV)");
  	tex->SetTextFont(42);
	tex->SetTextSize(0.06);
		if (isPrelim)	{ 
	        	tex->SetTextSize(0.04);
			tex->DrawLatex(0.155, 0.85, "#bf{CMS} #it{Preliminary}");
		}
		else	tex->DrawLatex(0.14, 0.93, "#bf{CMS}");
	//}


	TGraph *SM = new TGraph();
	SM->SetPoint(0,bfx,bfy);
	SM->SetMarkerColor(kBlack);
	SM->SetMarkerStyle(34);
	SM->SetMarkerSize(1.6);
	SM->Draw("Psame");	
	
	TGraph *Stencil = new TGraph();
	Stencil->SetPoint(0,-1.446,2.161);
	Stencil->SetPoint(1,-1.490,2.124);
	Stencil->SetPoint(2,-1.401,2.196);
	Stencil->SetPoint(3,-1.490,2.196);
	Stencil->SetPoint(4,-1.401,2.124);
	Stencil->SetMarkerColor(kRed);
	Stencil->SetMarkerStyle(20);
	Stencil->SetMarkerSize(0.4);
	Stencil->Draw("Psame");	


	TLegend *leg;
	leg = new TLegend(0.6,0.72,0.82,0.88);
	leg->SetTextSize(0.042);
	leg->SetFillStyle(0);
	//leg->SetTextColor(kWhite);
	leg->SetBorderSize(0);
	TGraph *gr = new TGraph(); gr->SetLineWidth(2); gr->SetMarkerStyle(34); gr->SetLineColor(kWhite); gr->SetMarkerColor(kWhite);
	TGraph *gr2 = new TGraph(); gr2->SetLineWidth(2); gr2->SetLineColor(kWhite); gr2->SetLineStyle(2); 
	gr->SetMarkerSize(2);
	  TLatex *lat = new TLatex();
	  lat->SetTextSize(0.04);
	  lat->SetTextColor(kBlack);
	  lat->SetNDC();
	  //lat->DrawLatex(0.155,0.78,ext_text.c_str());
	can->SetTicky();
	can->SetTickx();

 	TH2D *sig1 = (TH2D*)h.Clone(); sig1->SetName("sigma1");
 	TH2D *sig2 = (TH2D*)h.Clone(); sig1->SetName("sigma2");
	sig1->SetContour(2); sig1->SetContourLevel(1,2.3);
	sig2->SetContour(2); sig2->SetContourLevel(1,5.99);
	sig1->SetLineWidth(3);
	sig2->SetLineWidth(3);
	sig1->SetLineStyle(1);
	sig2->SetLineStyle(2);
	sig1->SetLineColor(kBlack);
	sig2->SetLineColor(kBlack);
	sig1->Draw("cont3same");
	sig2->Draw("cont3same");
  	leg->AddEntry(SM,"Best fit","P");	
  	leg->AddEntry(sig1,"68% CL","L");	
  	leg->AddEntry(sig2,"95% CL","L");	
	leg->Draw();
	can->RedrawAxis();
}
void simplePlot2D(std::string file,std::string x, std::string y, std::string strx, std::string stry, double xmin, double xmax, double ymin, double ymax){

	
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
	gStyle->SetTitleXOffset(0.95);//0.9);
	gStyle->SetTitleYOffset(1.06); // => 1.15 if exponents

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


	// *************************************************************
	 int ncontours = 16; 
	 double stops[5]   = {0.0 ,  1,   2.    , 5     , 10    };  
	 double blue[5]    = {1.0 ,  1.  , 1  , 1     , 1.00   }; 
	 double green[5]   = {0.25 , 0.3 ,   0.5  , 0.75    , 1.00   }; 
	 double red [5]    = {0.1,  0.15 ,   0.4 , 0.6     , 1.00   }; 
	 
	 int npoints = 5; 
	 TColor::CreateGradientColorTable(npoints, stops, red, green, blue, ncontours);
	 gStyle->SetNumberContours(ncontours); 
	double bx,by; 
	
	TFile *fi2 = TFile::Open(file.c_str());
	TTree *tree2 = (TTree*)fi2->Get("limit");
	TH2D expected2(grKappa(tree2,x,y));
	TH2D dummyK2("dummyK","dummy",1,xmin,xmax,1,ymin,ymax);
	dummyK2.SetTitle("");
	dummyK2.GetZaxis()->SetTitleOffset(1.2);
	dummyK2.GetXaxis()->SetTitle(strx.c_str());
	dummyK2.GetYaxis()->SetTitle(stry.c_str());
	dummyK2.GetZaxis()->SetTitle("q(#kappa_{#lambda},#kappa_{V})");
	TCanvas *can2 = new TCanvas("cc2","c",800,720);
	can2->cd();
	expected2.Draw("colz");
	dummyK2.Draw();
	//double bx,by; 
	getBestFit(tree2,x,y,bx,by);
	decorate(can2,expected2,"#it{#kappa}_{F} = 1",bx,by);
	can2->SaveAs(Form("scan2D_%s_%s.pdf",x.c_str(),y.c_str()));
	can2->SaveAs(Form("scan2D_%s_%s.png",x.c_str(),y.c_str()));
}
