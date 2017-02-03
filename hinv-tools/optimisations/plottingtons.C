void plottingtons(double dphijj,std::string filestring,std::string out){

   gROOT->SetBatch(1);  
   gStyle->SetOptStat(0);
   TFile *fi = TFile::Open(Form("%s",filestring.c_str()));
   TTree *limit = (TTree*)fi->Get("limit");
   limit->Draw("trackedParam_deta_jj:trackedParam_mjj>>h",Form("limit*(quantileExpected==0.5 && TMath::Abs(trackedParam_dphi_jj-%g) <0.01)",dphijj),"colz");
   TH2D *h2 = (TH2D*)gROOT->FindObject("h");

   h2->GetXaxis()->SetTitle("m_{jj} > X [GeV]");
   h2->GetYaxis()->SetTitle("#Delta#eta(j,j) > Y");
   h2->GetZaxis()->SetTitle("Expected upper limit on BR(H->inv) @ 95% CL");
   h2->GetZaxis()->SetTitleOffset(1.35);
   h2->SetTitle(Form("#Delta#phi(j,j) < %.2f",dphijj));
   
   TCanvas *can = new TCanvas("megh","",900,800);
   can->SetRightMargin(0.15);

   gStyle->SetPaintTextFormat(".2f");
   h2->Draw("colz4");
   
   can->Update();
   TPaletteAxis *palette = (TPaletteAxis*)h2->GetListOfFunctions()->FindObject("palette");
   palette->SetX1NDC(0.87);
   palette->SetX2NDC(0.9);
   palette->SetY1NDC(0.1);
   palette->SetY2NDC(0.9);
   can->Modified();
   can->Update();
   
   h2->Draw("textsame");
   can->SaveAs(Form("%s/optimisation_dphi_jj_lt_%g.png",out.c_str(),dphijj));
   can->SaveAs(Form("%s/optimisation_dphi_jj_lt_%g.pdf",out.c_str(),dphijj));

}
