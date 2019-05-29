void cloneAndImportData(){
  ///gSystem->Load("$CMSSW_BASE/lib/$SCRAM_ARCH/libHiggsAnalysisCombinedLimit.so");
  gSystem->Load("libHiggsAnalysisCombinedLimit");

  //RooWorkspace *wTemplate_toy = wTemplate->Clone();
  TFile *fTemplate 	  	= TFile::Open("cms_combined_card.root");
  RooWorkspace *wTemplate      = (RooWorkspace*)fTemplate->Get("w");
  RooArgSet argsTemplate_toy  = (RooArgSet) wTemplate->allVars(); 
  RooArgSet catsTemplate_toy  = (RooArgSet) wTemplate->allCats();
  RooStats::ModelConfig *mc = (RooStats::ModelConfig*)  wTemplate->genobj("ModelConfig");
  argsTemplate_toy.Print();
  catsTemplate_toy.Print();

  TFile *fToy     = TFile::Open("higgsCombineTest.GenerateOnly.mH120.123456.root");
  //argsTemplate_toy->assignValueOnly(*argsToy);
  //catsTemplate_toy->assignFast(*catsToy);
  //setCategories(catsTemplate_toy,catsToy);

  RooDataSet *dataToy   = (RooDataSet*)fToy->Get("toys/toy_1");
  dataToy->SetName("toy_1");

  TFile *fout_toy = new TFile("hmm.technical.toy.root","RECREATE");
  RooWorkspace  *wNew = new RooWorkspace("w_hmumu","w_hmumu");

  wNew->import(*dataToy);
  wNew->import(argsTemplate_toy);
  wNew->import(catsTemplate_toy);

  RooStats::ModelConfig *mcN = new RooStats::ModelConfig("ModelConfig",wNew);
  mcN->SetParametersOfInterest(*(mc->GetParametersOfInterest()));
  mcN->SetNuisanceParameters(*(mc->GetNuisanceParameters()));
  mcN->SetObservables(*(mc->GetObservables()));
  mcN->SetGlobalObservables(*(mc->GetGlobalObservables()));
  mcN->SetPdf(*(mc->GetPdf()));

  wNew->import(*mcN);

  fout_toy->WriteTObject(wNew);
  fout_toy->Close();
  fTemplate->Close();


}
