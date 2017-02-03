bool isPrelim=false;

void drawBandyKV(){

	TFile *fi = TFile::Open("alllims.root");
	TTree *limit = (TTree*)fi->Get("limit");

	limit->Draw("limit:trackedParam_CV","trackedParam_CF==1 && TMath::Abs(quantileExpected-0.5)<0.01","L");
	TGraph *grExp = (TGraph*)(gROOT->FindObject("Graph")->Clone()); grExp->SetName("expected");
	limit->Draw("limit:trackedParam_CV","trackedParam_CF==1 && TMath::Abs(quantileExpected-0.16)<0.01","L");
	TGraph *gr16 = (TGraph*)(gROOT->FindObject("Graph")->Clone()); gr16->SetName("e16");
	limit->Draw("limit:trackedParam_CV","trackedParam_CF==1 && TMath::Abs(quantileExpected-0.025)<0.01","L");
	TGraph *gr025 = (TGraph*)(gROOT->FindObject("Graph")->Clone()); gr025->SetName("e025");
	limit->Draw("limit:trackedParam_CV","trackedParam_CF==1 && TMath::Abs(quantileExpected-0.84)<0.01","L");
	TGraph *gr84 = (TGraph*)(gROOT->FindObject("Graph")->Clone()); gr84->SetName("e84");
	limit->Draw("limit:trackedParam_CV","trackedParam_CF==1 && TMath::Abs(quantileExpected-0.975)<0.01","L");
	TGraph *gr975 = (TGraph*)(gROOT->FindObject("Graph")->Clone()); gr975->SetName("e975");
	limit->Draw("limit:trackedParam_CV","trackedParam_CF==1 && TMath::Abs(quantileExpected+1)<0.01","L");
	TGraph *grObs = (TGraph*)(gROOT->FindObject("Graph")->Clone()); grObs->SetName("obs");

	TGraphAsymmErrors *gr68 = new TGraphAsymmErrors();
	TGraphAsymmErrors *gr95 = new TGraphAsymmErrors();

	for (int i=0;i<grExp->GetN();i++){
		double x = grExp->GetX()[i];
		double y = grExp->GetY()[i];

		gr68->SetPoint(i,x,y);
		gr95->SetPoint(i,x,y);
		gr68->SetPointError(i,0,0,y-gr16->GetY()[i],gr84->GetY()[i]-y);
		gr95->SetPointError(i,0,0,y-gr025->GetY()[i],gr975->GetY()[i]-y);

	}
	gStyle->SetCanvasDefH(600); //Height of canvas
	gStyle->SetCanvasDefW(740); //Width of canvas
	gStyle->SetCanvasDefX(0);   //POsition on screen
	gStyle->SetCanvasDefY(0);

	gStyle->SetPadLeftMargin(0.13);//0.16);
	gStyle->SetPadRightMargin(0.105);//0.02);
	gStyle->SetPadTopMargin(0.085);//0.02);
	gStyle->SetPadBottomMargin(0.12);//0.02);


	TCanvas *can = new TCanvas("c","c",800,600);
	can->SetTicky();
	can->SetTickx();

	gStyle->SetTitleColor(1, "XYZ");
	gStyle->SetTitleFont(42, "XYZ");
	gStyle->SetTitleSize(0.045, "Z");
	gStyle->SetTitleSize(0.05, "XY");
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
	
	grExp->GetYaxis()->SetRangeUser(0.,1.4);
	grExp->SetTitle("");
	grExp->GetYaxis()->SetTitle("B(H #rightarrow inv.) - upper limit 95% CL");
	grExp->GetXaxis()->SetTitle("#it{#kappa}_{V}");

	// Make two hists with no line color 
	TH1F *histYellow = new TH1F("yellow","yellow",1,0,1);
	TH1F *histGreen = new TH1F("green","green",1,0,1);
	histGreen->SetLineWidth(0);
	histYellow->SetLineWidth(0);
	histGreen->SetLineColor(kGreen);
	histYellow->SetLineColor(kYellow);
	histGreen->SetFillColor(kGreen);
	histYellow->SetFillColor(kYellow);

	grExp->SetLineWidth(2);
	grExp->SetLineColor(1);
	grExp->SetLineStyle(2);
	gr68->SetFillColor(kGreen);
	gr95->SetFillColor(kYellow);
	gr68->SetLineWidth(0);
	gr95->SetLineWidth(0);
	gr68->SetLineColor(0);
	gr95->SetLineColor(0);
	grObs->SetLineColor(1);
	grObs->SetLineWidth(2);

	grExp->Draw("AL");
	gr95->Draw("E3same");
	gr68->Draw("E3same");
	grExp->Draw("Lsame");
	grObs->Draw("Lsame");
	grObs->SetMarkerSize(0.9);
	grObs->SetMarkerStyle(20);

	TLegend *leg = new TLegend(0.52,0.64,0.89,0.89);
	leg->SetFillColor(0);
	leg->AddEntry(grObs,"Observed","L");
	leg->AddEntry(grExp,"Median expected","L");
	leg->AddEntry(histGreen,"68% expected","F");
	leg->AddEntry(histYellow,"95% expected","F");
	leg->Draw();

	TLatex * tex = new TLatex();
	tex->SetNDC();
	tex->SetTextFont(42);
	tex->SetLineWidth(2);
	tex->SetTextSize(0.04);
	tex->DrawLatex(0.24,0.93,"4.9 fb^{-1} (7 TeV) + 19.7 fb^{-1} (8 TeV) + 2.3 fb^{-1} (13 TeV)");
  	tex->SetTextFont(42);
	tex->SetTextSize(0.054);
  	if( isPrelim) tex->DrawLatex(0.16, 0.82, "#bf{CMS} #it{Preliminary}");
  	else tex->DrawLatex(0.16, 0.82, "#bf{CMS}");
  	tex->DrawLatex(0.16, 0.76, "#it{#kappa}_{F} = 1");
	can->RedrawAxis();
	can->SaveAs("brlims_fixedCF1.pdf");
}

