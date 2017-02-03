bool isPrelim=false;

void decorate(TCanvas *can, bool isPublished){

	TLatex * tex = new TLatex();
	tex->SetNDC();
	tex->SetTextFont(42);
	tex->SetLineWidth(2);
	tex->SetTextSize(0.035);
	tex->DrawLatex(0.16,0.93,"4.9 fb^{-1} (7 TeV) + 19.7 fb^{-1} (8 TeV) + 2.3 fb^{-1} (13 TeV)");
  	tex->SetTextFont(42);
	tex->SetTextSize(0.06);
	if (!isPublished){
		
		TLegend *WHITEBOX = new TLegend(0.17,0.78,0.55,0.84);
		WHITEBOX->SetFillColor(kWhite);
		//WHITEBOX->Draw();
		TLegend *WHITEBOX2 = new TLegend(0.17,0.815,0.3,0.89);
		WHITEBOX2->SetFillColor(kWhite);
		WHITEBOX2->Draw();
  		//tex->DrawLatex(0.18, 0.83, "#splitline{#bf{CMS}}{#it{Supplementary}}");
  		if (isPrelim) tex->DrawLatex(0.18, 0.83, "#splitline{#bf{CMS}}{#it{Preliminary}}");
  		else tex->DrawLatex(0.18, 0.83, "#bf{CMS}");

	} else {

  		if (isPrelim) {  
			TLegend *WHITEBOX = new TLegend(0.17,0.78,0.6,0.84);
			WHITEBOX->SetFillColor(kWhite);
			WHITEBOX->Draw();
			tex->DrawLatex(0.18, 0.83, "#splitline{#bf{CMS}}{#it{Preliminary}}");
		}
		else tex->DrawLatex(0.18, 0.83, "#bf{CMS}");

	}
       can->SetTicky(1);
       can->SetTickx(1);
}

void makeNice1378ScanPlot(TH1F *hd){
	TFile *fi = TFile::Open("13_78TeV/brlhscan_78_13_neg-tree.root");


	TGraph *grCO =(TGraph*)fi->Get("_all-sys-neg");
	TGraph *grCE =(TGraph*)fi->Get("_all-sys-expected-neg");
	grCO->SetLineWidth(3);
	grCE->SetLineWidth(3);
	TGraph *gr13O =(TGraph*)fi->Get("13-neg");
	TGraph *gr13E =(TGraph*)fi->Get("13-expected-neg");
	TGraph *gr87O =(TGraph*)fi->Get("78-neg");
	TGraph *gr87E =(TGraph*)fi->Get("78-expected-neg");


       TCanvas *can = new TCanvas();
       hd->Draw("axis");
       grCO->Draw("lsame");
       grCE->Draw("lsame");
	gr13O->Draw("lsame");
        gr13E->Draw("lsame"); 
        gr87O->Draw("lsame"); 
        gr87E->Draw("lsame");

	TLegend *leg1 = new TLegend(0.66,0.16,0.90,0.3);
	leg1->SetTextSize(0.04);
	leg1->AddEntry(grCO  ,"Combined","L");
	leg1->AddEntry(gr13O ,"13 TeV","L");
	leg1->AddEntry(gr87O ,"7+8 TeV","L");
	leg1->Draw();

	TLegend *leg2 = new TLegend(0.46,0.16,0.625,0.25);
	leg2->SetTextSize(0.04);
	leg2->AddEntry(grCO,"Observed","L");
	leg2->AddEntry(grCE,"Expected","L");
	leg2->Draw();

       decorate(can,false);
       can->SaveAs("brlhscan_year_paper_neg.pdf");


}

void makeNiceBRScanPlot(TH1F *hd){
	// Input is just the tree from the other plotter 
	TFile *fi = TFile::Open("ChanSplit/brlhscan_tagged_neg-tree.root");
	
	
	TGraph *grCO =(TGraph*)fi->Get("_all-sys-neg");
	TGraph *grCE =(TGraph*)fi->Get("_all-sys-expected-neg");
	grCO->SetLineWidth(3);
	grCE->SetLineWidth(3);
	TGraph *grVBFO = (TGraph*)fi->Get("qqH-neg");
       TGraph *grVBFE = (TGraph*)fi->Get("qqH-expected-neg");
       TGraph *grVHO = (TGraph*)fi->Get("VH-neg");
       TGraph *grVHE = (TGraph*)fi->Get("VH-expected-neg");
       TGraph *grGGHO = (TGraph*)fi->Get("ggH-neg");
       TGraph *grGGHE = (TGraph*)fi->Get("ggH-expected-neg");



	fi->ls(); 

	std::cout << " Got the graphs" << std::endl;
	grVHO->SetLineColor(kGreen+1);
	grVHE->SetLineColor(kGreen+1);
	std::cout << " Got the graphs" << std::endl;

       TCanvas *can = new TCanvas();
       hd->Draw("axis");
       grCO->Draw("lsame");
       grCE->Draw("lsame");
	grVBFO->Draw("lsame");
	grVBFE->Draw("lsame");
        grVHO->Draw("lsame"); 
        grVHE->Draw("lsame"); 
        grGGHO->Draw("lsame");
       grGGHE->Draw("lsame");
	std::cout << " Got the graphs" << std::endl;

	TLegend *leg1 = new TLegend(0.65,0.16,0.87,0.35);
	leg1->SetTextSize(0.04);
	leg1->AddEntry(grCO  ,"Combined","L");
	leg1->AddEntry(grVBFO,"qqH-tagged","L");
	leg1->AddEntry(grVHO ,"VH-tagged","L");
	leg1->AddEntry(grGGHO,"ggH-tagged","L");
	leg1->Draw();

	TLegend *leg2 = new TLegend(0.46,0.16,0.625,0.25);
	leg2->SetTextSize(0.04);
	leg2->AddEntry(grCO,"Observed","L");
	leg2->AddEntry(grCE,"Expected","L");
	leg2->Draw();

       decorate(can,false);
       can->SetTicky();
       can->SetTickx();
       can->SaveAs("brlhscan_channel_paper_neg.pdf");
}

void plotItAllNeg(){
 	gStyle->SetOptStat(0);
	gROOT->SetBatch(1);
	gStyle->SetCanvasDefH(600); //Height of canvas
	gStyle->SetCanvasDefW(600); //Width of canvas
	gStyle->SetCanvasDefX(0);   //POsition on screen
	gStyle->SetCanvasDefY(0);

	gStyle->SetPadLeftMargin(0.13);//0.16);
	gStyle->SetPadRightMargin(0.08);//0.02);
	gStyle->SetPadTopMargin(0.085);//0.02);
	gStyle->SetPadBottomMargin(0.12);//0.02);

	  // For g axis titles:
	gStyle->SetTitleColor(1, "XYZ");
	gStyle->SetTitleFont(42, "XYZ");
	gStyle->SetTitleSize(0.045, "Z");
	gStyle->SetTitleSize(0.055, "XY");
	gStyle->SetLabelSize(0.05, "XY");
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
	
	

	TH1F *hd = new TH1F("h","",1,-.6,1.8);
	hd->SetMaximum(10);
	hd->SetMinimum(0);
	hd->GetXaxis()->SetTitle("B(H #rightarrow inv.)");
	hd->GetYaxis()->SetTitle("q");

        makeNiceBRScanPlot(hd);
        makeNice1378ScanPlot(hd);

}
