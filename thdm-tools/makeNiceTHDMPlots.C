double MARKERSIZE=0.4;

void Type1(){

	//TFile *fi = TFile::Open("outplots-2hdm-rotatey.root");
	TFile *fi = TFile::Open("outplots-2hdm-1Dfindcrossing.root");
	TFile *fi_exp = TFile::Open("outplots-2hdm-rotatey-exp.root");

	TCanvas *can = new TCanvas(); 
	TH1F *h_dummy = new TH1F("dummy",";cos(#beta-#alpha); tan(#beta)",1,-0.9,0.9);

	h_dummy->SetMaximum(10);
	h_dummy->SetMinimum(0.1);
	h_dummy->GetYaxis()->SetNdivisions(210);
	h_dummy->GetYaxis()->SetMoreLogLabels();
	h_dummy->Draw("axis");
	TGraph *type1 = (TGraph*)fi->Get("type1");
	type1->SetLineColor(1); 
	//type1->SetLineWidth(2203);
	type1->SetLineColor(kYellow);
	//type1->SetLineStyle(3);
	type1->Draw("pL");

	/*
	TGraph2D *grtype1_col = (TGraph2D*)fi->Get("type1_minscan");
	TH2F * type1_col= (TH2F*) grtype1_col->GetHistogram();
	type1_col->SetContour(2);
	type1_col->SetContourLevel(1,5.99);
	type1_col->SetFillColor(kPink); 
	type1_col->Draw("cont3");
	*/
	//type1->Draw("f");

	TGraph *type1_e = (TGraph*)fi_exp->Get("type1");
	type1_e->SetLineColor(4); type1_e->SetLineWidth(3);
	type1_e->SetMarkerColor(4);

	type1_e->Draw("p");

	type1->SetMarkerSize(MARKERSIZE);
	type1_e->SetMarkerSize(MARKERSIZE);

	TLatex *   texCMS = new TLatex(0.2,0.84,"#bf{CMS} #it{Preliminary}");
	TLegend *WHITEBOX = new TLegend(0.18,0.82,0.44,0.88);
	WHITEBOX->SetFillColor(kWhite);
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
	tex->DrawLatex(0.42,0.94,"19.7 fb^{-1} (8 TeV) + 5.1 fb^{-1} (7 TeV)");
	tex->DrawLatex(0.15,0.94,"2HDM - Type I");

	TLegend *leg = new TLegend(0.18,0.2,0.5,0.3);
	leg->SetFillColor(10); leg->SetTextFont(42);
	leg->AddEntry(type1,"Observed 95% CL","L");
	leg->AddEntry(type1_e,"Expected 95% CL","L");
	//leg->AddEntry(type1,"Observed 95% CL","L");
	//
	leg->Draw(); 

	can->SetLogy();
	can->RedrawAxis();
	can->SaveAs("type_1.pdf");


}
void Type2(){

	TFile *fi = TFile::Open("outplots-2hdm-rotatey.root");
	TFile *fi_exp = TFile::Open("outplots-2hdm-rotatey-exp.root");
	//TFile *fi_exp = TFile::Open("outplots-2hdm-rotatey.root");

	TCanvas *can = new TCanvas(); 
	TH1F *h_dummy = new TH1F("dummy",";cos(#beta-#alpha); tan(#beta)",1,-0.8,0.8);

	h_dummy->SetMaximum(10);
	h_dummy->SetMinimum(0.048);
	h_dummy->GetYaxis()->SetNdivisions(210);
	h_dummy->GetYaxis()->SetMoreLogLabels();
	h_dummy->Draw("axis");
	TGraph *type2 = (TGraph*)fi->Get("type2");
	type2->SetLineColor(1); type2->SetLineWidth(3);

	type2->Draw("p");

	TGraph *type2_e = (TGraph*)fi_exp->Get("type2");
	type2_e->SetLineColor(4); type2_e->SetLineWidth(3);
	type2_e->SetMarkerColor(4);
	type2_e->Draw("p");


	type2->SetMarkerSize(MARKERSIZE);
	type2_e->SetMarkerSize(MARKERSIZE);


	TLatex *   texCMS = new TLatex(0.2,0.84,"#bf{CMS} #it{Preliminary}");
	TLegend *WHITEBOX = new TLegend(0.18,0.82,0.44,0.88);
	WHITEBOX->SetFillColor(kWhite);
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
	tex->DrawLatex(0.42,0.94,"19.7 fb^{-1} (8 TeV) + 5.1 fb^{-1} (7 TeV)");
	tex->DrawLatex(0.15,0.94,"2HDM - Type II");

	TLegend *leg = new TLegend(0.58,0.2,0.9,0.3);
	leg->SetFillColor(10); leg->SetTextFont(42);
	leg->AddEntry(type2,"Observed 95% CL","L");
	leg->AddEntry(type2_e,"Expected 95% CL","L");
	//leg->AddEntry(type1,"Observed 95% CL","L");
	//
	leg->Draw(); 

	can->SetLogy();
	can->RedrawAxis();
	can->SaveAs("type_2.pdf");


}

Type1_sanity_check(){

	TFile *fi = TFile::Open("outplots-2hdm-rotatey.root");
	//TFile *fi_exp = TFile::Open("outplots-2hdm-rotatey-exp.root");

	TGraph *type1 = (TGraph*) fi->Get("type1");

	TGraph2D *ku_gr = fi->Get("t1_ku");	
	TGraph2D *kV_gr = fi->Get("t1_kV");	


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

Type2_sanity_check(){

	TFile *fi = TFile::Open("outplots-2hdm-rotatey.root");
	//TFile *fi_exp = TFile::Open("outplots-2hdm-rotatey-exp.root");

	TGraph *type2 = (TGraph*) fi->Get("type2");

	TGraph2D *ku_gr = fi->Get("t2_ku");	
	TGraph2D *kV_gr = fi->Get("t2_kV");	
	TGraph2D *kd_gr = fi->Get("t2_kd");	


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


	TCanvas *can2 = new TCanvas();
	kd_gr->SetMaximum(2.5);
	kd_gr->SetMinimum(-2.5);
	kd_gr->Draw("colz");
	kd_gr->GetXaxis()->SetTitle("cos(#beta-#alpha)");
	kd_gr->GetYaxis()->SetTitle("tan#beta");
	kd_gr->SetTitle("#kappa_{d}");
	type2->Draw("p");
	can2->SetLogy();
	can2->RedrawAxis();
	can2->SaveAs("type2_kd.pdf");

		
}

void makeNiceTHDMPlots(){
	gROOT->ProcessLine(".x paperStyle.C");
	gStyle->SetPalette(1);

	Type1();
//	Type2();
	
//	Type1_sanity_check();
//	Type2_sanity_check();
}

