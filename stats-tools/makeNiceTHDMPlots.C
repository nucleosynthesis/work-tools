/*
#include "TMath.h"
#include "TColor.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TROOT.h"
#include "TSystem.h"
#include "TLegend.h"
#include "TLatex.h"
#include "TEfficiency.h"
#include "TGraphAsymmErrors.h"
#include "TGraph2D.h"
#include "TGraph.h"
#include "RooDataHist.h"
#include "RooWorkspace.h"
#include <iostream>
#include <string>
#include <vector>


struct Point {
  double x=0;
  double y=0;
};

bool sortPoints (Point i,Point j) { return (!(i.y > j.y)); }

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
   	//std::cout << gr->GetName() << ", "<< p<<", " << points[p].x << ", " << points[p].y <<std::endl;
   	gr->SetPoint(p,points[p].x,points[p].y);
   }
}

TGraph *giveMeOneLine(TGraph *grIn, double xmin, double xmax, double ymin, double ymax){

	TGraph *gr_keep = new TGraph(); //grIn->Clone(); gr_keep->SetName("FuckROOT");
	int npoints = grIn->GetN();
	int kp=0;
	for (int p=0;p<npoints;p++){
		double x=grIn->GetX()[p];
		double y=grIn->GetY()[p];

		//if (x>xmin && x<xmax && y>ymin && y<ymax) {
		//if (y>ymax) break; 
		if (x>xmin && x < xmax && y > ymin && y < ymax){
			gr_keep->SetPoint(kp,x,y);
			kp++;
		} else {
			//std::cout << " Gone ! = " << x <<", "<<y<<std::endl;
			continue;
		}	
	}
	for (int p2=0;p2<gr_keep->GetN();p2++){

		double x=gr_keep->GetX()[p2];
		double y=gr_keep->GetY()[p2];
		std::cout << " Yo ! = " << p2 << ", "<< x <<", "<<y<<std::endl;
	}

	gr_keep->SetMarkerColor(grIn->GetMarkerColor());
	gr_keep->SetLineColor(grIn->GetLineColor());
	gr_keep->SetLineStyle(grIn->GetLineStyle());
	gr_keep->SetLineWidth(grIn->GetLineWidth());
	reorderFuckingUselessGraph(gr_keep);	
	return (TGraph*)gr_keep;

}

TGraph * iHateROOT(TGraph *grIn){

	TGraph *gr_keep = new TGraph(); //grIn->Clone(); gr_keep->SetName("FuckROOT");
	int npoints = grIn->GetN();
	int kp=0;
	for (int p=0;p<npoints;p++){
		double x=grIn->GetX()[p];
		double y=grIn->GetY()[p];

		if (x>=-0.8 && x <= 0.8 && y<=10 && y>=5E-2) {
			gr_keep->SetPoint(kp,x,y);
			kp++;
		} else {
			continue;
		}	
	}


	return (TGraph*)gr_keep;
	//grIn =(Tgraph*) gr_keep->Clone();
}
*/


double MARKERSIZE=0.4;

void recenterToZero(TH2F *h){
  for (int i=1;i<=h->GetNbinsX();i++){
    for (int j=1;j<=h->GetNbinsY();j++){
       if (h->GetBinContent(i,j)<0) h->SetBinContent(i,j,0.001);
    }
  }
}

