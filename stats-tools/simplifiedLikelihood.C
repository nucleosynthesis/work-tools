//Simple script to fit a signal with background + systematics and data

bool isTH1Input=false;
std::string channel = "ggH_hinv_13TeV_datacard_SR_monoJ";
bool ignoreCorrelation = false;
bool justCalcLimit = false;

double GetCLs(RooAbsReal *nllD_, RooAbsReal *nllA_, RooRealVar *r, double rVal){
   
  r->setConstant(0);  
  RooMinimizer mCA(*nllA_);
  mCA.minimize("Minuit2","minimize"); 
  double minNllA_ = nllA_->getVal();
  RooMinimizer mCD(*nllD_);
  mCD.minimize("Minuit2","minimize");
  double minNllD_ = nllD_->getVal();
  rBestD_ = r->getVal();
  std::cout << "R Best =  " << rBestD_ << std::endl;

  r->setConstant(1);  r->setVal(rVal);
  RooMinimizer mUA(*nllA_);
  mUA.minimize("Minuit2","minimize"); 
  RooMinimizer mUD(*nllD_);
  mUD.minimize("Minuit2","minimize");

  double qmu = 2*(nllD_->getVal() - minNllD_); if (qmu < 0) qmu = 0;
  if (rVal < rBestD_) qmu=0;
  
  double qA  = 2*(nllA_->getVal() - minNllA_); if (qA < 0) qA = 0; // shouldn't this always be 0?

  double CLsb = ROOT::Math::normal_cdf_c(sqrt(qmu));
  double CLb  = ROOT::Math::normal_cdf(sqrt(qA)-sqrt(qmu));
  if (qmu > qA) {
    // In this region, things are tricky
    double mos = sqrt(qA); // mu/sigma
    CLsb = ROOT::Math::normal_cdf_c( (qmu + qA)/(2*mos) );
    CLb  = ROOT::Math::normal_cdf_c( (qmu - qA)/(2*mos) );
  }
  double CLs  = (CLb == 0 ? 0 : CLsb/CLb);
  return CLs;
    
}
double getUpperLimit(RooAbsReal *nllD_, RooAbsReal *nllA_, RooRealVar *r, double cl){

  rMin = 0.1;
  rMax = 2.; 

  TGraph *CLSgraph = new TGraph(); int pt=0;
  for (double rV = rMin;rV<=rMax;rV+=0.1){
  	double clsV = GetCLs(nllD_,nllA_,r,rV);
	CLSgraph->SetPoint(pt,clsV,rV);
	pt++;
  }
//  for (int pt=0;pt<CLSgraph->GetN();pt++){
//	std::cout << " At r="<<CLSgraph->GetY()[pt] << ",  CLs="<<CLSgraph->GetX()[pt]<<std::endl;
//  }

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

double fitSignal(std::string outname="simple.root"){

	std::string shapes_file = "mlfit.root";
	std::string data_file = "monoJet.root";
     
     TFile *dfile = TFile::Open(data_file.c_str());
     TFile *sfile = TFile::Open(shapes_file.c_str());

     TH1F *bkg    = (TH1F*)sfile->Get(Form("shapes_fit_b/%s/total",channel.c_str()));
     TH1F *signal = (TH1F*)sfile->Get(Form("shapes_prefit/%s/total_signal",channel.c_str()));		// TH1 for signal  
     TH1F data(getData((RooWorkspace*)dfile->Get("w"),signal));			// TH1 for data :( 
     TH2F *covar  = (TH2F*)sfile->Get(Form("shapes_fit_b/%s/total_covar",channel.c_str()));

     covar->Print();
     signal->Print();
     bkg->Print();

     TH2F *corr = (TH2F*)covar->Clone();  corr->SetName("correlation");
     
     // bkg and covariance defined as pdf / GeV, so scale by bin widhts 
     int nbins = data.GetNbinsX();

     if (!isTH1Input){
      for (int b=1;b<=nbins;b++){
       double bw = bkg->GetBinWidth(b);
       bkg->SetBinContent(b,bkg->GetBinContent(b)*bw);
       bkg->SetBinError(b,bkg->GetBinError(b)*bw);
       signal->SetBinContent(b,signal->GetBinContent(b)*bw);
       for (int j=1;j<=nbins;j++){
        double bj = bkg->GetBinWidth(j);
       	covar->SetBinContent(b,j,covar->GetBinContent(b,j)*bw*bj);
	if (ignoreCorrelation && b!=j) covar->SetBinContent(b,j,0); 
       }
      }
     }

     for (int b=1;b<=nbins;b++){
       for (int j=1;j<=nbins;j++){
	double sigb = TMath::Sqrt(covar->GetBinContent(b,b));
	double sigj = TMath::Sqrt(covar->GetBinContent(j,j));
	corr->SetBinContent(b,j,covar->GetBinContent(b,j)/(sigb*sigj));
	std::cout << b << ", " << j << ", " << covar->GetBinContent(b,j) << ", " << corr->GetBinContent(b,j)  << std::endl;
	if ( b==j )  std::cout << "      " << bkg->GetBinError(b)*bkg->GetBinError(b)  << std::endl;
       }
     }

     RooArgList xlist_;
     RooArgList olist_;
     RooArgList mu_;

     bkg->Print() ;
     covar->Print() ; 
     signal->Print() ;
     data.Print() ;  

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
        observation.setVal(data.GetBinContent(b));
        obsdata.add(RooArgSet(observation,sampleType));
	std::cout << " Observed at " << b << ", " << observation.getVal() << std::endl;
     }

     // make a constraint term for the background, and a RooRealVar for bkg 
     for (int b=1;b<=nbins;b++){
	double bkgy = (double)bkg->GetBinContent(b);
	RooRealVar *mean_ = new RooRealVar(Form("exp_bin_%d_In",b),Form("expected bin %d",b),bkgy); 
	mean_->setConstant(true);
	RooRealVar *x_ = new RooRealVar(Form("exp_bin_%d",b),Form("bkg bin %d",b),bkgy,0.01*bkgy,bkgy*10);
	std::cout << " Exp background At " << b << ", " << x_->getVal() << std::endl;
	xlist_.add(*x_);
	mu_.add(*mean_);
     }      

     // constraint PDF for background
     // Convert TH2 -> TMatrix 
     TMatrixDSym Tcovar(nbins);
     for (int i=0;i<nbins;i++){
      for (int j=0;j<nbins;j++){
	//if (i==j)Tcovar[i][j] = covar->GetBinContent(i+1,j+1);
	//else Tcovar[i][j] = 0;
	Tcovar[i][j] = covar->GetBinContent(i+1,j+1);
      }
     }
     std::cout<< "Made Covariance" << std::endl;
     RooMultiVarGaussian constraint_pdf("constraint_pdf","Constraint for background pdf",xlist_,mu_,Tcovar);
     std::cout<< "Made Covariance Gauss" << std::endl;
     
     // Make the signal component 
     RooRealVar r("r","r",1,-5,5);
     RooArgList signals_;
     for (int b=1;b<=nbins;b++) {
	RooProduct *sigF = new RooProduct(Form("signal_%d",b),"signal nominal",RooArgSet(r,RooFit::RooConst(signal->GetBinContent(b))));
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
       //RooGaussian *gaus = new RooGaussian(Form("pdf_bin_%d",b),Form("Poisson in bin %d",b),observation,(*sum),RooFit::RooConst(TMath::Sqrt(sum->getVal())));
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
     m.setStrategy(1);
     m.minimize("Minuit2","minimize");
     // constrained fit!
     r.setConstant(true);
     double nllMin = nll_->getVal();

     TFile *fout = new TFile(outname.c_str(),"RECREATE");
     TTree *tree = new TTree("limit","limit");

     float deltaNLL_;
     float r_;
     tree->Branch("r",&r_,"r/F");
     tree->Branch("deltaNLL",&deltaNLL_,"deltaNLL/F");

     RooMinimizer mc(*nll_);
     //combinedpdfprod.fitTo(obsdata);
     //
     double minimum_r = r.getVal();
     r_=r.getVal();
     deltaNLL_=0;
     tree->Fill();
     if (!justCalcLimit){
      for(float rv=-2;rv<=2;rv+=0.1){
	r.setVal(rv);
	r_=rv;
	mc.minimize("Minuit2","minimize");
	deltaNLL_ = nll_->getVal() - nllMin; 
	std::cout << "r="<< rv <<", Dnll="<<deltaNLL_ << std::endl;
	tree->Fill();
      }
     }

     fout->cd();
     tree->Write();
     corr->Write();
     fout->Close();

     // Now make an asimov dataset
     r.setVal(0); mc.minimize("Minuit2","minimize"); 
     RooDataSet asimovdata("AsimovData","Asimov in all Bins",obsargset);
 
     for (int b=1;b<=nbins;b++){
        sampleType.setIndex(b-1);
        //std::cout << sampleType.getLabel() << ", " << sampleType.getIndex() << std::endl;
        //RooArgSet localset(observation,sampleType);
   	//obsdata.add(localset);
	observation.setVal((int)bkg->GetBinContent(b));
        asimovdata.add(RooArgSet(observation,sampleType));
     }
     RooAbsReal *nllA_ = combined_pdf.createNLL(asimovdata,RooFit::ExternalConstraints(RooArgList(constraint_pdf)));

     //double UL = getUpperLimit(nll_,nllA_,&r,0.95);
     UL = 1.;
     std::cout << "Upper Limit 95% " << UL << ", Best Fit r=" << minimum_r  << std::endl;
     return UL;
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
