// plot 2D likelihood scan from file
// assume file already open as _file0
void scanLH2D(std::string outname="scanLH-cont.root",std::string x="RF", std::string y="RV"){
//TH2F scanLH2D(TTree *limit, std::string x="RF", std::string y="RV", double &xbf, double &ybf){

  _file0->cd();
  TGraph2D *g = new TGraph2D(); g->SetName("PFFF");
  TGraph2D *gD = new TGraph2D();
  gD->SetMarkerStyle(34);
  gD->SetMarkerSize(2.0);
  int n = limit->GetEntries();
  float rV,rF,deltaNLL,quant;

  limit->SetBranchAddress(y.c_str(),&rV);
  limit->SetBranchAddress(x.c_str(),&rF);
  limit->SetBranchAddress("deltaNLL",&deltaNLL);
  limit->SetBranchAddress("quantileExpected",&quant);
  
  int c=0;
  bool datanotfound = true;
  for (int i=0;i<n;i++){
   limit->GetEntry(i);
   if (quant==1 ) {
	if (!datanotfound) continue;
	//std::cout << rF << " "<<rV <<std::endl;
	gD->SetPoint(0,rF,rV,1);
	datanotfound=false;
   } else if (quant >-1){
	//std::cout << rV << " "<<rF <<std::endl;
        g->SetPoint(c,rF,rV,2*deltaNLL);c++;
   }

  }

  TH2F *h = (TH2F*) g->GetHistogram();
  //h->SetName("newName");
  //return *(h);
  TH2F *h68 = (TH2F*)h->Clone();
  h68->SetContourLevel(1,1-0.68);
  h68->SetLineColor(2); 
  h68->SetLineWidth(2);
  h->SetLineWidth(2);
 
  //h->Draw("CONT3");
  h->GetYaxis()->SetTitle(y.c_str());
  h->GetXaxis()->SetTitle(x.c_str());

  //h68->Draw("CONT3same");
  TFile *nf = new TFile(Form("%s",outname.c_str()),"RECREATE");
  nf->cd();
  h->Write("hall");
  h68->Write("h68");
  gD->Write("bestfit");

}