void Type1(){

	TFile *fi = TFile::Open("outplots-2hdm-rotatey.root");
	//TFile *fi = TFile::Open("outplots-2hdm-1Dfindcrossing.root");
	TFile *fi_exp = TFile::Open("outplots-2hdm-rotatey-exp.root");

	TCanvas *can = new TCanvas(); 
	TH1F *h_dummy = new TH1F("dummy",";cos(#beta-#alpha); tan#beta",1,-0.8,0.8);
	h_dummy->GetZaxis()->SetTitle("#Deltaq(cos(#beta-#alpha),tan#beta)");
	h_dummy->GetZaxis()->SetTitleOffset(0.6);
	h_dummy->SetMaximum(10);
	h_dummy->SetMinimum(0.1);
	h_dummy->GetYaxis()->SetNdivisions(210);
	h_dummy->GetZaxis()->SetNdivisions(210);
	h_dummy->GetYaxis()->SetMoreLogLabels();

	/* David Style */
	//h_dummy->GetXaxis()->SetLabelFont(62);
	h_dummy->GetXaxis()->SetLabelSize(0.03);
	h_dummy->GetXaxis()->SetLabelOffset(0.015);
	//h_dummy->GetXaxis()->SetTitleFont(62);
	h_dummy->GetXaxis()->SetTitleColor(1);
	h_dummy->GetXaxis()->SetTitleOffset(1.20);
	h_dummy->SetNdivisions(50005, "X");
	h_dummy->GetXaxis()->SetMoreLogLabels();
	h_dummy->GetXaxis()->SetNoExponent();
	h_dummy->GetXaxis()->SetLabelSize(0.040);
	h_dummy->SetYTitle("tan#beta");
	//h_dummy->GetYaxis()->SetLabelFont(62);
	//h_dummy->GetYaxis()->SetTitleOffset(1.60);
	h_dummy->GetYaxis()->SetLabelSize(0.034);
	h_dummy->GetYaxis()->SetNoExponent();
	h_dummy->SetNdivisions(50005, "Y");
	h_dummy->GetYaxis()->SetMoreLogLabels();



	h_dummy->Draw("axis");
	TGraph *type1 = (TGraph*)fi->Get("type1");
	TGraph2D *type1_color = (TGraph2D*)fi->Get("type1_minscan");
	TH2F *type1_color_h = (TH2F*)type1_color->GetHistogram(); 
	
	recenterToZero(type1_color_h);

	type1_color_h->SetMaximum(11); 
	type1_color_h->SetMinimum(0); 

	TGraph *type1_e = (TGraph*)fi_exp->Get("type1");
	type1_e->SetLineColor(kRed+1); type1_e->SetLineWidth(3);
	type1_e->SetMarkerColor(kRed+1);

	//type1 = iHateROOT(type1);
	//type1_e = iHateROOT(type1_e);
	

	type1->SetLineColor(1); 
	//type1->SetLineWidth(2203);
	//type1->SetLineColor(kYellow);
	type1->SetLineStyle(1);
	type1->SetLineWidth(3);
	//
	//
	//TGraph *type1_left = (TGraph*)  giveMeOneLine(type1,-0.8,0,1E-2,10);
	//TGraph *type1_right = (TGraph*)  giveMeOneLine(type1,0,0.8,1E-2,10);
	type1_color_h->Draw("colzsame");
	type1->Draw("p");
	//type1_right->Draw("L");

	/*
	TGraph2D *grtype1_col = (TGraph2D*)fi->Get("type1_minscan");
	TH2F * type1_col= (TH2F*) grtype1_col->GetHistogram();
	type1_col->SetContour(2);
	type1_col->SetContourLevel(1,5.99);
	type1_col->SetFillColor(kPink); 
	type1_col->Draw("cont3");
	*/
	//type1->Draw("f");


	type1_e->Draw("p");

	type1->SetMarkerSize(MARKERSIZE);
	type1_e->SetMarkerSize(MARKERSIZE);

	TLine *line = new TLine(0,h_dummy->GetYaxis()->GetXmin(),0,10);
	line->SetLineColor(kRed+1);
	line->SetLineStyle(2);
	line->SetLineWidth(2);
	line->Draw();

	TGraph *bfpoint = (TGraph*)fi->Get("best_fit_type1");
	bfpoint->SetMarkerStyle(34);
	bfpoint->SetMarkerSize(2.);
	bfpoint->SetMarkerColor(kBlack);
	bfpoint->Draw("p");


	TLatex *   texCMS = new TLatex(0.18,0.22,"2HDM Type I");
	TLegend *WHITEBOX = new TLegend(0.16,0.2,0.42,0.26);
	//WHITEBOX->SetFillColor(kWhite);
	//WHITEBOX->SetBorderSize(1);
	//WHITEBOX->Draw();
	texCMS->SetNDC();
	texCMS->SetTextFont(42);
	texCMS->SetLineWidth(2);
	texCMS->SetTextSize(0.042); texCMS->Draw();




	TLatex * tex = new TLatex();
	tex->SetNDC();
	tex->SetTextFont(42);
	tex->SetLineWidth(2);
	tex->SetTextSize(0.035);
	tex->DrawLatex(0.42,0.93,"#leq 5.1 fb^{-1} (7 TeV) + #leq 19.7 fb^{-1} (8 TeV)");
	tex->SetTextAlign(31);
  	tex->SetTextFont(63);
  	tex->SetTextSize(25);
  	tex->SetTextAngle( 0);
  	tex->SetTextColor(kBlack);
  	tex->DrawLatex(0.2, 0.93, "CMS");

  	tex->SetTextFont(53);
  	tex->SetTextSize(25);
  	tex->DrawLatex(0.4, 0.93, "Preliminary");


	tex->SetTextFont(42);
	tex->SetTextAngle(270);
	tex->SetTextSize(0.045);
	//tex->DrawLatex(0.965,0.965,"#Deltaq[cos(#beta-#alpha),tan#beta]");
	tex->DrawLatex(0.95,0.9,"#Deltaq");

	TLegend *leg = new TLegend(0.56,0.2,0.84,0.3);
	leg->SetFillColor(10); leg->SetTextFont(42);
	leg->SetBorderSize(0);
	leg->AddEntry(type1,"Observed 95% CL","L");
	leg->AddEntry(type1_e,"Expected 95% CL","L");

	TLegend *leg2 = new TLegend(0.57,0.15,0.84,0.2);
	leg2->SetFillColor(10); leg2->SetTextFont(42);
	leg2->SetNColumns(2);
	leg2->SetBorderSize(0);
	leg2->AddEntry(line,"SM","L");
	leg2->AddEntry(bfpoint,"Best fit","P");
	//leg->AddEntry(type1,"Observed 95% CL","L");
	//
	leg->Draw(); 
	leg2->Draw(); 

	can->SetLogy();
	can->RedrawAxis();
	can->SaveAs("type_1.pdf");


}
void Type2(){

	TFile *fi = TFile::Open("outplots-2hdm-rotatey.root");
	TFile *fi_exp = TFile::Open("outplots-2hdm-rotatey-exp.root");
	//TFile *fi_exp = TFile::Open("outplots-2hdm-rotatey.root");

	TCanvas *can = new TCanvas(); 
	TH1F *h_dummy = new TH1F("dummy",";cos(#beta-#alpha); tan#beta",1,-0.8,0.8);

	h_dummy->SetMaximum(10);
	h_dummy->GetZaxis()->SetTitle("-2 #Delta Log(L)");
	h_dummy->SetMinimum(0.1);
	h_dummy->GetYaxis()->SetNdivisions(210);
	h_dummy->GetYaxis()->SetMoreLogLabels();
	h_dummy->Draw("axis");

	//h_dummy->GetXaxis()->SetLabelFont(62);
	h_dummy->GetXaxis()->SetLabelSize(0.03);
	h_dummy->GetXaxis()->SetLabelOffset(0.015);
	//h_dummy->GetXaxis()->SetTitleFont(62);
	h_dummy->GetXaxis()->SetTitleColor(1);
	h_dummy->GetXaxis()->SetTitleOffset(1.20);
	h_dummy->SetNdivisions(50005, "X");
	h_dummy->GetXaxis()->SetMoreLogLabels();
	h_dummy->GetXaxis()->SetNoExponent();
	h_dummy->GetXaxis()->SetLabelSize(0.040);
	h_dummy->SetYTitle("tan#beta");
	//h_dummy->GetYaxis()->SetLabelFont(62);
	//h_dummy->GetYaxis()->SetTitleOffset(1.60);
	h_dummy->GetYaxis()->SetLabelSize(0.034);
	h_dummy->GetYaxis()->SetNoExponent();
	h_dummy->SetNdivisions(50005, "Y");
	h_dummy->GetYaxis()->SetMoreLogLabels();



	TGraph2D *type2_color = (TGraph2D*)fi->Get("type2_minscan");
	TH2F *type2_color_h = (TH2F*)type2_color->GetHistogram(); 

	TGraph *type2 = (TGraph*)fi->Get("type2");
	type2->SetLineColor(1); type2->SetLineWidth(3);

	recenterToZero(type2_color_h);
	type2_color_h->SetMaximum(11); 
	type2_color_h->SetMinimum(0); 
	type2_color_h->Draw("colzsame");
	type2->Draw("p");

	TGraph *type2_e = (TGraph*)fi_exp->Get("type2");
	type2_e->SetLineColor(kRed+1); type2_e->SetLineWidth(3);
	type2_e->SetMarkerColor(kRed+1);
	type2_e->Draw("p");


	type2->SetMarkerSize(MARKERSIZE);
	type2_e->SetMarkerSize(MARKERSIZE);

	TLine *line = new TLine(0,h_dummy->GetYaxis()->GetXmin(),0,10);
	line->SetLineColor(kRed+1);
	line->SetLineStyle(2);
	line->SetLineWidth(2);
	line->Draw();

	TGraph *bfpoint = (TGraph*)fi->Get("best_fit_type2");
	bfpoint->SetMarkerStyle(34);
	bfpoint->SetMarkerSize(2.);
	bfpoint->SetMarkerColor(kBlack);
	bfpoint->Draw("p");

	TLatex *   texCMS = new TLatex(0.18,0.84,"2HDM Type II");
	TLegend *WHITEBOX = new TLegend(0.16,0.82,0.42,0.88);
	WHITEBOX->SetFillColor(kWhite);
	//WHITEBOX->SetBorderSize(1);
	WHITEBOX->SetLineColor(1);
	//WHITEBOX->SetLineWidth(2);
	WHITEBOX->Draw();
	texCMS->SetNDC();
	texCMS->SetTextFont(42);
	texCMS->SetLineWidth(2);
	texCMS->SetTextSize(0.042); texCMS->Draw();

	TLatex * tex = new TLatex();
	tex->SetNDC();
	tex->SetTextFont(42);
	tex->SetLineWidth(2);
	tex->SetTextSize(0.035);
	tex->Draw();
	tex->DrawLatex(0.42,0.93,"#leq 5.1 fb^{-1} (7 TeV) + #leq 19.7 fb^{-1} (8 TeV)");
	tex->SetTextAlign(31);
  	tex->SetTextFont(63);
  	tex->SetTextSize(25);
  	tex->SetTextAngle( 0);
  	tex->SetTextColor(kBlack);
  	tex->DrawLatex(0.2, 0.93, "CMS");

  	tex->SetTextFont(53);
  	tex->SetTextSize(25);
  	tex->DrawLatex(0.4, 0.93, "Preliminary");

	tex->SetTextFont(42);
	tex->SetTextAngle(270);
	tex->SetTextSize(0.045);

	//tex->DrawLatex(0.965,0.965,"#Deltaq[cos(#beta-#alpha), tan#beta]");
	tex->DrawLatex(0.95,0.9,"#Deltaq");
	//tex->DrawLatex(0.95,0.965,"-2#DeltaLog(L)");

	TLegend *leg = new TLegend(0.56,0.2,0.84,0.3);
	leg->SetFillColor(10); leg->SetTextFont(42);
	leg->SetBorderSize(0);
	leg->AddEntry(type2,"Observed 95% CL","L");
	leg->AddEntry(type2_e,"Expected 95% CL","L");

	TLegend *leg2 = new TLegend(0.57,0.15,0.84,0.2);
	leg2->SetFillColor(10); leg2->SetTextFont(42);
	leg2->SetNColumns(2);
	leg2->SetBorderSize(0);
	leg2->AddEntry(line,"SM","L");
	leg2->AddEntry(bfpoint,"Best fit","P");
	//leg->AddEntry(type1,"Observed 95% CL","L");
	//
	leg->Draw(); 
	leg2->Draw(); 

	can->SetLogy();
	can->RedrawAxis();
	can->SaveAs("type_2.pdf");


}

