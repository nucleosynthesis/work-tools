void printCats(std::string finame, bool loadSnap){
  gSystem->Load("libHiggsAnalysisCombinedLimit");
  TFile *fi = TFile::Open(finame.c_str());
  RooWorkspace *w = (RooWorkspace*)fi->Get("w");
  if (loadSnap) w->loadSnapshot("MultiDimFit");
  RooFIter iter = w->allCats().fwdIterator();
	RooAbsArg* arg;
	while ((arg = iter.next())) {
		//if (arg->IsA() == RooFormulaVar::Class()) {
		if (std::string(arg->GetName()).find("pdfindex")!=std::string::npos){
			//cout << arg->GetName() << endl;
			RooCategory *var = dynamic_cast<RooCategory*>(arg);
			var->Print("");
		}
	}
}
