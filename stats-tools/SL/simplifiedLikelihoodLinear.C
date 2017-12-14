// ***********************************************************/
// simplifiedLikelihood as in CMS-NOTE-2017-001 
// Original Author - Nicholas Wardle - Imperial College London 
// ***********************************************************/

#include "NLL.h"
//#include "Moments.h"

/* OPTIONS */ 
bool gMultiplicative=false;
bool justCalcLimit = false;
bool ignoreCorrelation = false;
bool includeQuadratic  = false;
bool verb=1;

// for LH scanning
double RMIN = -.5;
double RMAX = 2.0;
int globalNbins=100;
int globalNpoints=30;
std::string outname = "SL.root";

// ********************* Touch nothing below here ! ************ /
const int MAXBINS=100;
// USER INPUTS 	(inputs from Note below, you should use python to configure this) 
double globalData[MAXBINS] ; // = {1964,877,354,182,82,36,15,11};
double globalBackground[MAXBINS]; // = {2006.4,836.4,350.,147.1,62.0,26.2,11.1,4.7};
double globalSignal[MAXBINS] ; // = {47,29.4,21.1,14.3,9.4,7.1,4.7,4.3};
double globalThirdMoments[MAXBINS] ; // = {47,29.4,21.1,14.3,9.4,7.1,4.7,4.3};
double globalCovariance[(int) (MAXBINS*MAXBINS)] ; /*= 
{
18774.2, -2866.97, -5807.3, -4460.52, -2777.25, -1572.97, -846.653, -442.531, -2866.97, 496.273, 900.195, 667.591, 403.92, 222.614, 116.779, 59.5958, -5807.3, 900.195, 1799.56, 1376.77, 854.448, 482.435, 258.92, 134.975, -4460.52, 667.591, 1376.77, 1063.03, 664.527, 377.714, 203.967, 106.926, -2777.25, 403.92, 854.448, 664.527, 417.837, 238.76, 129.55, 68.2075, -1572.97, 222.614, 482.435, 377.714, 238.76, 137.151, 74.7665, 39.5247, -846.653, 116.779, 258.92, 203.967, 129.55, 74.7665, 40.9423, 21.7285, -442.531, 59.5958, 134.975, 106.926, 68.2075, 39.5247, 21.7285, 11.5732
};
*/
/*{
16787.2,-1691.3,-4520.3,-3599.9,-2286.4,-1316.5,-719.8,-381.1,
603.1,754.6,513.3,294.,154.9,78.1,38.3,
1454.0,1110.9,691.1,392.3,212.1,111.2,
871.2,551.8,318.1,174.3,92.5,
353.9,206.2,114.1,61.0,
121.3,67.6,36.4,
38.0,20.6,
11.2
};
*/