void Type1_sanity_check(){

	TFile *fi = TFile::Open("outplots-2hdm-rotatey.root");
	//TFile *fi_exp = TFile::Open("outplots-2hdm-rotatey-exp.root");

	TGraph *type1 = (TGraph*) fi->Get("type1");

	TGraph2D *ku_gr = (TGraph2D*)fi->Get("t1_ku");	
	TGraph2D *kV_gr = (TGraph2D*)fi->Get("t1_kV");	


	TCanvas *can = new TCanvas();
	ku_gr->SetMaximum(3);
	ku_gr->Draw("colz");
	ku_gr->GetXaxis()->SetTitle("cos(#beta-#alpha)");
	ku_gr->GetYaxis()->SetTitle("tan#beta");
	ku_gr->SetTitle("#kappa_{F}");
	type1->Draw("p");
	can->SetLogy();
	can->RedrawAxis();
	can->SaveAs("type1_ku.pdf");

	TCanvas *can2 = new TCanvas();
	kV_gr->SetMaximum(1.2);
	kV_gr->Draw("colz");
	kV_gr->GetXaxis()->SetTitle("cos(#beta-#alpha)");
	kV_gr->GetYaxis()->SetTitle("tan#beta");
	kV_gr->SetTitle("#kappa_{V}");
	type1->Draw("p");
	can2->SetLogy();
	can2->RedrawAxis();
	can2->SaveAs("type1_kV.pdf");
		
}

