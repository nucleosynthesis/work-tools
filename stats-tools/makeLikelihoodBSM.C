int doMSSM=1;
int doTHDM=1;
int doXCHECK=1;

double gamma(double kV, double ku, double kd){
  
   
   double kglu2 = 1.06*ku*ku + 0.01*kd*kd - 0.07*ku*kd;
   double kgam2 = 1.59*kV*kV + 0.07*ku*ku - 0.66*kV*ku;
   double kZg2 = kgam2;
   double g = 0.57*kd*kd + 0.22*kV*kV + 0.09*kglu2 +0.06*kd*kd +0.03*kV*kV +0.03*ku*ku +0.0023*kgam2 +0.0016*kZg2 + 0.0001*kd*kd+0.00022*kd*kd;
   return TMath::Sqrt(g);
}

void type1(double cosbma, double tanbeta, double *ldu, double *lvu, double *kuu){
   double sinbma = TMath::Sqrt(1-cosbma*cosbma);
   double tana = (tanbeta*cosbma-sinbma)/(cosbma-tanbeta*sinbma);
   double cosa = 1./(TMath::Sqrt(1+tana*tana));
   double sinb = tanbeta/(TMath::Sqrt(1+tanbeta*tanbeta));

   // Type-1
   double kV = sinbma;
   double kf = cosa/sinb;

   // now the returns!
   *ldu = 1.; 
   *lvu = kV/kf;
   *kuu = kf*kf/gamma(kV,kf,kf);
   
}

void MSSM(double mA, double tanb, double *ldu, double *lvu, double *kuu){

  double mZ = 91.0;
  double mh = 125.09;
  double su_d = TMath::Sqrt(1+  ( ((mA*mA)+(mZ*mZ))*((mA*mA)+(mZ*mZ))*tanb*tanb ) / (( (mZ*mZ) + (mA*mA*tanb*tanb) - (mh*mh)*(1+tanb*tanb) )*( (mZ*mZ) + (mA*mA*tanb*tanb) - (mh*mh)*(1+tanb*tanb) )) );
  double su = 1./su_d;

  double sd = su*( ((mA*mA)+(mZ*mZ))*tanb ) / ((mZ*mZ) + (mA*mA*tanb*tanb) - mh*mh*(1+tanb*tanb)); 

  // MSSM Stylee
  double tanb2s = TMath::Sqrt(1+(tanb*tanb));
  double kV = (sd+(tanb*su))/tanb2s;
  double ku = su*tanb2s/tanb;
  double kd = sd*tanb2s;

  //double G = gamma(kV,ku,kd);
//  std::cout << mA << ", " << tanb <<  std::endl;
//  std::cout << kV << ", " << ku << ", " << kd << ", " << std::endl;
//  std::cout << gamma(kV,ku,kd) << std::endl;
  *ldu = kd/ku; 
  *lvu = kV/ku;
  *kuu = ku*ku/gamma(kV,ku,kd);  
}

void type2(double cosbma, double tanbeta, double *ldu, double *lvu, double *kuu){

   double sinbma = TMath::Sqrt(1-cosbma*cosbma);
   double tana = (tanbeta*cosbma-sinbma)/(cosbma-tanbeta*sinbma);
   double cosa = 1./(TMath::Sqrt(1+tana*tana));
   double sinb = tanbeta/(TMath::Sqrt(1+tanbeta*tanbeta));

   double sina = cosa*tana;
   double cosb = (1./tanbeta)*sinb ;
   
   // Type-1
   double kV = sinbma;
   double ku = cosa/sinb;
   double kd = -1*sina/cosb;

   // now the returns!
   *ldu = kd/ku; 
   *lvu = kV/ku;
   *kuu = ku*ku/gamma(kV,ku,kd);  
}

/*
void MSSM(){
 return;
}
*/

