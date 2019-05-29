TH1F *target;
TH1F *source;

TRandom3 *rnd;
bool reWeight=false;

bool fitEffs = false; 

double weight(int nvtx){
  if (!reWeight) return 1.;
  if (nvtx>80 ) return 0;
  if (source->GetBinContent(nvtx) == 0 ) return 1.;
  return target->GetBinContent(nvtx)/source->GetBinContent(nvtx);
}

TF1 fit(TGraphAsymmErrors *efficiency, int p50, std::string title){
 
 TF1 fitFcn(Form("fit_fcn_%g",rnd->Uniform()),"[0]*0.5*(1+TMath::Erf((x-[1])/(sqrt([2]))))",0,500); 
 fitFcn.SetParameters( 0.937871,(double)p50,1378.23);
 TFitResultPtr fitRes_p = (TFitResultPtr)efficiency->Fit(fitFcn.GetName(),"ES0"); 
 TFitResult* fitRes = (TFitResult*)fitRes_p.Get();

 //fitFcn.SetName(Form("%s_fitFcn",efficiency->GetName()));
 fitFcn.SetLineColor(efficiency->GetLineColor());
 fitFcn.SetLineWidth(2);

 efficiency->GetXaxis()->SetTitle(title.c_str());
 efficiency->GetYaxis()->SetTitle("Efficiency");
 efficiency->GetYaxis()->SetRangeUser(0,1.2);
 
 return fitFcn;
}  