void Type2_sanity_check(){

	TFile *fi = TFile::Open("outplots-2hdm-rotatey.root");
	//TFile *fi_exp = TFile::Open("outplots-2hdm-rotatey-exp.root");

	TGraph *type2 = (TGraph*) fi->Get("type2");

	TGraph2D *ku_gr = (TGraph2D*)fi->Get("t2_ku");	
	TGraph2D *kV_gr = (TGraph2D*)fi->Get("t2_kV");	
	TGraph2D *kd_gr = (TGraph2D*)fi->Get("t2_kd");	


	TCanvas *can = new TCanvas();
	ku_gr->SetMaximum(3);
	ku_gr->Draw("colz");
	ku_gr->GetXaxis()->SetTitle("cos(#beta-#alpha)");
	ku_gr->GetYaxis()->SetTitle("tan#beta");
	ku_gr->SetTitle("#kappa_{u}");
	type2->Draw("p");
	can->SetLogy();
	can->RedrawAxis();
	can->SaveAs("type2_ku.pdf");

	TCanvas *can2 = new TCanvas();
	kV_gr->SetMaximum(1.2);
	kV_gr->Draw("colz");
	kV_gr->GetXaxis()->SetTitle("cos(#beta-#alpha)");
	kV_gr->GetYaxis()->SetTitle("tan#beta");
	kV_gr->SetTitle("#kappa_{V}");
	type2->Draw("p");
	can2->SetLogy();
	can2->RedrawAxis();
	can2->SaveAs("type2_kV.pdf");


	TCanvas *can3 = new TCanvas();
	kd_gr->SetMaximum(2.5);
	kd_gr->SetMinimum(-2.5);
	kd_gr->Draw("colz");
	kd_gr->GetXaxis()->SetTitle("cos(#beta-#alpha)");
	kd_gr->GetYaxis()->SetTitle("tan#beta");
	kd_gr->SetTitle("#kappa_{d}");
	type2->Draw("p");


	can3->SetLogy();
	can3->RedrawAxis();
	can3->SaveAs("type2_kd.pdf");

		
}

void makeNiceTHDMPlots(){
	gROOT->ProcessLine(".x paperStyle.C");
   gROOT->LoadMacro("CMS_lumi.C");
   int ncontours = 99; 
   
   double stops[5]   = {0.0 ,  .1,   .25 , .5     , 1    };  
   double blue[5]    = {1.0 ,  1.  ,   1.0  , 1.0     , 1.00   }; 
   double green[5]   = {0.25 , 0.3 ,   0.5  , 0.75    , 1.00   }; 
   double red [5]    = {0.1,  0.15 ,   0.4 , 0.6     , 1.00   }; 
   
   int npoints = 5; 
   TColor::CreateGradientColorTable(npoints, stops, red, green, blue, ncontours); 
   gStyle->SetNumberContours(ncontours); 

	Type1();
	Type2();
	
//	Type1_sanity_check();
//	Type2_sanity_check();
}

