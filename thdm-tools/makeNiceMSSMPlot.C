double MARKERSIZE=0.4;


sanity_check(){

	TFile *fi = TFile::Open("outplots-2hdm-neg-fine-mssm.root");
	//TFile *fi_exp = TFile::Open("outplots-2hdm-rotatey-exp.root");

	//TGraph *mssm = (TGraph*) fi->Get("mssm");

	TGraph2D *ku_gr = fi->Get("mssm_ku");	
	TGraph2D *kV_gr = fi->Get("mssm_kV");	
	TGraph2D *kd_gr = fi->Get("mssm_kd");	

	TH1F *hdum = new TH1F("hdum",";m_{A} (GeV);tan#beta",1,200,500);
	hdum->SetMinimum(1);
	hdum->SetMaximum(50);
	hdum->GetYaxis()->SetMoreLogLabels();
	hdum->GetXaxis()->SetMoreLogLabels();


	TCanvas *can = new TCanvas();
	hdum->Draw("axis");
	ku_gr->Draw("colzsame");
	ku_gr->GetYaxis()->SetMoreLogLabels();
	ku_gr->GetXaxis()->SetMoreLogLabels();
	ku_gr->GetXaxis()->SetTitle("m_{A}");
	ku_gr->GetYaxis()->SetTitle("tan#beta");
	ku_gr->SetTitle("#kappa_{u}");
	hdum->SetTitle("#kappa_{u}");
//	mssm->Draw("p");
	can->SetLogy();
	can->SetLogx();
	can->RedrawAxis();
	can->SaveAs("mssm_ku.pdf");

	TCanvas *can2 = new TCanvas();
	hdum->Draw("axis");
	kV_gr->Draw("colzsame");
	kV_gr->GetYaxis()->SetMoreLogLabels();
	kV_gr->GetXaxis()->SetMoreLogLabels();
	kV_gr->GetXaxis()->SetTitle("cos(#beta-#alpha)");
	kV_gr->GetYaxis()->SetTitle("tan#beta");
	hdum->SetTitle("#kappa_{V}");
//	mssm->Draw("p");
	can2->SetLogy();
	can2->SetLogx();
	can2->RedrawAxis();
	can2->SaveAs("mssm_kV.pdf");


	TCanvas *can2 = new TCanvas();
	hdum->Draw("axis");
	kd_gr->Draw("colzsame");
	kd_gr->GetYaxis()->SetMoreLogLabels();
	kd_gr->GetXaxis()->SetMoreLogLabels();
	kd_gr->GetXaxis()->SetTitle("cos(#beta-#alpha)");
	kd_gr->GetYaxis()->SetTitle("tan#beta");
	kd_gr->SetTitle("#kappa_{d}");
	hdum->SetTitle("#kappa_{d}");
//	mssm->Draw("p");
	can2->SetLogy();
	can2->SetLogx();
	can2->RedrawAxis();
	can2->SaveAs("mssm_kd.pdf");

		
}

void makeNiceMSSMPlot(){
//	gROOT->ProcessLine(".x paperStyle.C");
//		
	gStyle->SetOptStat(0);
	gStyle->SetPalette(1);

	sanity_check();
}

