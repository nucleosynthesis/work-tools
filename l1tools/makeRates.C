TH1F *target;
TH1F *source;

TRandom3 *rnd;
bool reWeight=false;

bool fitEffs = false; 

double weight(int nvtx){
  if (!reWeight) return 1.;
  if (nvtx>80 ) return 0;
  if (source->GetBinContent(nvtx) == 0 ) return 1.;
  return target->GetBinContent(nvtx)/source->GetBinContent(nvtx);
}

TGraphErrors *makeGraph(TH1F* histo, int nZB){

	double avrgInstLumi = 4.5e33; 
	double sigmaPP = 6.9e-26;
	double norm = (11.246*2736.)/nZB; // zb rate = n_colliding * 11 kHz 

	TGraphErrors *gr = new TGraphErrors();
	int pt=0; 
	int nb=histo->GetNbinsX();
	gr->SetName(Form("graph_%s",histo->GetName()));
	for (int b=1;b<=nb;b++){
		double err;
		double integral = histo->IntegralAndError(b,nb,err);
		double x = histo->GetBinLowEdge(b);
		gr->SetPoint(pt,x,integral*norm);
		gr->SetPointError(pt,0,err*norm);
		std::cout << gr->GetName() << ", pt " << pt <<  ", x " << x << ", rate " << integral << std::endl;
		pt++;
	}
	return gr;
}