// *******************************************//
void Minimize(RooMinimizer &minim){
//        minim.optimizeConst(1);
	minim.minimize("Minuit","minimize");	
}
// *******************************************//
double globalVariance[(int) MAXBINS] ;  
void getCoefficiencts(double *A, double *B, double *C, int bin){
    // mean 
    double m1 = globalBackground[bin-1];
    double m2 = globalVariance[bin-1];
    double m3 = globalThirdMoments[bin-1];
    
    std::complex<double> inside(m3*m3 - 8*m2*m2*m2,0);
    std::complex<double> root = std::pow(inside,0.5);
    std::complex<double> c_m3(-m3,0);
    std::complex<double> k3 = c_m3+root;
    std::complex<double> k = std::pow(k3,1./3);

    std::complex<double> j2(1,TMath::Sqrt(3));
    std::complex<double> j(1,-TMath::Sqrt(3));
	
    std::complex<double> c = -j*m2/k-0.5*j2*k;

    double localC = c.real();
    
    // What should be done in this case really? should we flip the sign?
    // for now what I will do is to ignore the C part and return the linear component only - sqrt(m2)
    *A = m1 - localC/2;
    *C = localC;
    if ( m2 - (localC*localC)/2 < 0 ) {
      std::cout << " Cant calculate coeffs, resort to linear version " << bin << ", " << *A << ", " << *C << ", " <<  m1 << " " <<  m2 << " " <<  m3 <<std::endl; 
      *B = TMath::Sqrt(m2) ;
      *C = 0;
    } else {
      *B = TMath::Sqrt(m2 - (localC*localC)/2);
    }
}
//ROOT::Math::MinimizerOptions::SetDefaultStrategy(2);
//ROOT::RooMsgService::setGlobalKillBelow(RooFit::FATAL);
TGraph *globalLimitGraph;
TRandom3 *rnd = new TRandom3;
// FUNCTIONS START HERE
TGraph *vectorToTGraph(double *V){
 TGraph *gr = new TGraph();
 for (int i=0;i<globalNbins;i++){
	gr->SetPoint(i,i+.5,V[i]);
 }
 return gr;
}
TH1F *vectorToTH1(double *V){
 TH1F *gr = new TH1F(Form("h%g",rnd->Uniform()),"h",globalNbins,0,globalNbins);
 for (int i=0;i<globalNbins;i++){
	gr->SetBinContent(i+1,V[i]);
 }
 return gr;
}
TH2D *vectorToTH2(double *V){
 TH2D *gr = new TH2D(Form("h%g",rnd->Uniform()),"h",globalNbins,0,globalNbins,globalNbins,0,globalNbins);
 int vCounter = 0;
 for (int i=0;i<globalNbins;i++){
  for (int j=0;j<globalNbins;j++){
        if (verb) std::cout << "i="<<i<<", j="<< j<<", V="<<V[vCounter] <<std::endl;
	gr->SetBinContent(i+1,j+1,V[vCounter]);
	// check correlation of off diagonals 
	if (i==j)  globalVariance[i]=V[vCounter];
	vCounter++;
  }
 }
 /*
 // make sure initialize to 0 so that TMatrixDSym handles mirroring 
 for (int i=0;i<globalNbins;i++){
  for (int j=0;j<globalNbins;j++){
  	if (i==j) continue;
  	double sx = TMath::Sqrt(gr->GetBinContent(i+1,i+1));
  	double sy = TMath::Sqrt(gr->GetBinContent(j+1,j+1));
   	double cv = gr->GetBinContent(i+1,j+1)/(sx*sy);
	if ( TMath::Abs(cv) > 0.999 ) {
		std::cout << " was " << cv*sx*sy<< std::endl;
		gr->SetBinContent(i+1,j+1,0.999*(cv/TMath::Abs(cv))*sx*sy);
		std::cout << " is " << gr->GetBinContent(i+1,j+1) << std::endl;
	}
  }
 }
 */
 return gr;
}

