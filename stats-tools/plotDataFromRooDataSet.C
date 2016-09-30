RooHist getDataMV(TH1F *sigh, TGraphAsymmErrors *rat){

	RooBinning bins(sigh->GetNbinsX(), ((sigh->GetXaxis())->GetXbins())->GetArray(), "databinning");
	// Input workspace 
	TFile *workspace = TFile::Open("comb_EXO-16-013.root");
	RooWorkspace *w = (RooWorkspace*)workspace->Get("w");

	RooRealVar *mv = (RooRealVar*)w->var("met_MV");
	mv->setBinning(bins,"databinning");

	RooPlot *fr1 = mv->frame();
	RooDataHist *dataF = (RooDataHist*)w->data("data_obs");
	RooDataHist *data = (RooDataHist*)dataF->reduce(RooFit::Cut("CMS_channel==CMS_channel::VH_had_hinv_13TeV_datacard_SR_monoV"));

	TH1* t = data->createHistogram("t",*mv); //makes the internal histogra	

        RooHist *hist = new RooHist(*t,0,1,RooAbsData::SumW2,1.,false);  // will do this by hand, RooFit SUUCKS!
	hist->SetName("data");

	// Properly normalise 
	for (int b=0;b<sigh->GetNbinsX();b++){
		double bw = sigh->GetBinWidth(b+1);

		double yv = hist->GetY()[b];

		// Taken from http://onbiostatistics.blogspot.ch/2014/03/computing-confidence-interval-for.html
		//double up = TMath::ChisquareQuantile(0.84,2*(cont+1))/2;
		//double dn = TMath::ChisquareQuantile(0.16,2*cont)/2;
		double up; 
		double dn;

		RooHistError::instance().getPoissonInterval(yv,dn,up,1);

		double errlow  = (yv-dn)/bw;
		double errhigh = (up-yv)/bw;

		hist->SetPoint(b,hist->GetX()[b],yv/bw);
		hist->SetPointError(b,bw/2,bw/2,errlow,errhigh);

		// Also make the ratio !!!!!!!
		double contE = sigh->GetBinContent(b+1);
		rat->SetPoint(b,hist->GetX()[b],yv/(bw*contE));
		rat->SetPointError(b,bw/2,bw/2,errlow/contE,errhigh/contE);
	}
	return *hist; 
}
RooHist getDataMJ(TH1F *sigh, TGraphAsymmErrors *rat){

	RooBinning bins(sigh->GetNbinsX(), ((sigh->GetXaxis())->GetXbins())->GetArray(), "databinning");
	// Input workspace 
	TFile *workspace = TFile::Open("comb_EXO-16-013.root");
	RooWorkspace *w = (RooWorkspace*)workspace->Get("w");

	RooRealVar *mv = (RooRealVar*)w->var("met_MJ");
	mv->setBinning(bins,"databinning");

	RooPlot *fr1 = mv->frame();
	RooDataHist *dataF = (RooDataHist*)w->data("data_obs");
	RooDataHist *data = (RooDataHist*)dataF->reduce(RooFit::Cut("CMS_channel==CMS_channel::ggH_hinv_13TeV_datacard_SR_monoJ"));

	TH1* t = data->createHistogram("t",*mv); //makes the internal histogra	

        RooHist *hist = new RooHist(*t,0,1,RooAbsData::SumW2,1.,false);  // will do this by hand, RooFit SUUCKS!
	hist->SetName("data");

	// Properly normalise 
	for (int b=0;b<sigh->GetNbinsX();b++){
		double bw = sigh->GetBinWidth(b+1);

		double yv = hist->GetY()[b];
		// Taken from http://onbiostatistics.blogspot.ch/2014/03/computing-confidence-interval-for.html
		//double up = TMath::ChisquareQuantile(0.84,2*(cont+1))/2;
		//double dn = TMath::ChisquareQuantile(0.16,2*cont)/2;
		double up; 
		double dn;

		RooHistError::instance().getPoissonInterval(yv,dn,up,1);

		double errlow  = (yv-dn)/bw;
		double errhigh = (up-yv)/bw;

		std::cout <<" Point " << b << " interval " << dn <<"-"<<up << "centre "<< yv << std::endl;
		std::cout <<" Point " << b << " interval " << dn <<"-"<<up << "centre "<< yv << std::endl;

		hist->SetPoint(b,hist->GetX()[b],yv/bw);
		hist->SetPointError(b,bw/2,bw/2,errlow,errhigh);

		// Also make the ratio !!!!!!!
		double contE = sigh->GetBinContent(b+1);
		rat->SetPoint(b,hist->GetX()[b],yv/(bw*contE));
		rat->SetPointError(b,bw/2,bw/2,errlow/contE,errhigh/contE);

	}
	return *hist; 
}

