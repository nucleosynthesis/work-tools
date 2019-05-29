void makeCorrNVTXplots(std::string input){

	TFile *fi = TFile::Open(input.c_str());
	TTree *tree = (TTree*)fi->Get("entries");

	int nttdefs[5] = {4,10,15,28,41};
	
	for (int i=0;i<5;i++){

		tree->Draw(Form("nvtx:ntt%d>>h(500,0,500,50,0,50)",nttdefs[i]));
		TH2F * h2 = (TH2F*)gROOT->FindObject("h");
		h2->GetXaxis()->SetTitle("N TT");
		h2->GetYaxis()->SetTitle("N VTX");

		double corr = h2->GetCorrelationFactor();
		TH1F *prj = (TH1F*)h2->ProfileX();
		prj->SetLineColor(2);
		prj->SetMarkerColor(2);
		TCanvas *can = new TCanvas(Form("can%d",i),"",660,600);
		can->SetRightMargin(0.12);
		h2->Draw("colz");
		prj->Draw("same");
		h2->SetTitle("");
		gStyle->SetOptStat(0);
		can->SetLogz();

     		TLatex *latex = new TLatex(); latex->SetTextFont(42);
     		latex->SetNDC();
     		latex->DrawLatex(0.12,0.92,Form("#bf{CMS} #it{Preliminary}, NTT in |ieta|#leq %d",nttdefs[i]));
     		latex->DrawLatex(0.125,0.82,Form("Correlation = %.3f",corr));
    		can->SaveAs(Form("Correlation_ntt%d.png",nttdefs[i]));
    		can->SaveAs(Form("Correlation_ntt%d.pdf",nttdefs[i]));
	}

}
