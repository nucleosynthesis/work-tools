//#include <typeinfo.h>
void addFlatNuisances(std::string fi){
  gSystem->Load("libHiggsAnalysisCombinedLimit.so");
  TFile *fin = TFile::Open(fi.c_str());
  RooWorkspace *wspace = (RooWorkspace*)fin->Get("w_hmumu");

  wspace->Print("");

  RooStats::ModelConfig *mc = (RooStats::ModelConfig*)wspace->genobj("ModelConfig");
  RooArgSet *nuis = (RooArgSet*) mc->GetNuisanceParameters();
  std::cout << "Before...." << std::endl;
  nuis->Print();
  
  RooRealVar *mgg = (RooRealVar*)wspace->var("mmm");
  // Get all of the "flat" nuisances to be added to the nusiances:
  RooArgSet pdfs = (RooArgSet) wspace->allVars();
  RooAbsReal *pdf;
  TIterator *it_pdf = pdfs.createIterator();
  

  while ( (pdf=(RooAbsReal*)it_pdf->Next()) ){
  	  if (!(std::string(pdf->GetName()).find("zmod") != std::string::npos )) {
  	   if (!(std::string(pdf->GetName()).find("__norm") != std::string::npos )) {
	   	continue;
	   }
	  }
	  pdf->Print();
	  RooArgSet* pdfpars = (RooArgSet*)pdf->getParameters(RooArgSet(*mgg));
	  pdfpars->Print();

	  std::string newname_pdf = (std::string("unconst_")+std::string(pdf->GetName()));
	  wspace->import(*pdf,RooFit::RenameVariable(pdf->GetName(),newname_pdf.c_str()));
	  pdf->SetName(newname_pdf.c_str());
	  nuis->add(*pdf);
  }
 
  wspace->var("MH")->setVal(125.0);
  std::cout << "After..." << std::endl;
  nuis->Print();
  mc->SetNuisanceParameters(*nuis);
  //RooWorkspace *wspace_new = wspace->Clone();
  //mc->SetWorkspace(*wspace_new);
  //wspace_new->import(*mc,true);

  TFile *finew = new TFile((std::string(fin->GetName())+std::string("_unconst.root")).c_str(),"RECREATE");
  //wspace_new->SetName("w");
  finew->WriteTObject(wspace);
  finew->Close();
}