double GetCLs(RooAbsReal *nllD_, RooAbsReal *nllA_, RooRealVar *r, double rVal){
    r->setConstant(false);  

    RooMinimizer mCA(*nllA_);
    Minimize(mCA);//.minimize("Minuit","minimize"); 
    double minNllA_ = nllA_->getVal();
    //double rBestA_ = r->getVal();

    RooMinimizer mCD(*nllD_);
    Minimize(mCD);//.minimize("Minuit","minimize");
    double minNllD_ = nllD_->getVal();
    double rBestD_ = r->getVal();

    // Conditional fit
    r->setConstant(true);  r->setVal(rVal);

    RooMinimizer mUA(*nllA_);
    Minimize(mUA);//.minimize("Minuit","minimize");
    double nllFixA = nllA_->getVal();

    RooMinimizer mUD(*nllD_);
    Minimize(mUD);//.minimize("Minuit","minimize");
    double nllFixD = nllD_->getVal();

    // Now we plug into https://arxiv.org/pdf/1007.1727.pdf
   
    // Eqn 16. Our test-statistic is defined as 
    // q_mu = {  -2 ln  [ L(mu,theta_mu)/L(mu=0,theta_0) ]   	      ... hat{mu} < 0 
    //        {  -2 ln  [ L(mu,theta_mu)/L(mu=hat{mu},hat{theta}) ]   ... 0 <= hat{mu} <= mu
    //        {   0 						      ... hat{mu} > mu

    double qmu = 2*(nllFixD - minNllD_); if (qmu < 0) qmu = 0;
    if (rVal < rBestD_) qmu=0;
    if (rBestD_<0 ) {   // Eqn 16 
	r->setVal(0);
	Minimize(mUD);//.minimize("Minuit","minimize");
	double nllFix0Signal_ = nllD_->getVal();
	qmu =  2*(nllFixD - nllFix0Signal_); if (qmu < 0) qmu = 0;
    }

    double qA  = 2*(nllFixA - minNllA_); if (qA < 0) qA = 0;

    // Eqns 66 and 65 
    double CLsb = ROOT::Math::normal_cdf_c(TMath::Sqrt(qmu));
    double CLb  = ROOT::Math::normal_cdf(TMath::Sqrt(qA)-TMath::Sqrt(qmu));
    
    // Eqn 66 (lower half) 
    if (qmu > qA) {
	// In this region, things are tricky
	double mos = TMath::Sqrt(qA); // mu/sigma
	CLsb = ROOT::Math::normal_cdf_c( (qmu + qA)/(2*mos) );
	CLb  = ROOT::Math::normal_cdf_c( (qmu - qA)/(2*mos) );
    }

    r->setConstant(false);

    double CLs  = (CLb == 0 ? 0 : CLsb/CLb);
    std::cout << "at r = " << rVal <<  ", CLsplusb = " << CLsb << ", CLb " << CLb << ", CLs " << CLs << std::endl;
    std::cout << "rMIN (data) = " << rBestD_ << ", qmu = " << qmu << ", qA = " << qA <<std::endl;
    //return CLsb;
    return CLs;

}

double getUpperLimit(RooAbsReal *nllD_, RooAbsReal *nllA_, RooRealVar *r, double cl,bool runExpected,double rMin,double rMax,double steps){

    globalLimitGraph = new TGraph(); 
    TGraph *gCLS	     = new TGraph(); int pt=0;
    double  cls_min=999;
    double  cls_max=-999;
    double clsV;
    //if (runExpected) clsV = GetExpectedCLs(nllA_,r,rMin);
    clsV = GetCLs(nllD_,nllA_,r,rMin);

    for (double rV = rMin;rV<=rMax;rV+=steps){
	//if (runExpected) clsV = GetExpectedCLs(nllA_,r,rV);
	clsV = GetCLs(nllD_,nllA_,r,rV);
	gCLS->SetPoint(pt,clsV,rV);
	globalLimitGraph->SetPoint(pt,rV,clsV);
	pt++;
	if (clsV<cls_min )cls_min = clsV;
	if (clsV>cls_max )cls_max = clsV;
    }
    if (cls_min>1-cl) return   rMax ;
    if (cls_max<1-cl) return   rMin ;
    globalLimitGraph->SetMarkerSize(1.0);
    globalLimitGraph->SetMarkerStyle(21);
    globalLimitGraph->SetLineWidth(2);
    globalLimitGraph->SetLineColor(1);
    return gCLS->Eval(1-cl);
}


/* LEAVE THESE (CMS specific) */
const bool isTH1Input=true;
const std::string channel = "htsearch";
bool doExpected = false;
/* ***************************/ 


TH1F getData(RooWorkspace *w, TH1F *sigh){

    
    RooBinning bins(sigh->GetNbinsX(), ((sigh->GetXaxis())->GetXbins())->GetArray(), "databinning");
    RooRealVar *mv = (RooRealVar*)w->var("CMS_th1x");
    mv->setBinning(bins,"databinning");

    RooPlot *fr1 = mv->frame();
    RooDataHist *dataF = (RooDataHist*)w->data("data_obs");
    RooDataHist *data = (RooDataHist*)dataF->reduce(RooFit::Cut(Form("CMS_channel==CMS_channel::%s",channel.c_str())));

    TH1F* t = (TH1F*) data->createHistogram("t",*mv); //makes the internal histogra	
    return *t; 
}
  
