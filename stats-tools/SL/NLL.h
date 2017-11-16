// ***********************************************************
// My own likelihood rather than use RooFit
// Original Author - Nicholas Wardle - Imperial College London 
// ***********************************************************
/* 
 * Builds Product of poissons * multivariate gaussian
 * Call diagonal version if you already diagonalized, otherwise pass covariance matrix if not
*/

RooRealVar *NLL(RooArgList &sums, TH1F &data, RooArgList &theta, RooArgList &means, TMatrixDSym &cov){
	int n = sums.getSize();
	
	RooArgList pois;

	for (int i=0;i<n;i++){
	  int d = data.GetBinContent(i+1);
	  RooAbsReal *s  = (RooAbsReal*)sums.at(i);
	  // [-d*log(s) + s ]
	  RooFormulaVar *p = new RooFormulaVar(Form("log_poisson_bin_%d_%s",i+1,data.GetName()),Form("-%d*TMath::Log(@0) + @0",d),RooArgList(*s));
	  pois.add(*p);
	}
	RooAddition *Poisson = new RooAddition(Form("log_Poisson_%s",data.GetName()),"my Poisson",pois);
	TMatrixDSym Vinv = cov.Invert();	

        // make the dtheta
	RooArgList dtheta;

	for (int i=0;i<n;i++){
	  RooFormulaVar *delta = new RooFormulaVar(Form("delta_theta_%d_%s",i+1,data.GetName()),"@0-@1",RooArgList(*(theta.at(i)), *(means.at(i))));
	  dtheta.add(*delta);
        }

	RooArgList constraint;
	for (int i=0;i<n;i++){
	  RooArgList columns;
	  for (int j=0;j<n;j++){
	    RooFormulaVar *Vx = new RooFormulaVar(Form("V_%d_%d_th_%d_%s",i+1,j+1,j+1,data.GetName()),Form("%g*@0",Vinv[i][j]),RooArgList(*(dtheta.at(j))));
	    columns.add(*Vx);
	  }
	  std::cout << std::endl;
	  RooAddition *add = new RooAddition(Form("add_%d_%s",i+1,data.GetName()),"",columns);
	  RooFormulaVar *row = new RooFormulaVar(Form("row_%d_%s",i+1,data.GetName()),"0.5*@0*@1",RooArgList(*(dtheta.at(i)),*add));
	  constraint.add(*row);
	}
	
	RooAddition *ConstTerm = new RooAddition(Form("log_constraint_%s",data.GetName()),"",constraint);
	RooAddition *ret = new RooAddition(Form("nll_%s",data.GetName()),"Final NLL summation",RooArgList(*Poisson,*ConstTerm));
	return (RooRealVar*) ret;
}


RooRealVar *NLLDiagonal(RooArgList &sums, TH1F &data, RooArgList &theta, RooArgList &means){
	int n = sums.getSize();
	RooArgList pois;
	for (int i=0;i<n;i++){
	  int d = data.GetBinContent(i+1);
	  RooAbsReal *s  = (RooAbsReal*)sums.at(i);
	  // [-d*log(s) + s ]
	  RooFormulaVar *p = new RooFormulaVar(Form("log_poisson_bin_%d_%s",i+1,data.GetName()),Form("-%d*TMath::Log(@0) + @0",d),RooArgList(*s));
	  pois.add(*p);
	}
	RooAddition *Poisson = new RooAddition(Form("log_poisson_%s",data.GetName()),"my Poisson",pois);

        // make the dtheta
	RooArgList dtheta;
	for (int i=0;i<n;i++){

	  RooFormulaVar *delta = new RooFormulaVar(Form("delta_phi_%d_%s",i+1,data.GetName()),"@0-@1",RooArgList(*(theta.at(i)), *(means.at(i))));
	  dtheta.add(*delta);
        }
	RooArgList constraint;
	for (int i=0;i<n;i++){
	  RooFormulaVar *row = new RooFormulaVar(Form("row_%d_%s",i+1,data.GetName()),"0.5*@0*@0",RooArgList(*(dtheta.at(i))));
	  constraint.add(*row);
	}
	RooAddition *ConstTerm = new RooAddition(Form("log_constraint_%s",data.GetName()),"",constraint);
	RooAddition *ret = new RooAddition(Form("nll_%s",data.GetName()),"Final NLL summation",RooArgList(*Poisson,*ConstTerm));

	return (RooRealVar*) ret;
}