void makeLikelihood(){

   gSystem->Load("libHiggsAnalysisCombinedLimit.so");
   //TFile *fi = TFile::Open("lduscan_neg_ext/3D/lduscan_neg_ext_3D.root");
   TFile *fi = TFile::Open("allthepoints.root");
   TTree *tree = (TTree*)fi->Get("limit");
   //TTree *tree = new TTree("tree_vals","tree_vals");  

   // ------------------------------ THIS IS WHERE WE BUILD THE SPLINE ------------------------ //
   // Create 2 Real-vars, one for each of the parameters of the spline 
   // The variables MUST be named the same as the corresponding branches in the tree
   RooRealVar ldu("lambda_du","lambda_du",0.1,-2.5,2.5); 
   RooRealVar lVu("lambda_Vu","lambda_Vu",0.1,0,3);
   RooRealVar kuu("kappa_uu","kappa_uu",0.1,0,3);
   
   RooSplineND *spline = new RooSplineND("spline","spline",RooArgList(ldu,lVu,kuu),tree,"deltaNLL",1.,true,"deltaNLL<1000 && TMath::Abs(quantileExpected)!=1 && TMath::Abs(quantileExpected)!=0");
   // ----------------------------------------------------------------------------------------- //
   
   //TGraph *gr = spline->getGraph("x",0.1); // Return 1D graph. Will be a slice of the spline for fixed y generated at steps of 0.1
   fOut = new TFile("outplots-2hdm-neg-fine-mssm-final-try2.root","RECREATE");
   // Plot the 2D spline 
   TGraph2D *gr  		= new TGraph2D();  gr->SetName("type1");
   TGraph2D *gr2 		= new TGraph2D();  gr2->SetName("type2");
   TGraph2D *gr_ldu 		= new TGraph2D(); gr_ldu->SetName("ldu");
   TGraph2D *gr_lVu 		= new TGraph2D(); gr_lVu->SetName("lVu");
   TGraph2D *gr_kuu 		= new TGraph2D(); gr_kuu->SetName("kuu");
   TGraph2D *gr2_ldu		= new TGraph2D(); gr2_ldu->SetName("ldu_2");
   TGraph2D *gr2_lVu 		= new TGraph2D(); gr2_lVu->SetName("lVu_2");
   TGraph2D *gr2_kuu 		= new TGraph2D(); gr2_kuu->SetName("kuu_2");
   TGraph2D *gr_t1_lVu_V_kuu    = new TGraph2D(); gr_t1_lVu_V_kuu->SetName("t1_lVu_V_kuu");

   TGraph2D *gr_mssm_ldu 	= new TGraph2D(); gr_mssm_ldu->SetName("mssm_ldu");
   TGraph2D *gr_mssm_lVu 	= new TGraph2D(); gr_mssm_lVu->SetName("mssm_lVu");
   TGraph2D *gr_mssm_kuu 	= new TGraph2D(); gr_mssm_kuu->SetName("mssm_kuu");

   TGraph2D *g_FFS = new TGraph2D(); g_FFS->SetName("ffs_kuu1");
   double x,y,z;
   double mintF = 10000;
   int pt=0 ;
   /*
   for (double x=-1.6;x<=1.6;x+=0.05){
     for (double y=0.5;y<=1.5;y+=0.05){
	ldu.setVal(x);
	lVu.setVal(y);
	kuu.setVal(1);
	double dnll2 = 2*spline->getVal();
	if (dnll2 < mintF) mintF = dnll2;
	g_FFS->SetPoint(pt,x,y,dnll2);
	pt++;
     }
   }
   */

   TGraph2D *gcvcf = new TGraph2D(); gcvcf->SetName("cvcf");
   TGraph2D *gcvcf_kuu = new TGraph2D(); gcvcf_kuu->SetName("cvcf_kuu");
   TGraph2D *gcvcf_lVu = new TGraph2D(); gcvcf_lVu->SetName("cvcf_lVu");
   double mintkvkf = 10000;
   int pt=0 ;
   if (doXCHECK){
   // Sanity check, for ldu = 1, we should resolve kv kf ?
   //
   for (double cv=0.5;cv<=1.4;cv+=0.05){
     for (double cf=0.3;cf<=1.7;cf+=0.05){
	ldu.setVal(1.);
	lVu.setVal(cv/cf);
	kuu.setVal(cf*cf/gamma(cv,cf,cf));
	double dnll2 = 2*spline->getVal();
	if (dnll2 < mintkvkf) mintkvkf = dnll2;
	gcvcf->SetPoint(pt,cv,cf,dnll2);
	gcvcf_lVu->SetPoint(pt,cv,cf,lVu.getVal());
	gcvcf_kuu->SetPoint(pt,cv,cf,kuu.getVal());
	pt++;
     }
   }
   std::cout << " Min cV-cF = " << mintkvkf << std::endl;
   for (int p=0;p<gcvcf->GetN();p++){
        double z = (gcvcf->GetZ())[p] - mintkvkf;
        double x = (gcvcf->GetX())[p];
        double y = (gcvcf->GetY())[p];
	gcvcf->SetPoint(p,x,y,z);
   }
   }


   double Vldu, VlVu, Vkuu;

   int pt = 0;
   double mint2 = 10000;
   double mint1 = 10000;

   if (doTHDM){
   for (double scbma=-1;scbma<1;scbma+=0.01){
     for (double b=0.01;b<1.45;b+=0.01){
        double tanb = TMath::Tan(b);
     	if (tanb>1. ) b+=0.05;
	double cbma;
	if (scbma < 0) cbma = -1*scbma*scbma;
	else cbma = scbma*scbma;
	// Type 1 
	type1(cbma, tanb, &Vldu, &VlVu, &Vkuu);
	if (Vldu > ldu.getMax() || Vldu < ldu.getMin()) {
        	gr->SetPoint(pt,cbma,tanb,10);
	}
	if (VlVu > lVu.getMax() || VlVu < lVu.getMin()) {
        	gr->SetPoint(pt,cbma,tanb,10);
	}
	if (Vkuu > kuu.getMax() || Vkuu < kuu.getMin()) {
        	gr->SetPoint(pt,cbma,tanb,10);
	} else {
          ldu.setVal(Vldu);
          lVu.setVal(VlVu);
          kuu.setVal(Vkuu);
	  double dnll2 = 2*spline->getVal();
	  //std::cout << " pt, cbma, tanb , 2xdeltaNLL " << pt << ", " << cbma << ", " << tanb << ", " << dnll2  << std::endl;
	  if (dnll2 < mint1) mint1 = dnll2;
          gr->SetPoint(pt,cbma,tanb,dnll2);
	}
        gr_ldu->SetPoint(pt,cbma,tanb,Vldu);
        gr_lVu->SetPoint(pt,cbma,tanb,VlVu);
        gr_kuu->SetPoint(pt,cbma,tanb,Vkuu);
	gr_t1_lVu_V_kuu->SetPoint(pt,VlVu,Vkuu,dnll2);
	// Type 2 
	type2(cbma, tanb, &Vldu, &VlVu, &Vkuu);
	if (Vldu > ldu.getMax() || Vldu < ldu.getMin()) {
        	gr2->SetPoint(pt,cbma,tanb,10);
	}
	if (VlVu > lVu.getMax() || VlVu < lVu.getMin()) {
        	gr2->SetPoint(pt,cbma,tanb,10);
	}
	if (Vkuu > kuu.getMax() || Vkuu < kuu.getMin()) {
        	gr2->SetPoint(pt,cbma,tanb,10);
	} else {
          ldu.setVal(Vldu);
          lVu.setVal(VlVu);
          kuu.setVal(Vkuu);
	  double dnll2 = 2*spline->getVal();
	  //std::cout << " pt, cbma, tanb , 2xdeltaNLL " << pt << ", " << cbma << ", " << tanb << ", " << dnll2  << std::endl;
	  if (dnll2 < mint2) mint2 = dnll2;
          gr2->SetPoint(pt,cbma,tanb,dnll2);
	}
	// Fill variables too 
        gr2_ldu->SetPoint(pt,cbma,tanb,Vldu);
        gr2_lVu->SetPoint(pt,cbma,tanb,VlVu);
        gr2_kuu->SetPoint(pt,cbma,tanb,Vkuu);

        pt++;
     }
   }


   std::cout << " T2 minimum 2xdeltaNLL "  << mint2  << std::endl;
   // Need to re-normalise deltaNLL for the type-2 histogram 
   for (int p=0;p<gr2->GetN();p++){
        z = (gr2->GetZ())[p] - mint2;
        x = (gr2->GetX())[p];
        y = (gr2->GetY())[p];
	gr2->SetPoint(p,x,y,z);

        z = (gr->GetZ())[p] - mint1;
        x = (gr->GetX())[p];
        y = (gr->GetY())[p];
	gr->SetPoint(p,x,y,z);
   }
   }


   // MSSM Plot 
   TGraph2D *gr_mssm    = new TGraph2D(); gr_mssm->SetName("mssm");
   
   
   int pt = 0;
   double minmssm = 10000;
   if (doMSSM){
   for (double mA=200;mA<=550;mA+=10){
     for (double b=0.1;b<1.4;b+=0.02){
        double tanb = TMath::Tan(b);
     	if (tanb >10.) b+=0.05;
	// MSSM
	MSSM(mA, tanb, &Vldu, &VlVu, &Vkuu);
	std::cout << " pt, mA, tanb, ldu, lvu, kuu = " << pt << ", " << mA << ", " << tanb << ", " << Vldu << ", " << VlVu << ", " << Vkuu << std::endl;
	if (Vldu > ldu.getMax() || Vldu < ldu.getMin()) {
        	gr_mssm->SetPoint(pt,mA,tanb,10);
	}
	if (VlVu > lVu.getMax() || VlVu < lVu.getMin()) {
        	gr_mssm->SetPoint(pt,mA,tanb,10);
	}
	if (Vkuu > kuu.getMax() || Vkuu < kuu.getMin()) {
        	gr_mssm->SetPoint(pt,mA,tanb,10);
	} else {
	  //std::cout << " pt, mA, tanb, ldu, lvu, kuu = " << pt << ", " << mA << ", " << tanb << ", " << Vldu << ", " << VlVu << ", " << Vkuu << std::endl;
          ldu.setVal(Vldu);
          lVu.setVal(VlVu);
          kuu.setVal(Vkuu);
	  double dnll2 = 2*spline->getVal();
//	  std::cout << " pt, mA, tanb, ldu, lvu, kuu = " << pt << ", " << mA << ", " << tanb << ", " << Vldu << ", " << VlVu << ", " << Vkuu << ", "<<dnll2 <<std::endl;
	  if (dnll2 < minmssm) minmssm = dnll2;
          gr_mssm->SetPoint(pt,mA,tanb,dnll2);
	}
	gr_mssm_ldu->SetPoint(pt,mA,tanb,Vldu);
	gr_mssm_lVu->SetPoint(pt,mA,tanb,VlVu);
	gr_mssm_kuu->SetPoint(pt,mA,tanb,Vkuu);

        pt++;
     }
   }

   for (int p=0;p<gr_mssm->GetN();p++){
        z = (gr_mssm->GetZ())[p] - minmssm;
        x = (gr_mssm->GetX())[p];
        y = (gr_mssm->GetY())[p];
	gr_mssm->SetPoint(p,x,y,z);

   }
   }


  gr->SetMaximum(10);   		
  gr2->SetMaximum(10);  		
  gr_ldu->SetMaximum(10);  	
  gr_lVu->SetMaximum(10);  		
  gr_kuu->SetMaximum(10);  		
  gr2_ldu->SetMaximum(10); gr2_ldu->SetMinimum(-10);		
  gr2_lVu->SetMaximum(10);  		
  gr2_kuu->SetMaximum(10);  		
  gr_t1_lVu_V_kuu->SetMaximum(10);   
  gr_mssm->SetMaximum(10);   
  gr_mssm_ldu->SetMaximum(10);   gr_mssm_ldu->SetMinimum(-10); 
  gr_mssm_lVu->SetMaximum(10);
  gr_mssm_kuu->SetMaximum(10);
  gcvcf->SetMaximum(10);
//   TH2F *h = (TH2F*)gr->GetHistogram(); h->SetName("h_type1"); h->SetMaximum(10);
//   TH2F *h2 = (TH2F*)gr2->GetHistogram(); h2->SetName("h_type2"); h2->SetMaximum(10);
//   TH2F *hmssm = (TH2F*)gr_mssm->GetHistogram(); hmssm->SetName("h_mssm"); hmssm->SetMaximum(10);
//   TH2F *hldu = (TH2F*)gr_ldu->GetHistogram(); hldu->SetName("h_ldu"); hldu->SetMaximum(10);
//   TH2F *hlVu = (TH2F*)gr_lVu->GetHistogram(); hlVu->SetName("h_lVu"); hlVu->SetMaximum(10);
//   TH2F *hkuu = (TH2F*)gr_kuu->GetHistogram(); hkuu->SetName("h_kuu"); hkuu->SetMaximum(10);
//   TH2F *h2ldu = (TH2F*)gr2_ldu->GetHistogram(); h2ldu->SetName("h2_ldu"); h2ldu->SetMaximum(10);
//   TH2F *h2lVu = (TH2F*)gr2_lVu->GetHistogram(); h2lVu->SetName("h2_lVu"); h2lVu->SetMaximum(10);
//   TH2F *h2kuu = (TH2F*)gr2_kuu->GetHistogram(); h2kuu->SetName("h2_kuu"); h2kuu->SetMaximum(10);
//   TH2F *ht1_lVu_V_kuu = (TH2F*) gr_t1_lVu_V_kuu->GetHistogram(); ht1_lVu_V_kuu->SetName("h2_t1_lVu_V_kuu"); ht1_lVu_V_kuu->SetMaximum(10);

   fOut->cd(); 
   gr->Write(); gr2->Write(); 
   gr_ldu->Write(); gr_lVu->Write(); gr_kuu->Write();
   gr2_ldu->Write(); gr2_lVu->Write(); gr2_kuu->Write();
   gr_t1_lVu_V_kuu->Write();
   gr_mssm->Write();
   gcvcf->Write();
   gcvcf_kuu->Write();
   gcvcf_lVu->Write();
   gr_mssm_ldu->Write();
   gr_mssm_lVu->Write();
   gr_mssm_kuu->Write();
   g_FFS->Write();
   
   std::cout << "Saved stuff to -> " << fOut->GetName() << std::endl; 
   fOut->Close();
}

