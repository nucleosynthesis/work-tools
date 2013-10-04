// Quick Macro to make plots of the LH around the best fitted point

// run in CINT

// For LH Plots, n-sigma along x axis
int npoints = 15;
int nsigma  = 5;

RooAbsReal *nll;
RooWorkspace *w;
RooStats::ModelConfig *mc_s;

TGraph *graphLH(std::string nuisname, double err ){

	w->loadSnapshot("bestfitall"); // SetTo BestFit values as start

	// Get The parameter we want 
	RooRealVar *nuis =(RooRealVar*) w->var(nuisname.c_str());
	double bf = nuis->getVal();
	double nll_0=nll->getVal();


	TGraph *gr = new TGraph(2*npoints+1);
	for (int i=-1*npoints;i<=npoints;i++){
		nuis->setVal(bf+err*( ((float)i)*nsigma/npoints));
		double nll_v = nll->getVal();
		gr->SetPoint(i+npoints,nuis->getVal(),nll_v-nll_0);
	}

	gr->SetTitle("");
	gr->GetYaxis()->SetTitle("NLL - obs data");
	gr->GetYaxis()->SetTitleOffset(1.1);
	gr->GetXaxis()->SetTitleSize(0.05);
	gr->GetYaxis()->SetTitleSize(0.05);
	gr->GetXaxis()->SetTitle(nuisname.c_str());
	gr->SetLineColor(4);
	gr->SetLineWidth(2);
	gr->SetMarkerStyle(21);
	gr->SetMarkerSize(0.6);
	
	return gr;
	
}

void checkBestFitPoint(std::string workspace, std::string fitFile){
	
	// Open the ws file...
	TFile *fd_=0;
	TFile *fw_=0;

	gSystem->Load("$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so");
	gROOT->SetBatch(true);
	gStyle->SetOptFit(0);
	gStyle->SetOptStat(0);
	gStyle->SetPalette(1,0);

	fw_ =  TFile::Open(workspace.c_str());
	w   = (RooWorkspace*) fw_->Get("w");
	RooDataSet *data = (RooDataSet*) w->data("data_obs");
	mc_s = (RooStats::ModelConfig*)w->genobj("ModelConfig");
	std::cout << "make nll"<<std::endl;
	nll = mc_s->GetPdf()->createNLL(
		*data,RooFit::Constrain(*mc_s->GetNuisanceParameters())
		,RooFit::Extended(mc_s->GetPdf()->canBeExtended()));
	
	// Now get the best fit result
	fd_ =  TFile::Open(fitFile.c_str());
	RooFitResult *fit =(RooFitResult*)fd_->Get("fit_s");
	RooArgSet fitargs = fit->floatParsFinal();
	
	std::cout << "Got the best fit values" <<std::endl;		
	w->saveSnapshot("bestfitall",fitargs,true);
	
	// Now make the plots!	
	TCanvas *c = new TCanvas("c","",600,600);
	c->SaveAs(Form("minimum.pdf["));

	TIterator* iter(fitargs->createIterator());
        for (TObject *a = iter->Next(); a != 0; a = iter->Next()) {
                 RooRealVar *rrv = dynamic_cast<RooRealVar *>(a);      
                 std::string name = rrv->GetName();
		 TGraph *gr = graphLH(name,rrv->getError());
		 gr->Draw("ALP");
		 c->SaveAs(Form("minimum.pdf["));
	}
	c->SaveAs(Form("minimum.pdf]"));
}