double simplifiedLikelihoodLinear(){
	
    std::cout << " Running SimplifiedLikelihoodLinear " << std::endl;
    gROOT->SetBatch(1);
    gStyle->SetOptStat(0);
    
    bool doExpected = false;

    if (ignoreCorrelation) outname += "NoCorrelation";
    if (doExpected) outname += "Expected";
    //std::string outnameRDeltaNLL = outname+ "DeltaNLL";
    outname += ".root";
    //outnameRDeltaNLL += ".root";

   
    // Convert the Inputs ---------------------------------
    TGraph *dataG = (TGraph*) vectorToTGraph(globalData);
    TH2D *covar  = (TH2D*) vectorToTH2(globalCovariance);
    TH1F *bkg    = (TH1F*) vectorToTH1(globalBackground);
    TH1F *signal = (TH1F*) vectorToTH1(globalSignal);
    // ----------------------------------------------------


    if (verb){
      signal->Print();
      bkg->Print();
      covar->Print();
      dataG->Print();
    }

    TH1F *data = (TH1F*)bkg->Clone(); data->SetName("data");
    for (int b=0;b<data->GetNbinsX();b++){
	data->SetBinContent(b+1,dataG->GetY()[b]);
	if (verb) {
	 std::cout << " N Events in bin " << b+1 << " = " << data->GetBinContent(b+1) <<std::endl;
	 std::cout << " N Bkg in bin " << b+1 << " = " << bkg->GetBinContent(b+1) <<std::endl;
	}
    }


    TH2D *corr = (TH2D*)covar->Clone();  corr->SetName("correlation");
    int nbins = globalNbins;
    for (int b=1;b<=nbins;b++){
	for (int j=1;j<=nbins;j++){
	    double sigb = TMath::Sqrt(covar->GetBinContent(b,b));
	    double sigj = TMath::Sqrt(covar->GetBinContent(j,j));
	    corr->SetBinContent(b,j,covar->GetBinContent(b,j)/(sigb*sigj));
	    /*if (gMultiplicative) { 
	    	double Bb = bkg->GetBinContent(b);
	    	double Cb = TMath::Log(1+sigb*sigb/(Bb*Bb)) ; // mean is 1!
	    	double Bj = bkg->GetBinContent(b);
	    	double Cj = TMath::Log(1+sigj*sigj/(Bj*Bj))  ;// mean is 1!
	    	covar->SetBinContent(b,j,corr->GetBinContent(b,j)*Cj*Cb);
	    }
	    */

	}
    }

    // Convert TH2 -> TMatrix 
    TMatrixDSym Tcovar(nbins);
    TMatrixDSym Tcorr(nbins);
    for (int i=0;i<nbins;i++){
	for (int j=0;j<nbins;j++){
	    if (ignoreCorrelation){ 
		if (i==j){
		    Tcovar[i][j] = covar->GetBinContent(i+1,j+1);
		    Tcorr[i][j]  = corr->GetBinContent(i+1,j+1);
		} else {
		  Tcorr[i][j] = 0;
		}
	    } else {
		Tcovar[i][j] = covar->GetBinContent(i+1,j+1);
		Tcorr[i][j]  = corr->GetBinContent(i+1,j+1);
		if (verb) std::cout << " Correlation (" << i+1 << "," << j+1 << ") " << corr->GetBinContent(i+1,j+1) << std::endl;
	    }
	 }
    }

    // Now we will build up the pdf model -> in the end we will feed this into our own likelihood 
    // 1. diagonalize the covariance matrix to get the directions for the "independant" parameters 

    TVectorD eigenv;
    TMatrixD eigenvectors = Tcorr.EigenVectors(eigenv);
    RooArgList philist_;

    for (int b=1;b<=nbins;b++){
	RooRealVar *phi = new RooRealVar(Form("phi_%d",b),Form("free parameter - %d",b),0,-5,5);
	philist_.add(*phi);
    }

    //return 0;
    // 2. build up the theta terms ( for b + theta ),  
    RooArgList thetalist_;
    
    for (int i=0;i<nbins;i++){
        RooArgList theta_components;
        for (int j=0;j<nbins;j++){
	   double sqrtLambda = TMath::Sqrt(eigenv[j]);
	   double E 	     = eigenvectors[i][j];  
	   RooFormulaVar *c = new RooFormulaVar(Form("c_%d_%d",i+1,j+1),Form("%g*%g*@0",sqrtLambda,E),RooArgList(*(philist_.at(j))));
	   theta_components.add(*c);
	}
	RooAddition *theta = new RooAddition(Form("theta_%d",i+1),Form("theta in bin - %d",i),theta_components);
	thetalist_.add(*theta);
    }

    RooArgList xlist_;
    RooArgList olist_;
    RooArgList mu_, muA_;

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
	if (verb) std::cout << sampleType.getLabel() << ", " << sampleType.getIndex() << std::endl;
	observation.setVal(data->GetBinContent(b));
	obsdata.add(RooArgSet(observation,sampleType));
	if (verb) std::cout << " Observed at " << b << ", " << observation.getVal() << std::endl;
    }

    TH1F *h_pre_fit = (TH1F*)bkg->Clone(); h_pre_fit->SetLineColor(1); h_pre_fit->SetLineStyle(3); 
    h_pre_fit->SetName("simple_prefit");

    // make a constraint term for the background, and a RooRealVar for bkg 
    for (int b=1;b<=nbins;b++){
	double bkgy = (double)bkg->GetBinContent(b);
	double kappa = TMath::Sqrt((double)covar->GetBinContent(b,b));
	if (gMultiplicative) kappa = 1+covar->GetBinContent(b,b)/(bkgy*bkgy);
	if (verb){
	  std::cout << " Covar = " << covar->GetBinContent(b,b) <<std::endl;
	  std::cout << " Kappa "  << b << ", = "<< kappa <<std::endl;
	}

	RooRealVar *mean_ ;	

	mean_ = new RooRealVar(Form("phi_bin_%d_In",b),Form("phi bin %d",b),0); 
	mean_->setConstant(true);
	//if (gMultiplicative) mean_->setError(1.);
	//else mean_->setError(1.);

	RooRealVar *meanAsimov_;
	meanAsimov_ = new RooRealVar(Form("Asimov_phi_bin_%d_In",b),Form("Asimov expected bin %d",b),0); 
	meanAsimov_->setConstant(true);

 	//double thMin = -4*kappa; 
	//if (bkgy-4*kappa < 0) thMin=-bkgy;

	//RooRealVar *theta_ 	= new RooRealVar(Form("theta_bin_%d",b),Form("delta bin %d",b),0,thMin,4*kappa); theta_->setConstant(false);
	//RooRealVar *theta_ 	= new RooRealVar(Form("theta_bin_%d",b),Form("delta bin %d",b),0,-4,4); theta_->setConstant(false);
	//theta_->setError(1);
	//theta_->setVal(0.01);
	//if (gMultiplicative){ theta_->setMin(-4); theta_->setMax(4);}

	RooFormulaVar *x_ ;
	RooAbsReal *theta_ = (RooAbsReal*)thetalist_.at(b-1);

	if (gMultiplicative)  x_ = new RooFormulaVar(Form("exp_bin_%d",b),Form("%g*TMath::Power(%g,@0)",bkgy,kappa),RooArgList(*theta_));
	else if (includeQuadratic)  {
	  double A,B,C;
	  getCoefficiencts(&A,&B,&C,b);
	  if (verb) {
		std::cout << " Coefficients " << "A = " << A << ", B =  " << B << ", C = " << C <<std::endl;
	  }
	  x_ = new RooFormulaVar(Form("exp_bin_%d",b),Form("%g+@0*%g+@0*@0*%g",A,B,C/2),RooArgList(*theta_));
	} else {
	  x_ = new RooFormulaVar(Form("exp_bin_%d",b),Form("%g+@0*%g",bkgy,kappa),RooArgList(*theta_));
        }

	if (verb) std::cout << " Pre-fit Exp background At " << b << ", " << x_->getVal() << std::endl;
	h_pre_fit->SetBinContent(b,x_->getVal());
	xlist_.add(*x_);
	//thetalist_.add(*theta_);
	
	mu_.add(*mean_);
	muA_.add(*meanAsimov_);
    }      
    // constraint PDF for background
    //std::cout << "is symmetric ? " << Tcovar.IsSymmetric() <<std::endl;
    //std::cout << "DET =  " << Tcovar.Determinant() <<std::endl;

    //RooMultiVarGaussian constraint_pdf("constraint_pdf","Constraint for background pdf",thetalist_,mu_,Tcovar);
    // Make the signal component 
    RooRealVar r("r","r",1,RMIN,RMAX);  // remove the range, and re-eval LH I think is best 
    //r.removeRange();
    RooArgList signals_;
    for (int b=1;b<=nbins;b++) {
	    //RooProduct *sigF = new RooProduct(Form("signal_%d",b),"signal nominal",RooArgSet(r,RooFit::RooConst(signal->GetBinContent(b))));
	    RooFormulaVar *sigF = new RooFormulaVar(Form("signal_%d",b),Form("@0*%g",signal->GetBinContent(b)),RooArgSet(r));
	    if (verb) std::cout << " Signal At " << b << ", " << sigF->getVal() << std::endl;
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
    // Make a prodpdf instread
    //RooProdPdf combinedpdfprod("maybefinalpdf","finalpdf",RooArgList(combined_pdf,constraint_pdf));
    //RooAbsReal *nll_ = combined_pdf.createNLL(obsdata,RooFit::ExternalConstraints(RooArgList(constraint_pdf)));
    RooRealVar *nll_ =(RooRealVar*) NLLDiagonal(slist_,*data, philist_,mu_);

    r.setVal(0.0);
    RooMinimizer m(*nll_);
    if (verb) std::cout << "NLL Value " << nll_->getVal()<< std::endl;
    //m.setStrategy(2);
    //m.setEps(0.01);
    Minimize(m); //.minimize("Minuit","minimize");

    double nllMin = nll_->getVal();
    double rMin = r.getVal();

    if (verb) std::cout << "RMIN = " << rMin << std::endl;

    TFile *fout; 
    TTree *tree;

    double deltaNLL_,nuisanceLL;
    double r_;

    // make a histogram for post-fits 
    TH1F *h_post_fit = (TH1F*)bkg->Clone(); h_post_fit->SetLineColor(4); 
    h_post_fit->SetName("simple");

    r.setConstant(true);

    RooMinimizer mc(*nll_);
    for (int b=1;b<=nbins;b++){
	    sampleType.setIndex(b-1);
	    //RooArgSet localset(observation,sampleType);
	    double expR = (double) (*(RooRealVar*)slist_.at(b-1)).getVal();
	    double expB = (double) (*(RooRealVar*)xlist_.at(b-1)).getVal();
	    double exp = (double) (TMath::Nint((*(RooRealVar*)slist_.at(b-1)).getVal()));
	    //observation.setVal(exp);
	    h_post_fit->SetBinContent(b,expB);
	    if (verb){
	      std::cout << " prefit signal in bin " << b << " = " << signal->GetBinContent(b) << std::endl;
	      std::cout << " data - total in bin  " << b << " = " << data->GetBinContent(b) - expR << std::endl;
	    }
    }

    TCanvas *can = new TCanvas();
    data->SetMarkerSize(1.0);
    data->SetMarkerStyle(20);
    //bkgcombfit->SetLineColor(1);
    signal->SetLineColor(2);
    signal->SetFillColor(kPink+5);
    data->Draw("PEL");
    h_post_fit->Draw("histsame");
    h_pre_fit->Draw("histsame");
    signal->Draw("histsame");

    TH1F *total_h = (TH1F*)h_post_fit->Clone(); total_h->SetName("totalsum");
    total_h->Add(signal,rMin);
    total_h->SetLineColor(kGreen+3);
    total_h->SetLineWidth(3);
    total_h->Draw("histsame");
    data->Draw("PELsame");
    TLegend *leg = new TLegend(0.6,0.6,0.89,.89);
    leg->AddEntry(&*data,"data","PEL");
    leg->AddEntry(h_pre_fit,"pre-fit background simplified LH","L");
    leg->AddEntry(h_post_fit,"post-fit background simplified LH","L");
    leg->AddEntry(total_h,Form("post-fit background+signal (#mu=%g) ",rMin),"L");
    leg->AddEntry(signal,"pre-fit signal (#mu=1)","L");
    leg->Draw();
    can->SetLogy();

    if (verb) obsdata.Print("v");

    double goCLS = 0;//GetCLs(nll_,nllA_,&r,1.);

    double db_[nbins];
    double tb_[nbins];

    TGraph *grLL = new TGraph();
    fout = new TFile(outname.c_str(),"RECREATE");
    tree = new TTree("limit","limit");
    tree->Branch("r",&r_,"r/D");
    
    double limit = 99;

    if (!justCalcLimit){

	tree->Branch("deltaNLL",&deltaNLL_,"deltaNLL/D");
	tree->Branch("nuisanceLL",&nuisanceLL,"nuisanceNLL/D");
	for (int b=0;b<nbins;b++){
	    tree->Branch(Form("nuis_bin_%d",b+1),&db_[b],Form("nuis_bin_%d/D",b+1));
	    tree->Branch(Form("bkg_bin_%d",b+1),&tb_[b],Form("bkg_bin_%d/D",b+1));
	}

	r.setConstant(false);

	r.setMin(RMIN);
	r.setMax(RMAX);

	RooMinimizer *minimG;
	//if (doExpected) minimG = new RooMinimizer(*nllA_);
	minimG = new RooMinimizer(*nll_);
	//minimG->setStrategy(2);
	//minimG->setEps(0.01);
	Minimize(*minimG); //->minimize("Minuit","minimize");
	r_=r.getVal();
	deltaNLL_=0;
	//nuisanceLL = -1*constraint_pdf.getLogVal();
	tree->Fill();
	//if (doExpected) nllMin = nllA_->getVal();
	nllMin = nll_->getVal();


	r.setConstant(true);
	RooMinimizer *minimC;
	//if (doExpected) minimC = new RooMinimizer(*nllA_);
	minimC = new RooMinimizer(*nll_);
	//minimC->setStrategy(2);
	minimC->setEps(0.01);

	// also save a graph of the profiled log-LH scan 
	grLL->SetName("deltaNLL_vs_r");
	grLL->SetLineColor(kRed);
	grLL->SetLineWidth(2);

	/*
	for (int ib=0;ib<nbins;ib++){
	      ((RooRealVar*)thetalist_.at(ib))->setVal(0);
	}
	*/

	int pt_i=0;
	r.setConstant(true);
	double dR = (RMAX-RMIN)/globalNpoints;
	std::cout << " Scanning profiled LH ... ";
	int counter = -1;
	for (float rv=RMAX;rv>=RMIN;rv-=dR){
	    counter+=1;
	    if ( counter%2==0 ) std::cout << "\b+" ;
	    else 	        std::cout << "\bx" ;
	    std::cout.flush();
	    r.setVal(rv);
	    r_=rv;
	    Minimize(*minimC); //->minimize("Minuit","minimize");
	    deltaNLL_  = nll_->getVal() - nllMin;
	    //nuisanceLL = -1*constraint_pdf.getLogVal();
	    if (verb) std::cout << "r="<< rv <<", Dnll="<<deltaNLL_ << std::endl;

	    grLL->SetPoint(pt_i,rv,2*deltaNLL_);
	    pt_i++;
	    for (int b=0;b<nbins;b++){
	          db_[b] = ((RooRealVar*)thetalist_.at(b))->getVal();//(((RooRealVar*)xlist_.at(b))->getVal() - (bkg->GetBinContent(b+1)) )/TMath::Sqrt(covar->GetBinContent(b+1,b+1));
		  tb_[b] = ((RooRealVar*)xlist_.at(b))->getVal();    //(((RooRealVar*)xlist_.at(b))->getVal() - (bkg->GetBinContent(b+1)) )/TMath::Sqrt(covar->GetBinContent(b+1,b+1));
		}

		tree->Fill();
	}
	std::cout << endl;
	std::cout << " ... finished profile LH scan " << std::endl;

	} else {

	  //double rValForRange=0;
	  double rValForRange = r.getVal();
	  double minRangeForLimit = rValForRange-r.getError()*0.1;  // something just below the minimum point 
	  double maxRangeForLimit = RMAX ; 			    // User setting rValForRange+r.getError()*5.;
	  if (rValForRange > 0 && maxRangeForLimit > rValForRange+r.getError()*5 ) maxRangeForLimit = rValForRange+r.getError()*5;
	  double stepsForLimit = (maxRangeForLimit-minRangeForLimit)/30.;
	  r.setMax(maxRangeForLimit);

	  // Calculate the limit 
	  r.setConstant(true);
	  RooMinimizer mc(*nll_);
	  r.setVal(0); Minimize(mc); //.minimize("Minuit","minimize"); 

	  // Make the background only Asimov data-set (for calculating CLb)
	  RooDataSet asimovdata("AsimovData","Asimov in all Bins",obsargset);
	  TH1F *dataAsimov = (TH1F*) data->Clone();
	  for (int b=1;b<=nbins;b++){
	    sampleType.setIndex(b-1);
	    double exp = (double) (TMath::Nint((*(RooRealVar*)slist_.at(b-1)).getVal()));
	    double constV = ((RooRealVar*)philist_.at(b-1))->getVal();
	    ((RooRealVar*) muA_.at(b-1))->setVal(constV); 
	    observation.setVal(exp);
	    asimovdata.add(RooArgSet(observation,sampleType));
	    dataAsimov->SetBinContent(b,exp);
	  }

	  // create NLL for asimov data 
	  //RooMultiVarGaussian asimov_constraint_pdf("asimov_constraint_pdf","Constraint for background pdf",thetalist_,muA_,Tcovar);
	  //RooAbsReal *nllA_ = combined_pdf.createNLL(asimovdata,RooFit::ExternalConstraints(RooArgList(asimov_constraint_pdf)));

    	  RooRealVar *nllA_ =(RooRealVar*) NLLDiagonal(slist_,*dataAsimov, philist_,muA_);

	  tree->Branch("limit",&limit,"limit/D");
	  limit = getUpperLimit(nll_,nllA_,&r,0.95,doExpected,minRangeForLimit,maxRangeForLimit,stepsForLimit);
	  tree->Fill();
	  fout->cd();
	  globalLimitGraph->SetName("cls_vs_r");
	  globalLimitGraph->Write();
	}

	// End the things .....
	tree->Write();

	fout->WriteTObject(covar,"covar");
	fout->WriteTObject(corr,"correlation");
	fout->WriteTObject(data,"data");
	fout->WriteTObject(dataG,"dataG");
	fout->WriteTObject(bkg,"bkg");
	fout->WriteTObject(signal,"signal");
	fout->WriteTObject(can,"bestfit");
	fout->WriteTObject(grLL,"TwoDeltaNLL");
	fout->Close();
	std::cout << " .... Saved stuff to " << outname << std::endl;

//	if (verb) {
	 if (justCalcLimit) std::cout << "Upper Limit 95% " << limit << std::endl;
	 else std::cout << "RMIN = " << rMin << std::endl;
//	}

	return 0;
}