void makeRates(std::string infile){

	std::string MET       = "hfmet3x3";
	std::string METPUS    = "hfmet3x3pus";	// this is recalculated + PUS
	std::string METPUS3x3 = "hfmet3x3pus0";	// this is recalculated + Regional PUS

	std::string recomet = "recomet";

	std::string labels[3] = {"MET","MET + PUS","MET + PUS (0)"};
	//std::string title ="PF E_{T}^{miss} Type-1 Corrected (GeV)";
	std::string title ="L1 E_{T}^{miss} (GeV)";

	rnd = new TRandom3();
 	gStyle->SetOptFit(0);
 	gStyle->SetOptStat(0);

	std::string drawOpts = "pl";
	if (fitEffs) drawOpts =  "p";

	TFile *fin = TFile::Open(infile.c_str());
	TTree *tree = (TTree*)fin->Get("entries");


	double minMET = 0; 
	double maxMET = 300;
	int nxbins = 30;
	int nvtxbins[4] = {0,10,20,1000};

	// Keep Threshold = 60; 
	// We will also make a canvas for a certain threshold with different nvtx 
        int keepThreshold=20;	

	int nZB = tree->GetEntries();

	for (int vtxi=-1;vtxi<0;vtxi+=1){


	  TH1F *numerator = new TH1F(Form("num_%d",vtxi),"num",nxbins,minMET,maxMET);
	  numerator->Sumw2();
	  if (vtxi<0) tree->Draw(Form("%s>>num_%d",MET.c_str(),vtxi),"weight(nvtx)");
	  else tree->Draw(Form("%s>>num_%d",MET.c_str(),vtxi),Form("nvtx>=%d && nvtx<%d",nvtxbins[vtxi],nvtxbins[vtxi+1]));

	  TH1F *numeratorpus = new TH1F(Form("num_p_%d",vtxi),"num",nxbins,minMET,maxMET);
	  numeratorpus->Sumw2();
	  if (vtxi<0) tree->Draw(Form("%s>>num_p_%d",METPUS.c_str(),vtxi),"weight(nvtx)");
	  else tree->Draw(Form("%s>>num_p_%d",METPUS.c_str(),vtxi),Form("nvtx>=%d && nvtx<%d",nvtxbins[vtxi],nvtxbins[vtxi+1]));

	  TH1F *numeratorpus3x3 = new TH1F(Form("num_p3x3_%d",vtxi),"num",nxbins,minMET,maxMET);
	  numeratorpus3x3->Sumw2();
	  if (vtxi<0) tree->Draw(Form("%s>>num_p3x3_%d",METPUS3x3.c_str(),vtxi),"weight(nvtx)");
	  else tree->Draw(Form("%s>>num_p3x3_%d",METPUS3x3.c_str(),vtxi),Form("nvtx>=%d && nvtx<%d",nvtxbins[vtxi],nvtxbins[vtxi+1]));

	  TLegend *legx = new TLegend(0.6,0.2,0.89,0.4); 
 	  TCanvas *canx = new TCanvas();

	  TGraphErrors *effs 	    = (TGraphErrors*) makeGraph(numerator,nZB);
	  TGraphErrors *effs_pus    = (TGraphErrors*) makeGraph(numeratorpus,nZB);
	  TGraphErrors *effs_pus3x3 = (TGraphErrors*) makeGraph(numeratorpus3x3,nZB);
	
	  TLatex *latex = new TLatex(); latex->SetTextFont(42);
	  latex->SetNDC();
	  if (vtxi<0) latex->DrawLatex(0.12,0.92,"#bf{CMS} #it{Simulation}");
	  else latex->DrawLatex(0.12,0.92,Form("#bf{CMS} #it{Simulation},  %d #leq Num VTX < %d",nvtxbins[vtxi],nvtxbins[vtxi+1]));
 	  canx->SaveAs(Form("rates_%s_allthresh_vtx%d.png",infile.c_str(),vtxi));
 	  canx->SaveAs(Form("rates_%s_allthresh_vtx%d.pdf",infile.c_str(),vtxi));

	 
	  // For a given #nvtx selection, we can make a nice plot of MET, METPUS, METPUS3x3
	
	 TLegend *legp = new TLegend(0.5,0.1,0.89,0.55); 
	 legp->SetTextFont(42);
	 legp->SetFillColor(0);legp->SetBorderSize(0);legp->SetNColumns(3);
 	 TCanvas *canp = new TCanvas();

	 int color = 1; 
	 if (color >= 5 ) color++;
	 if (color >= 10 ) color++;

	 effs->SetLineColor(color);
	 effs->SetMarkerColor(color);
	 effs->SetMarkerStyle(20);
 	 effs->GetXaxis()->SetTitle(title.c_str());
 	 effs->GetYaxis()->SetTitle("Rate");
// 	 effs->GetYaxis()->SetRangeUser(0,1.2);

	 effs_pus->SetLineColor(color);
	 effs_pus->SetLineStyle(2);
	 effs_pus->SetMarkerColor(color);
	 effs_pus->SetMarkerStyle(21);

	 effs_pus3x3->SetLineColor(color);
	 effs_pus3x3->SetLineStyle(3);
	 effs_pus3x3->SetMarkerColor(color);
	 effs_pus3x3->SetMarkerStyle(25);

	effs->Draw("ALP");
	effs->Draw(Form("a%s",drawOpts.c_str()));
	effs_pus->Draw(Form("%s",drawOpts.c_str()));
	effs_pus3x3->Draw(Form("%s",drawOpts.c_str()));
	legp->AddEntry(effs,	   Form("%s",labels[0].c_str()),"LP");
	legp->AddEntry(effs_pus,   Form("%s",labels[1].c_str()),"LP");
	legp->AddEntry(effs_pus3x3,Form("%s",labels[2].c_str()),"LP");

	legp->Draw();
	TLatex *latexf = new TLatex(); latexf->SetTextFont(42);
	latexf->SetNDC();
	if (vtxi<0) latexf->DrawLatex(0.12,0.92,"#bf{CMS} #it{Simulation}");
	else latexf->DrawLatex(0.12,0.92,Form("#bf{CMS} #it{Simulation},  %d #leq Num VTX < %d",nvtxbins[vtxi],nvtxbins[vtxi+1]));
 	canp->SaveAs(Form("rates_%s_comparePUS_allthresh_vtx%d.png",infile.c_str(),vtxi));
 	canp->SaveAs(Form("rates_%s_comparePUS_allthresh_vtx%d.pdf",infile.c_str(),vtxi));
     }

}
