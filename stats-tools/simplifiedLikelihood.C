//Simple script to fit a signal with background + systematics and data, 
// The input is from a combine workspace + multiDimFit (masking appropriately the signal regions). 
// The signal is assumed to be from the "mlfit.root" output (prefit) of the combine MaxLikelihoodFit, but some simple re-writes could accept any histogram 

// ranges for LH scans
double RMIN = 0;
double RMAX = 1.;
int nPoints = 20;


const bool isTH1Input=false;
const std::string channel = "datacard_SR_monoJ";
bool justCalcLimit = true;
bool doExpected = false;

double GetCLs(RooAbsReal *nllD_, RooAbsReal *nllA_, RooRealVar *r, double rVal){
    r->setConstant(false);  

    RooMinimizer mCA(*nllA_);
    mCA.minimize("Minuit2","minimize"); 
    double minNllA_ = nllA_->getVal();
    double rBestA_ = r->getVal();

    RooMinimizer mCD(*nllD_);
    mCD.minimize("Minuit2","minimize");
    double minNllD_ = nllD_->getVal();
    double rBestD_ = r->getVal();

    // Conditional fit
    r->setConstant(true);  r->setVal(rVal);

    RooMinimizer mUA(*nllA_);
    mUA.minimize("Minuit2","minimize");
    double nllFixA = nllA_->getVal();

    RooMinimizer mUD(*nllD_);
    mUD.minimize("Minuit2","minimize");
    double nllFixD = nllD_->getVal();

    double qmu = 2*(nllFixD - minNllD_); if (qmu < 0) qmu = 0;
    if (rVal < rBestD_) qmu=0;
    if (rBestD_<0 ) {
	// could have set minimum of r to 0, but to help fit along, we fix r to 0 and evaluate 
	r->setVal(0);
	mUD.minimize("Minuit2","minimize");
	double nllFix0Signal_ = nllD_->getVal();
	qmu =  2*(nllFixD - nllFix0Signal_); if (qmu < 0) qmu = 0;
    }

    double qA  = 2*(nllFixA - minNllA_); if (qA < 0) qA = 0; // shouldn't this always be 0?

    double CLsb = ROOT::Math::normal_cdf_c(TMath::Sqrt(qmu));
    double CLb  = ROOT::Math::normal_cdf(TMath::Sqrt(qA)-TMath::Sqrt(qmu));

    if (qmu > qA) {
	// In this region, things are tricky
	double mos = TMath::Sqrt(qA); // mu/sigma
	CLsb = ROOT::Math::normal_cdf_c( (qmu + qA)/(2*mos) );
	CLb  = ROOT::Math::normal_cdf_c( (qmu - qA)/(2*mos) );
    }

    r->setConstant(false);

    double CLs  = (CLb == 0 ? 0 : CLsb/CLb);
    // std::cout << "CLsplusb = " << CLsb << ", CLb " << CLb << ", CLs " << CLs << std::endl;
    // std::cout << "rMIN (data), qmu = " << rBestD_ << ", " << qmu <<std::endl; 
    return CLs;

}
double GetExpectedCLs(RooAbsReal *nllA_, RooRealVar *r, double rVal){
    r->setConstant(false);  

    RooMinimizer mCA(*nllA_);
    mCA.minimize("Minuit2","minimize"); 
    double minNllA_ = nllA_->getVal();
    rBestA_ = r->getVal();

    // Conditional fit
    r->setConstant(true);  r->setVal(rVal);

    RooMinimizer mUA(*nllA_);
    mUA.minimize("Minuit2","minimize");
    double nllFixA = nllA_->getVal();
    double qA  = 2*(nllFixA - minNllA_); if (qA < 0) qA = 0; // shouldn't this always be 0?

    double N = ROOT::Math::normal_quantile(0.5, 1.0);
    double clb = 0.5;
    double clsplusb = ROOT::Math::normal_cdf_c( TMath::Sqrt(qA) - N, 1.);
    std::cout << "CLsplusb = " << clsplusb << ", CLb " << clb << ", CLs " << clsplusb/clb << std::endl;
    std::cout << "rMIN (asimov), qA = " << rBestA_ << ", " << qA << std::endl; 
    return (clb != 0 ? clsplusb/clb : 0); 
}
double getUpperLimit(RooAbsReal *nllD_, RooAbsReal *nllA_, RooRealVar *r, double cl,bool runExpected,double rMin,double rMax,double steps){

    TGraph *CLSgraph = new TGraph(); int pt=0;
    double  cls_min=999;
    double  cls_max=-999;
    double clsV;
    if (runExpected) clsV = GetExpectedCLs(nllA_,r,rMin);
    else clsV = GetCLs(nllD_,nllA_,r,rMin);

    for (double rV = rMin;rV<=rMax;rV+=steps){
	if (runExpected) clsV = GetExpectedCLs(nllA_,r,rV);
	else clsV = GetCLs(nllD_,nllA_,r,rV);
	CLSgraph->SetPoint(pt,clsV,rV);
	pt++;
	if (clsV<cls_min )cls_min = clsV;
	if (clsV>cls_max )cls_max = clsV;
    }
    //  for (int pt=0;pt<CLSgraph->GetN();pt++){
    //	std::cout << " At r="<<CLSgraph->GetY()[pt] << ",  CLs="<<CLSgraph->GetX()[pt]<<std::endl;
    //  }

    if (cls_min>1-cl) return   rMax ;
    if (cls_max<1-cl) return   rMin ;

    return CLSgraph->Eval(1-cl);
}

