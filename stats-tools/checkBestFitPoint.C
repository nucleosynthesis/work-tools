// Quick Macro to make plots of the LH around the best fitted point
// This will load in a snapshot from MultiDimFit to make the "best fit'
// run in CINT
/*
#include "TROOT.h"
#include "TObject.h"
#include "TStyle.h"
#include "TCanvas.h"
#include "TPaveText.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TH1F.h"
#include "TF1.h"
#include "TAxis.h"
#include "TTree.h"
#include "TFile.h"
#include "TString.h"
#include "TMath.h"
#include "TMatrixDSym.h"
#include "TMatrixD.h"
#include "TVectorD.h"
#include "TIterator.h"

// RooFit includes
#include "RooCategory.h"
#include "RooRealVar.h"
#include "RooConstVar.h"
#include "RooFormulaVar.h"
#include "RooArgSet.h"
#include "RooArgList.h"
#include "RooAddPdf.h"
#include "RooCmdArg.h"

// RooStats includes
#include "RooWorkspace.h"

#include <pair>
#include <string>
#include <vector>
#include <map>
#include <iostream>
*/
// For LH Plots, n-sigma along x axis
using namespace std;
int npoints = 200;
int nsigma  = 1.;

RooAbsReal *nll;
RooWorkspace *w;
RooStats::ModelConfig *mc_s;
//TLatex *lat = new TLatex();
//lat->SetTextFont(42);
//lat->SetTextSize(0.03);
//lat->SetNDC();

TGraph *graphLH(std::string nuisname, double err,std::map<std::string,double> & fit_values ){

	w->loadSnapshot("MultiDimFit"); // SetTo BestFit values as start

	// Get The parameter we want 
	RooRealVar *nuis =(RooRealVar*) w->var(nuisname.c_str());
	double bf = nuis->getVal();
	double nll_0=2*nll->getVal();


	TGraph *gr = new TGraph(2*npoints+1);
	for (int i=-1*npoints;i<=npoints;i++){
		double vval = bf+err*( ((float)i)*nsigma/npoints);
		nuis->setVal(vval);
		double nll_v = 2*nll->getVal();
		if (nll_v<nll_0) std::cout << " WARNING --  Found -ve nll " << nuisname << " = " << vval << nll_v-nll_0 << std::endl; 
		gr->SetPoint(i+npoints,nuis->getVal(),nll_v-nll_0);
	}

	//gr->SetTitle("");
	gr->GetYaxis()->SetTitle("2*NLL - obs data");
	gr->GetYaxis()->SetTitleOffset(1.1);
	gr->GetXaxis()->SetTitleSize(0.035);
	gr->GetYaxis()->SetTitleSize(0.04);
	gr->GetXaxis()->SetTitle(nuisname.c_str());
	gr->SetLineColor(4);
	gr->SetLineWidth(2);
	gr->SetMarkerStyle(21);
	gr->SetMarkerSize(0.6);
	//gr->SetTitleSize(0.04);
	gr->SetTitle(Form("Best fit val = %.3f +/- %.3f ", bf, err ));
	std::cout << " Best fit param " << nuisname << " = " << bf << " +/- " << err <<  std::endl;

	//fit_values.insert(std::pair<const std::string,double>(nuisname,bf)) ;
	// Find the crossings 

 	//std::cout << " Constructed NLL for " << nuisname << std::endl;	
	return gr;
	
}

void checkBestFitPoint(std::string workspace,std::string output, bool runExpected=0){
	std::map<std::string,double>  fit_values ; 
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
	if (runExpected) {
	  data = (RooDataSet*) fw_->Get("toys/toy_asimov");
	}
	mc_s = (RooStats::ModelConfig*)w->genobj("ModelConfig");
	std::cout << "make nll"<<std::endl;
	nll = mc_s->GetPdf()->createNLL(
		*data,RooFit::Constrain(*mc_s->GetNuisanceParameters())
		,RooFit::Extended(mc_s->GetPdf()->canBeExtended()));
	RooArgSet *discreteParameters = (RooArgSet*)w->genobj("discreteParams");
	
	std::cout << "Prefit Discretes .... " << std::endl;
        if (discreteParameters != 0) {
          TIterator *dp = discreteParameters->createIterator();
          for (TObject *arg = dp->Next(); arg!=0;arg=dp->Next()) {
             RooCategory *cat = dynamic_cast<RooCategory*>(arg);
            //if (cat && !cat->isConstant()) {
             if (cat) {
		std::cout << cat->GetName() << ", " << cat->getIndex()<<std::endl;
             }
	  }
        }
	// Now get the best fit result
	//fd_ =  TFile::Open(fitFile.c_str());
	//RooFitResult *fit =(RooFitResult*)fd_->Get("fit_s");
	//RooArgSet fitargs = fit->floatParsFinal();
	
	//std::cout << "Got the best fit values" <<std::endl;		
	//w->saveSnapshot("bestfitall",fitargs,true);
	RooArgSet *allargs = (RooArgSet*) w->allVars();
	RooStats::RemoveConstantParameters(allargs);
	// Now make the plots!	
	TCanvas *c = new TCanvas("c","",600,600);
	c->SaveAs(Form("%s.pdf[",output.c_str()));
	
	TIterator* iter(allargs->createIterator());
        for (TObject *a = iter->Next(); a != 0; a = iter->Next()) {
                 RooRealVar *rrv = dynamic_cast<RooRealVar *>(a);      
                 std::string name = rrv->GetName();
		 double err = 0.5; // guess
		 if (rrv->getError()) err = rrv->getError();
		 TGraph *gr = graphLH(name,err, fit_values);
		 gr->Draw("ALP");
	 	 TLine line(gr->GetXaxis()->GetXmin(),1,gr->GetXaxis()->GetXmax(),1);
		 line.SetLineColor(2);
		 line.SetLineWidth(2);
		 c->SetGridy();
		 c->SetGridx();
		 line.Draw();
		 c->SaveAs(Form("%s.pdf[",output.c_str()));
	}
	c->SaveAs(Form("%s.pdf]",output.c_str()));
	// lets also look at the discrete parameters
	w->loadSnapshot("MultiDimFit"); // SetTo BestFit values as start
	std::cout << "Postfit Continuous .... " << std::endl;
	
//	for(std::map<std::string,double>::iterator  it_map = fit_values.begin();it_map!=fit_values.end();it++){
//	   std::cout <<  it_map->first << " = " << it_map->second << std::endl;
//	}

	std::cout << "Postfit Discrete .... " << std::endl;
        if (discreteParameters != 0) {
          TIterator *dp = discreteParameters->createIterator();
          for (TObject *arg = dp->Next(); arg!=0;arg=dp->Next()) {
             RooCategory *cat = dynamic_cast<RooCategory*>(arg);
            //if (cat && !cat->isConstant()) {
           if (cat) {
		std::cout << cat->GetName() << ", " << cat->getIndex()<<std::endl;
           }
          }
    	}
}