void drawBandyKF(){

	TFile *fi = TFile::Open("alllims.root");
	TTree *limit = (TTree*)fi->Get("limit");

	limit->Draw("limit:trackedParam_CF","trackedParam_CV==1 && TMath::Abs(quantileExpected-0.5)<0.01","L");
	TGraph *grExp = (TGraph*)(gROOT->FindObject("Graph")->Clone()); grExp->SetName("expected");
	limit->Draw("limit:trackedParam_CF","trackedParam_CV==1 && TMath::Abs(quantileExpected-0.16)<0.01","L");
	TGraph *gr16 = (TGraph*)(gROOT->FindObject("Graph")->Clone()); gr16->SetName("e16");
	limit->Draw("limit:trackedParam_CF","trackedParam_CV==1 && TMath::Abs(quantileExpected-0.025)<0.01","L");
	TGraph *gr025 = (TGraph*)(gROOT->FindObject("Graph")->Clone()); gr025->SetName("e025");
	limit->Draw("limit:trackedParam_CF","trackedParam_CV==1 && TMath::Abs(quantileExpected-0.84)<0.01","L");
	TGraph *gr84 = (TGraph*)(gROOT->FindObject("Graph")->Clone()); gr84->SetName("e84");
	limit->Draw("limit:trackedParam_CF","trackedParam_CV==1 && TMath::Abs(quantileExpected-0.975)<0.01","L");
	TGraph *gr975 = (TGraph*)(gROOT->FindObject("Graph")->Clone()); gr975->SetName("e975");
	limit->Draw("limit:trackedParam_CF","trackedParam_CV==1 && TMath::Abs(quantileExpected+1)<0.01","L");
	TGraph *grObs = (TGraph*)(gROOT->FindObject("Graph")->Clone()); grObs->SetName("obs");

	TGraphAsymmErrors *gr68 = new TGraphAsymmErrors();
	TGraphAsymmErrors *gr95 = new TGraphAsymmErrors();

	for (int i=0;i<grExp->GetN();i++){
		double x = grExp->GetX()[i];
		double y = grExp->GetY()[i];

		gr68->SetPoint(i,x,y);
		gr95->SetPoint(i,x,y);
		gr68->SetPointError(i,0,0,y-gr16->GetY()[i],gr84->GetY()[i]-y);
		gr95->SetPointError(i,0,0,y-gr025->GetY()[i],gr975->GetY()[i]-y);

	}
	gStyle->SetCanvasDefH(600); //Height of canvas
	gStyle->SetCanvasDefW(740); //Width of canvas
	gStyle->SetCanvasDefX(0);   //POsition on screen
	gStyle->SetCanvasDefY(0);

	gStyle->SetPadLeftMargin(0.13);//0.16);
	gStyle->SetPadRightMargin(0.105);//0.02);
	gStyle->SetPadTopMargin(0.085);//0.02);
	gStyle->SetPadBottomMargin(0.12);//0.02);


	TCanvas *can = new TCanvas("c","c",800,600);
	can->SetTicky();
	can->SetTickx();

	gStyle->SetTitleColor(1, "XYZ");
	gStyle->SetTitleFont(42, "XYZ");
	gStyle->SetTitleSize(0.045, "Z");
	gStyle->SetTitleSize(0.05, "XY");
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
	
	grExp->GetYaxis()->SetRangeUser(0.,0.8);
	grExp->SetTitle("");
	grExp->GetYaxis()->SetTitle("B(H #rightarrow inv.) - upper limit 95% CL");
	grExp->GetXaxis()->SetTitle("#it{#kappa}_{F}");

	grExp->SetLineWidth(2);
	grExp->SetLineColor(1);
	grExp->SetLineStyle(2);
	gr68->SetFillColor(kGreen);
	gr95->SetFillColor(kYellow);
	grObs->SetLineColor(1);
	grObs->SetLineWidth(2);

	// Make two hists with no line color 
	TH1F *histYellow = new TH1F("yellow","yellow",1,0,1);
	TH1F *histGreen = new TH1F("green","green",1,0,1);
	histGreen->SetLineWidth(0);
	histYellow->SetLineWidth(0);
	histGreen->SetLineColor(kGreen);
	histYellow->SetLineColor(kYellow);
	histGreen->SetFillColor(kGreen);
	histYellow->SetFillColor(kYellow);

	grExp->Draw("AL");
	gr95->Draw("E3same");
	gr68->Draw("E3same");
	grExp->Draw("Lsame");
	grObs->Draw("Lsame");
	grObs->SetMarkerSize(0.9);
	grObs->SetMarkerStyle(20);

	TLegend *leg = new TLegend(0.52,0.64,0.89,0.89);
	leg->SetFillColor(0);
	leg->AddEntry(grObs,"Observed","L");
	leg->AddEntry(grExp,"Median expected","L");
	leg->AddEntry(histGreen,"68% expected","F");
	leg->AddEntry(histYellow,"95% expected","F");
	leg->Draw();

	TLatex * tex = new TLatex();
	tex->SetNDC();
	tex->SetTextFont(42);
	tex->SetLineWidth(2);
	tex->SetTextSize(0.04);
	tex->DrawLatex(0.24,0.93,"4.9 fb^{-1} (7 TeV) + 19.7 fb^{-1} (8 TeV) + 2.3 fb^{-1} (13 TeV)");
  	tex->SetTextFont(42);
	tex->SetTextSize(0.054);
  	if (isPrelim) tex->DrawLatex(0.16, 0.82, "#bf{CMS} #it{Preliminary}");
  	else tex->DrawLatex(0.16, 0.82, "#bf{CMS}");
  	tex->DrawLatex(0.16, 0.76, "#it{#kappa}_{V} = 1");
	can->RedrawAxis();
	can->SaveAs("brlims_fixedCV1.pdf");
}

void drawBandy(){
	drawBandyKV();
	drawBandyKF();
}