TH1F getData(RooWorkspace *w, TH1F *sigh){


    RooBinning bins(sigh->GetNbinsX(), ((sigh->GetXaxis())->GetXbins())->GetArray(), "databinning");
    std::cout << " Ok So far " << std::endl;
    RooRealVar *mv = (RooRealVar*)w->var("met_MJ");
    std::cout << " Ok So far " << std::endl;
    mv->setBinning(bins,"databinning");

    RooPlot *fr1 = mv->frame();
    RooDataHist *dataF = (RooDataHist*)w->data("data_obs");
    RooDataHist *data = (RooDataHist*)dataF->reduce(RooFit::Cut(Form("CMS_channel==CMS_channel::%s",channel.c_str())));

    TH1F* t = (TH1F*) data->createHistogram("t",*mv); //makes the internal histogra	
    /*
       std::cout << " Ok So far " << std::endl;

       RooHist *hist = new RooHist(*t,0,1,RooAbsData::SumW2,1.,false);  // will do this by hand, RooFit SUUCKS!
       hist->SetName("data");

    // Properly normalise 
    for (int b=0;b<sigh->GetNbinsX();b++){
    double bw = sigh->GetBinWidth(b+1);
    double yv = hist->GetY()[b];
    std::cout << " Bin content =  " << yv << std::endl;
    }
    */
    return *t; 
}

