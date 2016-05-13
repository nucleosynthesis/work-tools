//Simple script to fit a signal with background + systematics and data

bool isTH1Input=false;

void fitSignal(){

std::string shapes_file = "mlfit.root";
std::string data_file = "param_ws.root";
std::string channel = "ch1";
     
     TFile *dfile = TFile::Open(data_file.c_str());
     TFile *sfile = TFile::Open(shapes_file.c_str());

     TH1F *bkg   = (TH1F*)sfile->Get(Form("shapes_fit_b/%s/total",channel.c_str()));
     TH1F *data  = (TH1F*)dfile->Get("SR_data");		// TH1 for data 
     TH1F *signal= (TH1F*)dfile->Get("SR_signal");		// TH1 for signal 
     TH2F *covar = (TH2F*)sfile->Get(Form("shapes_fit_b/%s/total_covar",channel.c_str()));

     // bkg and covariance defined as pdf / GeV, so scale by bin widhts 
     //

     int nbins = data->GetNbinsX();

     if (!isTH1Input){
      for (int b=1;b<=nbins;b++){
       double bw = bkg->GetBinWidth(b);
       bkg->SetBinContent(b,bkg->GetBinContent(b)*bw);
       for (int j=1;j<=nbins;j++){
       	covar->SetBinContent(b,j,covar->GetBinContent(b,j)*bw*bw);
       }
      }
     }

     RooArgList xlist_;
     RooArgList olist_;
     RooArgList mu_;

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
        observation.setVal(data->GetBinContent(b));
        sampleType.setIndex(b-1);
        std::cout << sampleType.getLabel() << ", " << sampleType.getIndex() << std::endl;
        //RooArgSet localset(observation,sampleType);
   	//obsdata.add(localset);
        obsdata.add(RooArgSet(observation,sampleType));
	std::cout << " Observed at " << b << ", " << observation.getVal() << std::endl;
     }

     // make a constraint term for the background, and a RooRealVar for bkg 
     for (int b=1;b<=nbins;b++){
	double bkgy = (double)bkg->GetBinContent(b);
	RooRealVar *mean_ = new RooRealVar(Form("exp_bin_%d_In",b),Form("expected bin %d",b),bkgy); 
	mean_->setConstant(true);
	RooRealVar *x_ = new RooRealVar(Form("exp_bin_%d",b),Form("bkg bin %d",b),bkgy,0.2*bkgy,bkgy*4);
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
       // Who cares about poissons?
       //RooGaussian *pois = new RooGaussian(Form("pdf_bin_%d",b),Form("Poisson in bin %d",b),observation,(*sum),RooFit::RooConst(TMath::Sqrt(sum->getVal())));
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

     // constrained fit!
     r.setConstant(true);
     double nllMin = nll_->getVal();

     TFile *fout = new TFile("simple.root","RECREATE");
     TTree *tree = new TTree("limit","limit");

     float deltaNLL_;
     float r_;
     tree->Branch("r",&r_,"r/F");
     tree->Branch("deltaNLL",&deltaNLL_,"deltaNLL/F");

     RooMinimizer mc(*nll_);
     //combinedpdfprod.fitTo(obsdata);
     //
     for(float rv=-2;rv<=2;rv+=0.2){
	r.setVal(rv);
	r_=rv;
	mc.minimize("Minuit2","minimize");
	deltaNLL_ = nll_->getVal() - nllMin; 
	tree->Fill();
     }

     fout->cd();
     tree->Write();
     fout->Close();
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