void makeTurnOnPlots(std::string infile){

	std::string MET       = "hfmet3x3";
	std::string METPUS    = "hfmet3x3pus";	// this is recalculated + PUS
	std::string METPUS3x3 = "hfmet3x3pus0";	// this is recalculated + Regional PUS

	std::string recomet = "recomet";

	std::string labels[3] = {"MET","MET + PUS","MET + PUS (0)"};
	//std::string title ="PF E_{T}^{miss} Type-1 Corrected (GeV)";
	std::string title ="Calo E_{T}^{miss} (GeV)";

	rnd = new TRandom3();
 	gStyle->SetOptFit(0);
 	gStyle->SetOptStat(0);

	std::string drawOpts = "pl";
	if (fitEffs) drawOpts =  "p";

	TFile *fin = TFile::Open(infile.c_str());
	TTree *tree = (TTree*)fin->Get("entries");

	source = new TH1F("nvtx","source",80,0,80);
	tree->Draw("nvtx>>nvtx");
	source->Scale(1./source->Integral());

	// Target from data
	TFile *pufile = TFile::Open("targetpu.root");
	target = (TH1F*) pufile->Get("targetpu");
	target->Scale(1./target->Integral());

	TH1F *weightedsource = new TH1F("weighted_nvtx","",80,0,80);
	tree->Draw("nvtx>>weighted_nvtx","weight(nvtx)");
	TCanvas *cvtx = new TCanvas(); cvtx->SetName("nvtx_weighted_MC");
	weightedsource->Scale(1./weightedsource->Integral());
	weightedsource->SetLineColor(4);
	weightedsource->SetLineWidth(2);
	target->SetLineWidth(2);
	weightedsource->Draw();
	target->Draw("same");
	source->SetLineColor(2);
	source->SetLineWidth(2);
	source->Draw("same");
	weightedsource->GetXaxis()->SetTitle("N Vertex");
	cvtx->SaveAs(Form("%s_weight_nvtx.pdf",infile.c_str()));

	const int netmseeds=5;
	double etm_seeds[netmseeds] = {20,40,60,80,120};

	double minMET = 0; 
	double maxMET = 300;
	int nxbins = 30;
	int nvtxbins[4] = {0,10,20,1000};

	// Keep Threshold = 60; 
	// We will also make a canvas for a certain threshold with different nvtx 
        int keepThreshold=20;	
	TGraphAsymmErrors* effs_keep[4];
	TF1 *funcs_keep[4];

	// Save the fit results? -> As a tree ?

	TFile *fout = new TFile(Form("fitres_%s",infile.c_str()),"RECREATE");
	TTree *trout = new TTree("fitres","fitres");
	
	double sigma_       = 0.;
	double mu_          = 0.;
	double sigmapus_    = 0.;
	double mupus_       = 0.;
	double sigmapus3x3_ = 0.;
	double mupus3x3_    = 0.;
	double seed_        = 0.;

	trout->Branch("sigma_vtx_weighted",&sigma_,"sigma_vtx_weighted/D");
	trout->Branch("mu_vtx_weighted",&mu_,"mu_vtx_weighted/D");
	trout->Branch("sigmapus_vtx_weighted",&sigmapus_,"sigmapus_vtx_weighted/D");
	trout->Branch("mupus_vtx_weighted",&mupus_,"mupus_vtx_weighted/D");
	trout->Branch("sigmapus3x3_vtx_weighted",&sigmapus3x3_,"sigmapus3x3_vtx_weighted/D");
	trout->Branch("mupus3x3_vtx_weighted",&mupus3x3_,"mupus3x3_vtx_weighted/D");

	trout->Branch("etmseed",&seed_,"seed/D");

	for (int vtxi=-1;vtxi<3;vtxi+=1){

	  TH1F *denominator = new TH1F(Form("denom_%d",vtxi),"denom",nxbins,minMET,maxMET);
	  denominator->Sumw2();
	  if (vtxi<0)  tree->Draw(Form("%s>>denom_%d",recomet.c_str(),vtxi),"weight(nvtx)");
	  else tree->Draw(Form("%s>>denom_%d",recomet.c_str(),vtxi),Form("nvtx>=%d && nvtx<%d",nvtxbins[vtxi],nvtxbins[vtxi+1]));

	  TGraphAsymmErrors* effs[netmseeds];
	  TF1*		     funcs[netmseeds];
	  TGraphAsymmErrors* effs_pus[netmseeds];
	  TF1*		     funcs_pus[netmseeds];
	  TGraphAsymmErrors* effs_pus3x3[netmseeds];
	  TF1*		     funcs_pus3x3[netmseeds];
	  

	  for (int eti=0;eti<netmseeds;eti++){

		TH1F *numerator = new TH1F(Form("num_%d_%d",eti,vtxi),"num",nxbins,minMET,maxMET);
		numerator->Sumw2();
		if (vtxi<0) tree->Draw(Form("%s>>num_%d_%d",recomet.c_str(),eti,vtxi),Form("weight(nvtx)*(%s>%g)",MET.c_str(),etm_seeds[eti]));
		else tree->Draw(Form("%s>>num_%d_%d",recomet.c_str(),eti,vtxi),Form("%s>%g && nvtx>=%d && nvtx<%d",MET.c_str(),etm_seeds[eti],nvtxbins[vtxi],nvtxbins[vtxi+1]));

		TH1F *numeratorpus = new TH1F(Form("num_p_%d_%d",eti,vtxi),"num",nxbins,minMET,maxMET);
		numeratorpus->Sumw2();
		if (vtxi<0) tree->Draw(Form("%s>>num_p_%d_%d",recomet.c_str(),eti,vtxi),Form("weight(nvtx)*(%s>%g)",METPUS.c_str(),etm_seeds[eti]));
		else tree->Draw(Form("%s>>num_p_%d_%d",recomet.c_str(),eti,vtxi),Form("%s>%g && nvtx>=%d && nvtx<%d",METPUS.c_str(),etm_seeds[eti],nvtxbins[vtxi],nvtxbins[vtxi+1]));

		TH1F *numeratorpus3x3 = new TH1F(Form("num_p3x3_%d_%d",eti,vtxi),"num",nxbins,minMET,maxMET);
		numeratorpus3x3->Sumw2();
		if (vtxi<0) tree->Draw(Form("%s>>num_p3x3_%d_%d",recomet.c_str(),eti,vtxi),Form("weight(nvtx)*(%s>%g)",METPUS3x3.c_str(),etm_seeds[eti]));
		else tree->Draw(Form("%s>>num_p3x3_%d_%d",recomet.c_str(),eti,vtxi),Form("%s>%g && nvtx>=%d && nvtx<%d",METPUS3x3.c_str(),etm_seeds[eti],nvtxbins[vtxi],nvtxbins[vtxi+1]));


		TGraphAsymmErrors *efficiency = new TGraphAsymmErrors();
		efficiency->Divide(numerator,denominator,"cl=0.683 b(1,1) mode");
		efficiency->SetLineColor(1);
		TF1 fitfcn(fit(efficiency,etm_seeds[eti],title));

		TGraphAsymmErrors *efficiencypus = new TGraphAsymmErrors();
		efficiencypus->Divide(numeratorpus,denominator,"cl=0.683 b(1,1) mode");
		efficiencypus->SetLineColor(2);
		efficiencypus->SetMarkerColor(2);
		TF1 fitfcnpus(fit(efficiencypus,etm_seeds[eti],title));

		TGraphAsymmErrors *efficiencypus3x3 = new TGraphAsymmErrors();
		efficiencypus3x3->Divide(numeratorpus3x3,denominator,"cl=0.683 b(1,1) mode");
		efficiencypus3x3->SetLineColor(2);
		efficiencypus3x3->SetMarkerColor(2);
		TF1 fitfcnpus3x3(fit(efficiencypus3x3,etm_seeds[eti],title));


 		TCanvas *can = new TCanvas();
 		efficiency->Draw(Form("a%s",drawOpts.c_str()));
		if (fitEffs) fitfcn.Draw("lsame");
		efficiencypus->Draw(Form("%ssame",drawOpts.c_str()));
		if (fitEffs) fitfcnpus.Draw("lsame");

		TLatex *latex = new TLatex(); latex->SetTextFont(42);
		latex->SetNDC();
		latex->DrawLatex(0.12,0.92,"#bf{CMS} #it{Simulation}");
		if (vtxi<0)  latex->DrawLatex(0.72,0.92,Form("L1 ETM > %g",etm_seeds[eti]));
		else latex->DrawLatex(0.42,0.92,Form("L1 ETM > %g, %d #leq Num VTX < %d",etm_seeds[eti],nvtxbins[vtxi],nvtxbins[vtxi+1]));
		TLine *line = new TLine(minMET,0.95,maxMET,0.95);
		line->SetLineStyle(2);
		line->Draw();

		TLegend *leg = new TLegend(0.6,0.2,0.89,0.4); 
		leg->SetTextFont(42);
		leg->SetFillColor(0);leg->SetBorderSize(0);
		leg->AddEntry(efficiency,"MET Raw","PL");
		leg->AddEntry(efficiencypus,"MET PUS","PL");
		leg->Draw();
		
 		//can->SaveAs(Form("%s_%g_vtx%d.pdf",infile.c_str(),etm_seeds[eti],vtxi));
 		//can->SaveAs(Form("%s_%g_vtx%d.png",infile.c_str(),etm_seeds[eti],vtxi));

		funcs[eti]  =new TF1(fitfcn);		
		effs[eti]   =new TGraphAsymmErrors(*efficiency);	
		funcs_pus[eti]     =new TF1(fitfcnpus);		
		effs_pus[eti]      =new TGraphAsymmErrors(*efficiencypus);	
		funcs_pus3x3[eti]  =new TF1(fitfcnpus3x3);		
		effs_pus3x3[eti]   =new TGraphAsymmErrors(*efficiencypus3x3);	
		
		if (etm_seeds[eti]==keepThreshold && vtxi>-1){
		  funcs_keep[vtxi]= new TF1(fitfcn);		
		  effs_keep[vtxi]=new TGraphAsymmErrors(*efficiency);	
		}

		if (vtxi<0){
		 seed_ = etm_seeds[eti];
		 mu_   = fitfcn.GetParameter(1);
		 mupus_       = fitfcnpus.GetParameter(1);
		 mupus3x3_    = fitfcnpus3x3.GetParameter(1);
		 sigma_       = fitfcn.GetParameter(2);
		 sigmapus_    = fitfcnpus.GetParameter(2);
		 sigmapus3x3_ = fitfcnpus3x3.GetParameter(2);
        	 trout->Fill();
		}

	}

	TLegend *legx = new TLegend(0.6,0.2,0.89,0.4); 
	legx->SetTextFont(42);
	legx->SetFillColor(0);legx->SetBorderSize(0);
 	TCanvas *canx = new TCanvas();

	for (int eti=0;eti<netmseeds;eti++){
		int color = eti+1; 
		if (color >= 5 ) color++;
		if (color >= 10 ) color++;
		funcs[eti]->SetLineColor(color);
	        effs[eti]->SetLineColor(color);
	        effs[eti]->SetMarkerColor(color);
 		effs[eti]->GetXaxis()->SetTitle(title.c_str());
 		effs[eti]->GetYaxis()->SetTitle("Efficiency");
 		effs[eti]->GetYaxis()->SetRangeUser(0,1.2);
		if (eti==0) effs[eti]->Draw(Form("a%s",drawOpts.c_str()));
		else effs[eti]->Draw(Form("%ssame",drawOpts.c_str()));
		if (fitEffs) funcs[eti]->Draw("lsame");
		legx->AddEntry(effs[eti],Form("L1 ETM > %g",etm_seeds[eti]),"L");
	}
	legx->Draw();
	TLatex *latex = new TLatex(); latex->SetTextFont(42);
	latex->SetNDC();
	if (vtxi<0) latex->DrawLatex(0.12,0.92,"#bf{CMS} #it{Simulation}");
	else latex->DrawLatex(0.12,0.92,Form("#bf{CMS} #it{Simulation},  %d #leq Num VTX < %d",nvtxbins[vtxi],nvtxbins[vtxi+1]));
 	canx->SaveAs(Form("%s_allthresh_vtx%d.png",infile.c_str(),vtxi));
 	canx->SaveAs(Form("%s_allthresh_vtx%d.pdf",infile.c_str(),vtxi));


	// For a given #nvtx selection, we can make a nice plot of MET, METPUS, METPUS3x3
	
	TLegend *legp = new TLegend(0.5,0.1,0.89,0.55); 
	legp->SetTextFont(42);
	legp->SetFillColor(0);legp->SetBorderSize(0);legp->SetNColumns(3);
 	TCanvas *canp = new TCanvas();
	for (int eti=0;eti<netmseeds;eti++){

		int color = eti+1; 
		if (color >= 5 ) color++;
		if (color >= 10 ) color++;
		funcs[eti]->SetLineColor(color);
	        effs[eti]->SetLineColor(color);
	        effs[eti]->SetMarkerColor(color);
	        effs[eti]->SetMarkerStyle(20);
 		effs[eti]->GetXaxis()->SetTitle(title.c_str());
 		effs[eti]->GetYaxis()->SetTitle("Efficiency");
 		effs[eti]->GetYaxis()->SetRangeUser(0,1.2);

		funcs_pus[eti]->SetLineColor(color);
		funcs_pus[eti]->SetLineStyle(2);
	        effs_pus[eti]->SetLineColor(color);
	        effs_pus[eti]->SetLineStyle(2);
	        effs_pus[eti]->SetMarkerColor(color);
	        effs_pus[eti]->SetMarkerStyle(21);

		funcs_pus3x3[eti]->SetLineColor(color);
		funcs_pus3x3[eti]->SetLineStyle(3);
	        effs_pus3x3[eti]->SetLineColor(color);
	        effs_pus3x3[eti]->SetLineStyle(3);
	        effs_pus3x3[eti]->SetMarkerColor(color);
	        effs_pus3x3[eti]->SetMarkerStyle(25);

		if (eti==0) effs[eti]->Draw(Form("a%s",drawOpts.c_str()));
		else effs[eti]->Draw(Form("%ssame",drawOpts.c_str()));
		if (fitEffs) funcs[eti]->Draw("lsame");
		effs_pus[eti]->Draw(Form("%ssame",drawOpts.c_str()));
		if (fitEffs) funcs_pus[eti]->Draw("lsame");
		effs_pus3x3[eti]->Draw(Form("%ssame",drawOpts.c_str()));
		if (fitEffs) funcs_pus3x3[eti]->Draw("lsame");
		legp->AddEntry(effs[eti],	Form("%s > %g",labels[0].c_str(),etm_seeds[eti]),"LP");
		legp->AddEntry(effs_pus[eti],	Form("%s > %g",labels[1].c_str(),etm_seeds[eti]),"LP");
		legp->AddEntry(effs_pus3x3[eti],Form("%s > %g",labels[2].c_str(),etm_seeds[eti]),"LP");


	}

	legp->Draw();
	TLatex *latexf = new TLatex(); latexf->SetTextFont(42);
	latexf->SetNDC();
	if (vtxi<0) latexf->DrawLatex(0.12,0.92,"#bf{CMS} #it{Simulation}");
	else latexf->DrawLatex(0.12,0.92,Form("#bf{CMS} #it{Simulation},  %d #leq Num VTX < %d",nvtxbins[vtxi],nvtxbins[vtxi+1]));
 	canp->SaveAs(Form("%s_comparePUS_allthresh_vtx%d.png",infile.c_str(),vtxi));
 	canp->SaveAs(Form("%s_comparePUS_allthresh_vtx%d.pdf",infile.c_str(),vtxi));
     }


     //Final One 
     TLegend *legx = new TLegend(0.6,0.2,0.89,0.4); 
     legx->SetTextFont(42);
     legx->SetFillColor(0);legx->SetBorderSize(0);
     TCanvas *canx = new TCanvas();
     for (int vtxi=0;vtxi<3;vtxi++){
	int color = vtxi+1; 
	if (color >= 5 ) color++;
	if (color >= 10 ) color++;
	funcs_keep[vtxi]->SetLineColor(color);
	effs_keep[vtxi]->SetLineColor(color);
	effs_keep[vtxi]->SetMarkerColor(color);
 	effs_keep[vtxi]->GetXaxis()->SetTitle(title.c_str());
 	effs_keep[vtxi]->GetYaxis()->SetTitle("Efficiency");
 	effs_keep[vtxi]->GetYaxis()->SetRangeUser(0,1.2);
	if (vtxi==0) effs_keep[vtxi]->Draw("ap");
	else effs_keep[vtxi]->Draw("psame");
	funcs_keep[vtxi]->Draw("lsame");
	legx->AddEntry(effs_keep[vtxi], Form("%d #leq Num VTX < %d",nvtxbins[vtxi],nvtxbins[vtxi+1]),"L");
     }
     legx->Draw();
     TLatex *latex = new TLatex(); latex->SetTextFont(42);
     latex->SetNDC();
     latex->DrawLatex(0.12,0.92,Form("#bf{CMS} #it{Simulation},  L1 ETM > %d",keepThreshold));
     canx->SaveAs(Form("%s_keepthresh_allvtx.png",infile.c_str()));
     canx->SaveAs(Form("%s_keepthresh_allvtx.pdf",infile.c_str()));

     fout->cd();
     trout->Write();
     fout->Close();
}