double simplifiedLikelihood(std::string modelName="shapes_prefit/total_signal",std::string outname="ht400Output",std::string ifilename="CovarianceInput.root",std::string sfilename="SignalInput.root", bool runExpected = false,  bool ignoreCorrelation = false,std::string whichFit = "fit_b"){

    gROOT->SetBatch(1);
    gStyle->SetOptStat(0);
    doExpected = runExpected;
    TFile *ifile = TFile::Open(ifilename.c_str());
    TFile *sfile = TFile::Open(sfilename.c_str());
    if (ignoreCorrelation) outname += "NoCorrelation";
    if (doExpected) outname += "Expected";
    std::string outnameRDeltaNLL = outname+ "DeltaNLL";
    outname += ".root";
    outnameRDeltaNLL += ".root";

    std::string shapes_file = "mlfit.root";
    std::string data_file = "monoJet.root";
    // TFile *dfile = TFile::Open(data_file.c_str());
    // TFile *sfile = TFile::Open(shapes_file.c_str());
    // TFile *signalfile = TFile::Open(signalfilename.c_str());
    // std::cout << "Open files  " << signalfilename << std::endl; 

    // TH1F *bkg      = (TH1F*)sfile->Get(Form("shapes_fit_b/%s/total",channel.c_str()));
    // TH1F *bkgpf    = (TH1F*)sfile->Get(Form("shapes_prefit/%s/total_background",channel.c_str()));
    // TH1F *bkgcombfit    = (TH1F*)signalfile->Get(Form("shapes_fit_b/%s/total_background",channel.c_str()));
    // TH1F *signal = (TH1F*)signalfile->Get(Form("shapes_prefit/%s/total_signal",channel.c_str()));		// TH1 for signal  
    // TH1F data(getData((RooWorkspace*)dfile->Get("w"),signal));			// TH1 for data :( 
    // TH2F *covar  = (TH2F*)sfile->Get(Form("shapes_fit_b/%s/total_covar",channel.c_str()));
    // TH1F *bkgcombfit   = (TH1F*)ifile->Get("ewk")->Clone("total_background");
    // TH1F *bkg   = (TH1F*)ifile->Get("ewk");
    // TH2F *covar = (TH2F*)ifile->Get(Form("covariance"));
    // TH1F data  = *(TH1F*)ifile->Get("data");
    TH1F *signal= (TH1F*)sfile->Get(modelName.c_str());		// TH1 for signal 
     // TH1F *signal = (TH1F*)sfile->Get("shapes_prefit/total_signal");		// TH1 for signal  
    TH1F *bkg      = (TH1F*)ifile->Get(Form("shapes_%s/total_background",whichFit.c_str()));
    TH1F *bkgcombfit    = (TH1F*)ifile->Get(Form("shapes_%s/total_background",whichFit.c_str()));
    TH1F * data = (TH1F*)ifile->Get(Form("shapes_%s/total_data",whichFit.c_str()));
    TH2F *covar  = (TH2F*)ifile->Get(Form("shapes_%s/total_covar",whichFit.c_str()));
    covar->Print();
    signal->Print();
    bkg->Print();
    data->Print();

    TH2F *corr = (TH2F*)covar->Clone();  corr->SetName("correlation");

    // bkg and covariance defined as pdf / GeV, so scale by bin widhts 
    int nbins = data->GetNbinsX();
    //nbins = 3;
    if (!isTH1Input){
	for (int b=1;b<=nbins;b++){
	    double bw = bkg->GetBinWidth(b);
	    bkg->SetBinContent(b,bkg->GetBinContent(b)*bw);
	    bkgcombfit->SetBinContent(b,bkgcombfit->GetBinContent(b)*bw);
	    signal->SetBinContent(b,signal->GetBinContent(b)*bw);
	    for (int j=1;j<=nbins;j++){
		double bj = bkg->GetBinWidth(j);
		covar->SetBinContent(b,j,covar->GetBinContent(b,j)*bw*bj);
		if (ignoreCorrelation && b!=j) covar->SetBinContent(b,j,0); 
	    }
	}
    }
    //if ( signal->Integral() > 0.6*data.Integral()) return 0.;

    for (int b=1;b<=nbins;b++){
	for (int j=1;j<=nbins;j++){
	    double sigb = TMath::Sqrt(covar->GetBinContent(b,b));
	    double sigj = TMath::Sqrt(covar->GetBinContent(j,j));
	    corr->SetBinContent(b,j,covar->GetBinContent(b,j)/(sigb*sigj));
	}
    }

    RooArgList xlist_;
    RooArgList olist_;
    RooArgList mu_,muA_;

    bkg->Print() ;
    covar->Print() ; 
    signal->Print() ;
    data->Print() ;  

    // Make a dataset (simultaneous)
    RooCategory sampleType("bin_number","Bin Number");
    RooRealVar  observation("observed","Observed Events bin",1);

    // You have to define the samples types first!, because RooFit suuuuucks!
    for (int b=1;b<=nbins;b++){
	sampleType.defineType(Form("%d",b-1),b-1);
	sampleType.setIndex(b-1);
    }

    RooArgSet   obsargset(observation,sampleType);
    RooDataSet obsdata("combinedData","Data in all Bins",obsargset);
    //obsdata.add(RooArgSet(observation,sampleType));

    for (int b=1;b<=nbins;b++){
	sampleType.setIndex(b-1);
	std::cout << sampleType.getLabel() << ", " << sampleType.getIndex() << std::endl;
	//RooArgSet localset(observation,sampleType);
	//obsdata.add(localset);
	observation.setVal(data->GetBinContent(b));
	obsdata.add(RooArgSet(observation,sampleType));
	std::cout << " Observed at " << b << ", " << observation.getVal() << std::endl;
    }

    // make a constraint term for the background, and a RooRealVar for bkg 
    for (int b=1;b<=nbins;b++){
	double bkgy = (double)bkg->GetBinContent(b);
	RooRealVar *mean_ 	= new RooRealVar(Form("exp_bin_%d_In",b),Form("expected bin %d",b),bkgy); 
	RooRealVar *meanAsimov_ = new RooRealVar(Form("exp_bin_%d_In_asimov",b),Form("ASimov expected bin %d",b),bkgy); 
	mean_->setConstant(true);
	meanAsimov_->setConstant(true);
	RooRealVar *x_ = new RooRealVar(Form("exp_bin_%d",b),Form("bkg bin %d",b),bkgy,0.2*bkgy,bkgy*4);
	std::cout << " Pre-fit Exp background At " << b << ", " << x_->getVal() << std::endl;
	xlist_.add(*x_);
	mu_.add(*mean_);
	muA_.add(*meanAsimov_);
    }      

    // constraint PDF for background
    // Convert TH2 -> TMatrix 
    TMatrixDSym Tcovar(nbins);
    for (int i=0;i<nbins;i++){
	for (int j=0;j<nbins;j++){
	    if (ignoreCorrelation){ 
		if (i==j){
		    Tcovar[i][j] = covar->GetBinContent(i+1,j+1);
		    //std::cout << data->GetBinContent(i+1) << "\t" << bkg->GetBinContent(i+1) << "\t" << TMath::Sqrt(covar->GetBinContent(i+1,j+1))/bkg->GetBinContent(i+1) << std::endl;
		    }
		else Tcovar[i][j] = 0;}
	    else{
		Tcovar[i][j] = covar->GetBinContent(i+1,j+1);
		}
	    }
	}
	std::cout<< "Made Covariance" << std::endl;
	RooMultiVarGaussian constraint_pdf("constraint_pdf","Constraint for background pdf",xlist_,mu_,Tcovar);
	std::cout<< "Made Covariance Gauss" << std::endl;

	// Make the signal component 
	 RooRealVar r("r","r",1,0,10);  // remove the range, and re-eval LH I think is best 
	r.removeRange();
	RooArgList signals_;
	for (int b=1;b<=nbins;b++) {
	    //RooProduct *sigF = new RooProduct(Form("signal_%d",b),"signal nominal",RooArgSet(r,RooFit::RooConst(signal->GetBinContent(b))));
	    RooFormulaVar *sigF = new RooFormulaVar(Form("signal_%d",b),Form("@0*%g",signal->GetBinContent(b)),RooArgSet(r));
	    std::cout << " Signal At " << b << ", " << sigF->getVal() << std::endl;
	    signals_.add(*sigF);
	}

	RooArgList plist_;
	RooArgList slist_;

	sampleType.setIndex(1); 
	RooSimultaneous combined_pdf("combined_pdf","combined_pdf",sampleType);
	for (int b=1;b<=nbins;b++){
	    RooAddition *sum = new RooAddition(Form("splusb_bin_%d",b),Form("Signal plus background in bin %d",b),RooArgList(*((RooRealVar*)(signals_.at(b-1))),*((RooRealVar*)(xlist_.at(b-1)))));
	    RooPoisson  *pois = new RooPoisson(Form("pdf_bin_%d",b),Form("Poisson in bin %d",b),observation,(*sum)); 
	    combined_pdf.addPdf(*pois,Form("%d",b-1));
	    slist_.add(*sum);
	    plist_.add(*pois);
	}
	combined_pdf.Print("v");
	obsdata.Print("v");
	// Make a prodpdf instread
	RooProdPdf combinedpdfprod("maybefinalpdf","finalpdf",RooArgList(combined_pdf,constraint_pdf));
	RooAbsReal *nll_ = combined_pdf.createNLL(obsdata,RooFit::ExternalConstraints(RooArgList(constraint_pdf)));
	//
	RooMinimizer m(*nll_);
	m.minimize("Minuit2","minimize");
	double nllMin = nll_->getVal();
	double rMin = r.getVal();

	TFile *fout; 
	TTree *tree;

	float deltaNLL_;
	float r_;

	// Now make an asimov dataset
	// make a histogram for post-fits 
	TH1F *h_post_fit = (TH1F*)bkgcombfit->Clone(); h_post_fit->SetLineColor(4); 
	h_post_fit->SetName("simple");

	r.setConstant(true);
	RooMinimizer mc(*nll_);
	r.setVal(0); mc.minimize("Minuit2","minimize"); 
	RooDataSet asimovdata("AsimovData","Asimov in all Bins",obsargset);

	for (int b=1;b<=nbins;b++){
	    sampleType.setIndex(b-1);
	    //RooArgSet localset(observation,sampleType);
	    //obsdata.add(localset);
	    double exp = (double) (TMath::Nint((*(RooRealVar*)slist_.at(b-1)).getVal()));
	    ((RooRealVar*)muA_.at(b-1))->setVal(exp); 
	    observation.setVal(exp);
	    h_post_fit->SetBinContent(b,exp);
	    std::cout << " post fit Exp background At " << b << ", Simple code=" << exp << ", combine code=" << bkgcombfit->GetBinContent(b) << " Observed in the data " << data->GetBinContent(b) << std::endl;
	    std::cout << " Asi = "<< observation.getVal() << ", besty = " << ((RooRealVar*)muA_.at(b-1))->getVal()  << " before the fit that was " << bkg->GetBinContent(b) << std::endl;
	    asimovdata.add(RooArgSet(observation,sampleType));
	}
	TCanvas *can = new TCanvas();
	data->SetMarkerSize(1.0);
	data->SetMarkerStyle(20);
	bkgcombfit->Draw("");
	data->Draw("samep");
	signal->SetLineColor(2);
	signal->Draw("sameh");
	bkgcombfit->SetLineColor(1);
	h_post_fit->Draw("histsame");
	TLegend *leg = new TLegend(0.6,0.6,0.89,.89);
	leg->AddEntry(&*data,"data","PEL");
	leg->AddEntry(h_post_fit,"postfit simplified LH","L");
	leg->AddEntry(bkgcombfit,"postfit full LH","L");
	leg->AddEntry(signal,"prefit signal","L");
	leg->Draw();
	can->SetLogy();
	can->SaveAs("postfit.pdf");

	/* Reset constraints ! */
	RooMultiVarGaussian asimov_constraint_pdf("asimov_constraint_pdf","Constraint for background pdf",xlist_,muA_,Tcovar);
	RooAbsReal *nllA_ = combined_pdf.createNLL(asimovdata,RooFit::ExternalConstraints(RooArgList(asimov_constraint_pdf)));


	// dfile->Close();
	// sfile->Close();
	// signalfile->Close();
	obsdata.Print("v");
	asimovdata.Print("v");


	if (!justCalcLimit){

	    fout = new TFile(outnameRDeltaNLL.c_str(),"RECREATE");
	    tree = new TTree("limit","limit");
	    tree->Branch("r",&r_,"r/F");
	    tree->Branch("deltaNLL",&deltaNLL_,"deltaNLL/F");
	    r.setConstant(false);

	  r.setMin(RMIN);
	  r.setMax(RMAX);

	    RooMinimizer *minimG;
	    if (doExpected) minimG = new RooMinimizer(*nllA_);
	    else minimG = new RooMinimizer(*nll_);
	    minimG->minimize("Minuit2","minimize");
	    r_=r.getVal();
	    deltaNLL_=0;
	    tree->Fill();
	    if (doExpected) nllMin = nllA_->getVal();
	    else nllMin = nll_->getVal();


	    r.setConstant(true);
	    RooMinimizer *minimC;
	    if (doExpected) minimC = new RooMinimizer(*nllA_);
	    else minimC = new RooMinimizer(*nll_);

	  for(float rv=RMIN;rv<=RMAX;rv+=(RMIN-RMAX)/nPoints){
		r.setVal(rv);
		r_=rv;
		minimC->minimize("Minuit2","minimize");
		if (doExpected) deltaNLL_ = nllA_->getVal() - nllMin; 
		else deltaNLL_ = nll_->getVal() - nllMin; 
		std::cout << "r="<< rv <<", Dnll="<<deltaNLL_ << std::endl;
		tree->Fill();
	    }

	    fout->cd();
	    tree->Write();
	    //corr->Write();
	    fout->Close();
	 std::cout << " .... Saved stuff to " << outnameRDeltaNLL << std::endl;
	}


	r.setConstant(false);
	RooMinimizer *minimG1;
	if (doExpected) minimG1 = new RooMinimizer(*nllA_);
	else minimG1 = new RooMinimizer(*nll_);
	minimG1->minimize("Minuit2","minimize");
	double rValForRange = 0;
	if (r.getVal() > 0) rValForRange = r.getVal();
	double minRangeForLimit = rValForRange-r.getError()*2.;
	double maxRangeForLimit = rValForRange+r.getError()*5.;
	if (maxRangeForLimit <= 0)
	    return 0;
	if (minRangeForLimit <= 0) minRangeForLimit = maxRangeForLimit/20.;
	// double maxRangeForLimit = 0.1;
	double stepsForLimit = (maxRangeForLimit-minRangeForLimit)/20.;
	// double UL = getUpperLimit(nll_,nllA_,&r,0.95,runExpected);
	// std::cout << "Upper Limit 95% " << UL << std::endl;
	// return UL;
	double limit = 99;
	fout = new TFile(outname.c_str(),"RECREATE");
	tree = new TTree("limit","limit");
	tree->Branch("limit",&limit,"limit/D");
	limit = getUpperLimit(nll_,nllA_,&r,0.95,runExpected,minRangeForLimit,maxRangeForLimit,stepsForLimit);
	tree->Fill();
	if (doExpected){
	    tree->Fill();
	    tree->Fill();
	    tree->Fill();
	    tree->Fill();
	}
	tree->Write();
	fout->Close();
	std::cout << "Upper Limit 95% " << limit << std::endl;
	return limit;


	/*
	   RooAbsReal *nll_ = combinedpdfprod.createNLL(obsdata);
	   nll_->Print("v");
	// Minimize
	RooMinimizer m(*nll_);
	r.setConstant(true);
	std::cout << combinedpdfprod.getVal() << std::endl;
	std::cout << constraint_pdf.getVal() << std::endl;
	//m.Print();
	m.minimize("Minuit2","minimize");
	*/
}
