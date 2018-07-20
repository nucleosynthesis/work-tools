int doMSSM=0;
int doTHDM=1;
int doXCHECK=1;

double gamma(double kV, double ku, double kd){
  
   
   double kglu2 = 1.04*ku*ku + 0.002*kd*kd - 0.038*ku*kd;
   double kgam2 = 1.59*kV*kV + 0.07*ku*ku - 0.67*kV*ku;
   double kZg2 = kgam2;
   double g = 0.58*kd*kd + 0.22*kV*kV + 0.08*kglu2 +0.06*kd*kd +0.026*kV*kV +0.029*ku*ku +0.0023*kgam2 +0.0015*kZg2 + 0.00025*kd*kd+0.00022*kd*kd;
   return TMath::Sqrt(g);
}

void getAngles(double cosbma, double tanbeta, double *beta, double *bma){

  *beta = TMath::ATan(tanbeta);
  *bma = TMath::ACos(cosbma);
  //*alpha = *beta - bma; 
}

void type1(double cosbma, double tanbeta, double *ldu, double *lvu, double *kuu){
   double sinbma = TMath::Sqrt(1-cosbma*cosbma);
   double tana = (tanbeta*cosbma-sinbma)/(cosbma+tanbeta*sinbma);

   double cosa = 1./(TMath::Sqrt(1+tana*tana));
   double sinb = tanbeta/(TMath::Sqrt(1+tanbeta*tanbeta));

   // get the sign of cos(a) .... sigh!
   double bma = TMath::ACos(cosbma); 
   double beta = TMath::ATan(tanbeta); 
   double alpha = beta-bma;
   double scos = TMath::Cos(alpha); 
   cosa *= scos/TMath::Abs(scos);

   // Type-1
   double kV = sinbma;
   double kf = cosa/sinb;

   // now the returns!
   *ldu = 1.; 
   *lvu = kV/kf;
   *kuu = kf*kf/gamma(kV,kf,kf);
   
}
void type1_ex(double cosbma, double tanbeta, double *ku, double *kd, double *kV){

   double sinbma = TMath::Sqrt(1-cosbma*cosbma);
   double tana = (tanbeta*cosbma-sinbma)/(cosbma+tanbeta*sinbma);
   double cosa = 1./(TMath::Sqrt(1+tana*tana));
   double sinb = tanbeta/(TMath::Sqrt(1+tanbeta*tanbeta));

   // get the sign of cos(a) .... sigh!
   double bma = TMath::ACos(cosbma); 
   double beta = TMath::ATan(tanbeta); 
   double alpha = beta-bma;
   double scos = TMath::Cos(alpha); 
   cosa *= scos/TMath::Abs(scos);

   // Type-1
   *kV = sinbma;
   *ku = cosa/sinb;
   *kd - cosa/sinb;

   
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
   double tana = (tanbeta*cosbma-sinbma)/(cosbma+tanbeta*sinbma);
   double cosa = 1./(TMath::Sqrt(1+tana*tana));
   double sinb = tanbeta/(TMath::Sqrt(1+tanbeta*tanbeta));

   // get the sign of cos(a) .... sigh!
   double bma = TMath::ACos(cosbma); 
   double beta = TMath::ATan(tanbeta); 
   double alpha = beta-bma;
   double scos = TMath::Cos(alpha); 
   cosa *= scos/TMath::Abs(scos);


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

void type2_ex(double cosbma, double tanbeta, double *ku, double *kd, double *kV){

   double sinbma = TMath::Sqrt(1-cosbma*cosbma);
   double tana = (tanbeta*cosbma-sinbma)/(cosbma+tanbeta*sinbma);
   double cosa = 1./(TMath::Sqrt(1+tana*tana));
   double sinb = tanbeta/(TMath::Sqrt(1+tanbeta*tanbeta));


   // get the sign of cos(a) .... sigh!
   double bma = TMath::ACos(cosbma); 
   double beta = TMath::ATan(tanbeta); 
   double alpha = beta-bma;
   double scos = TMath::Cos(alpha); 
   cosa *= scos/TMath::Abs(scos);


   double sina = cosa*tana;
   double cosb = (1./tanbeta)*sinb ;
   
   // Type-1
   *kV = sinbma;
   *ku = cosa/sinb;
   *kd = -1*sina/cosb;

}

/*
void MSSM(){
 return;
}
*/

double interp(double r1, double cl1, double r2, double cl2, double cl){
	double d = (cl2-cl1)/(r2-r1);
	return ((cl - cl1) + r1*d)/d;
}

double get_x(double r, double th, double offx){
 //return offx+r*TMath::Cos(th);
 return r;
}
double get_y(double r, double th, double offy){
 //return offy+r*TMath::Sin(th);
 return TMath::Tan(th);
}

TGraph *gr21Dspline_tanB(RooSplineND *spline, RooRealVar &ldu, RooRealVar &lVu, RooRealVar &kuu, int type, double minNLL, double fixcbma)
{
	TGraph *points = new TGraph();
	int pcounter = 0;

   	double Vldu, VlVu, Vkuu; // holders for the values

	
	for (double th=0.001; th<=10;th+=0.1){

		 double x = fixcbma;
		 double y = TMath::Tan(th);  // x irrelevant in grid search

		 if (type==1)type1(x, y, &Vldu, &VlVu, &Vkuu);
		 if (type==2)type2(x, y, &Vldu, &VlVu, &Vkuu);
          	 ldu.setVal(Vldu);
          	 lVu.setVal(VlVu);
          	 kuu.setVal(Vkuu);

	  	 val = 2*spline->getVal() - minNLL;
		 points->SetPoint(pcounter,val,y);
		 pcounter++;
	}
	points->GetYaxis()->SetTitle("tan(#beta)");
	points->GetXaxis()->SetTitle("-2#Delta Log(L)");
	return points;

}

TGraph * gr2contour(RooSplineND *spline, RooRealVar &ldu, RooRealVar &lVu, RooRealVar &kuu, int type, double level, double minNLL, double best_x, double best_y, double step_r, double step_th)
{

	TGraph *points = new TGraph();
	int pcounter = 0;

   	double Vldu, VlVu, Vkuu; // holders for the values

        // Define 0 as the +ve Y-axis
	std::cout << " Centered at (type) " << best_x << ", " << best_y << ", " << type << std::endl;
	std::cout << " Minimum assumed to be " << minNLL << std::endl;
	TGraph *thepoints = new TGraph();
	int pointcounter =0 ;

	//for (double th=0; th<2*TMath::Pi();th+=step_th){
	for (double th=0.001; th<=10;th+=step_th){
	//for (double th=5.; th<6.;th+=0.2){	

		double r_pre_level=-1;
		double val_pre_level=-1;

		bool iscontained=true;
		//double r=0.05;
		double r=-0.99;

		bool invertLogic=false;
		while (iscontained){

		 double x = get_x(r,th,best_x);
		 double y = get_y(r,th,best_y);

		 if (x > 1 || y > 10 || x < -1 || y < 0.0001 ){
			iscontained=false;
			break;
		 }

   		 // x = cos(b-a) and y=tanb
		 if (type==1)type1(x, y, &Vldu, &VlVu, &Vkuu);
		 if (type==2)type2(x, y, &Vldu, &VlVu, &Vkuu);
		 double val = 1000;
		 if ( Vldu < ldu.getMax() && Vldu > ldu.getMin() && VlVu < lVu.getMax() && VlVu > lVu.getMin() && Vkuu < kuu.getMax() && Vkuu > kuu.getMin() ){

          	   ldu.setVal(Vldu);
          	   lVu.setVal(VlVu);
          	   kuu.setVal(Vkuu);

	  	   val = 2*spline->getVal() - minNLL;
		 }

		 if ( (invertLogic && val<level) || ( (!invertLogic) && val>level) ){
			double ave_r = interp(r,val,r_pre_level,val_pre_level,level);  // Do a better interpolation later
			if (get_x(ave_r,th,best_x) > -0.89 && get_x(ave_r,th,best_x) < 0.89 && y>0.05 && y < 11){
			  points->SetPoint(pcounter,get_x(ave_r,th,best_x),get_y(ave_r,th,best_y));
			  pcounter++;
			  //break;
			  //std::cout << " Oh I found a cheeky point!  x, y=" << get_x(ave_r,th,best_x) << ", " << get_y(ave_r,th,best_y) << ", (ave_r,th, r,r_pre=)" << ave_r << ", " << th << " avarage from " << r << ", " <<  r_pre_level << " (value,val_pre) == " << val << ", " << val_pre_level <<  std::endl;
			}
			invertLogic=(!invertLogic);
		 //} else {
		 }
		 r_pre_level = r;
		 val_pre_level = val;
		 //}
		 thepoints->SetPoint(pointcounter,get_x(r,th,best_x),get_y(r,th,best_y));
		 pointcounter++;

		 r+=step_r;
		}
	}

	points->SetMarkerStyle(20);
	points->SetMarkerSize(0.5);

        thepoints->SetMarkerColor(kRed);
	//thepoints->Draw("AP");
	//points->Draw("apL");

	return points;
}
void makeLikelihoodRotation(std::string inname, std::string outname, double SMOOTH, bool isAsimov=false){

   gSystem->Load("libHiggsAnalysisCombinedLimit.so");
   //TFile *fi = TFile::Open("lduscan_neg_ext/3D/lduscan_neg_ext_3D.root");
   //TFile *fi = TFile::Open("lduscan_neg_ext_2/exp3D/lduscan_neg_ext_2_exp3D.root");
   TFile *fi = TFile::Open(inname.c_str());
   TTree *tree = (TTree*)fi->Get("limit");
   //TTree *tree = new TTree("tree_vals","tree_vals");  

   // ------------------------------ THIS IS WHERE WE BUILD THE SPLINE ------------------------ //
   // Create 2 Real-vars, one for each of the parameters of the spline 
   // The variables MUST be named the same as the corresponding branches in the tree
   //
   RooRealVar ldu("lambda_du","lambda_du",0.1,-2.5,2.5); 
   RooRealVar lVu("lambda_Vu","lambda_Vu",0.1,0,2.2);
   RooRealVar kuu("kappa_uu","kappa_uu",0.1,0,2.2);
   
   RooSplineND *spline = new RooSplineND("spline","spline",RooArgList(ldu,lVu,kuu),tree,"deltaNLL",SMOOTH,true,"deltaNLL >= 0 && deltaNLL < 500 && ( (TMath::Abs(quantileExpected)!=1 && TMath::Abs(quantileExpected)!=0) || (Entry$==0) )");
   // ----------------------------------------------------------------------------------------- //
   
   //TGraph *gr = spline->getGraph("x",0.1); // Return 1D graph. Will be a slice of the spline for fixed y generated at steps of 0.1
   fOut = new TFile(outname.c_str(),"RECREATE");

   // Plot the 2D spline 

   /*
   TGraph2D *gcvcf = new TGraph2D(); gcvcf->SetName("cvcf");
   TGraph2D *gcvcf_kuu = new TGraph2D(); gcvcf_kuu->SetName("cvcf_kuu");
   TGraph2D *gcvcf_lVu = new TGraph2D(); gcvcf_lVu->SetName("cvcf_lVu");
   */
   TGraph2D *type1_minscan = new TGraph2D(); 
   type1_minscan->SetName("type1_minscan");
   TGraph2D *type2_minscan = new TGraph2D(); 
   type2_minscan->SetName("type2_minscan");

   TGraph2D *gr_ldu 		= new TGraph2D(); gr_ldu->SetName("t1_ldu");
   TGraph2D *gr_lVu 		= new TGraph2D(); gr_lVu->SetName("t1_lVu");
   TGraph2D *gr_kuu 		= new TGraph2D(); gr_kuu->SetName("t1_kuu");
   TGraph2D *gr2_ldu		= new TGraph2D(); gr2_ldu->SetName("t2_ldu");
   TGraph2D *gr2_lVu 		= new TGraph2D(); gr2_lVu->SetName("t2_lVu");
   TGraph2D *gr2_kuu 		= new TGraph2D(); gr2_kuu->SetName("t2_kuu");

   TGraph2D *gr_ku 		= new TGraph2D(); gr_ku->SetName("t1_ku");
   TGraph2D *gr_kd 		= new TGraph2D(); gr_kd->SetName("t1_kd");
   TGraph2D *gr_kV 		= new TGraph2D(); gr_kV->SetName("t1_kV");

   TGraph2D *gr2_ku 		= new TGraph2D(); gr2_ku->SetName("t2_ku");
   TGraph2D *gr2_kd 		= new TGraph2D(); gr2_kd->SetName("t2_kd");
   TGraph2D *gr2_kV 		= new TGraph2D(); gr2_kV->SetName("t2_kV");

   TGraph2D *gr_beta		= new TGraph2D(); gr_beta->SetName("beta");
   TGraph2D *gr_bma		= new TGraph2D(); gr_bma->SetName("beta_minis_alpha");
   // check the values of the three parameters during the scan ?!


   double Vldu, VlVu, Vkuu; // holders for the values
   int pt1,pt2 = 0;

   double mint2 = 10000;
   double mint1 = 10000;
   double mint1_x = 10000;
   double mint1_y = 10000;
   double mint2_x = 10000;
   double mint2_y = 10000;

   double mint1_lVu = 10000;
   double mint1_ldu = 10000;
   double mint1_kuu = 10000;

   double mint2_lVu = 10000;
   double mint2_ldu = 10000;
   double mint2_kuu = 10000;

   int ccounter = 0;

   double Vku, Vkd, VkV; 

   TGraph2D *g_FFS = new TGraph2D(); g_FFS->SetName("ffs_ldu_1");
   int pt=0;
   for (double x=0.;x<=3.0;x+=0.05){
     for (double y=0.;y<=3.0;y+=0.05){
	ldu.setVal(1);
	lVu.setVal(y);
	kuu.setVal(x);
	double dnll2 = 2*spline->getVal();
	g_FFS->SetPoint(pt,x,y,dnll2);
	pt++;
     }
   }

   if (!isAsimov){

    double Vbma, Vbeta; 

    for (double cbma=-0.8;cbma<0.8;cbma+=0.01){
     for (double b=0.1;b<1.4;b+=0.05){
        double tanb = TMath::Tan(b);

	getAngles(cbma,tanb,&Vbeta,&Vbma);

	type1(cbma, tanb, &Vldu, &VlVu, &Vkuu);
	type1_ex(cbma, tanb, &Vku, &Vkd, &VkV);

	if (Vldu > ldu.getMax() || Vldu < ldu.getMin()) {
        	type1_minscan->SetPoint(ccounter,cbma,tanb,10);
	}
	if (VlVu > lVu.getMax() || VlVu < lVu.getMin()) {
        	type1_minscan->SetPoint(ccounter,cbma,tanb,10);
	}
	if (Vkuu > kuu.getMax() || Vkuu < kuu.getMin()) {
        	type1_minscan->SetPoint(ccounter,cbma,tanb,10);
	} else {
         ldu.setVal(Vldu);lVu.setVal(VlVu);kuu.setVal(Vkuu);
	 double dnll2 = 2*spline->getVal();
	 if (dnll2 < mint1) { 
		mint1_x = cbma;
		mint1_y = tanb;
		mint1 = dnll2;

		mint1_lVu = VlVu; 
		mint1_kuu = Vkuu;
		mint1_ldu = Vldu;
	 }
	 type1_minscan->SetPoint(ccounter,cbma,tanb,dnll2);
	}
	//std::cout << " Checking point cbma,tanb -> ldu, lVu, kuu == 2DeltaNLL " << cbma << ", " << tanb << " --> " << Vldu << ", " << VlVu << ", " << Vkuu << " == " << dnll2 << std::endl;
        gr_ldu->SetPoint(ccounter,cbma,tanb,Vldu);
        gr_lVu->SetPoint(ccounter,cbma,tanb,VlVu);
        gr_kuu->SetPoint(ccounter,cbma,tanb,Vkuu);

        gr_ku->SetPoint(ccounter,cbma,tanb,Vku);
        gr_kd->SetPoint(ccounter,cbma,tanb,Vkd);
        gr_kV->SetPoint(ccounter,cbma,tanb,VkV);

	
	type2(cbma, tanb, &Vldu, &VlVu, &Vkuu);
	type2_ex(cbma, tanb, &Vku, &Vkd, &VkV);

	if (Vldu > ldu.getMax() || Vldu < ldu.getMin()) {
        	type2_minscan->SetPoint(ccounter,cbma,tanb,10);
	}
	if (VlVu > lVu.getMax() || VlVu < lVu.getMin()) {
        	type2_minscan->SetPoint(ccounter,cbma,tanb,10);
	}
	if (Vkuu > kuu.getMax() || Vkuu < kuu.getMin()) {
        	type2_minscan->SetPoint(ccounter,cbma,tanb,10);
	} else {
         ldu.setVal(Vldu);lVu.setVal(VlVu);kuu.setVal(Vkuu);
	 double dnll2 = 2*spline->getVal();
	 if (dnll2 < mint2) {
		mint2_x = cbma;
		mint2_y = tanb;
		mint2 = dnll2;

		mint2_lVu = VlVu; 
		mint2_kuu = Vkuu;
		mint2_ldu = Vldu;
	 }
	 type2_minscan->SetPoint(ccounter,cbma,tanb,dnll2);
	}
        gr2_ldu->SetPoint(ccounter,cbma,tanb,Vldu);
        gr2_lVu->SetPoint(ccounter,cbma,tanb,VlVu);
        gr2_kuu->SetPoint(ccounter,cbma,tanb,Vkuu);

        gr2_ku->SetPoint(ccounter,cbma,tanb,Vku);
        gr2_kd->SetPoint(ccounter,cbma,tanb,Vkd);
        gr2_kV->SetPoint(ccounter,cbma,tanb,VkV);

	gr_beta->SetPoint(ccounter,cbma,tanb,Vbeta);
	gr_bma->SetPoint(ccounter,cbma,tanb,Vbma);

	ccounter++;
     }
    }
    std::cout << "T1 Minimum found at " << mint1_x << "," << mint1_y << "( or in lVu, kuu, ldu) = " << mint1_lVu << ", " << mint1_kuu << ", " << mint1_ldu  << ", val=" << mint1 << std::endl;
    std::cout << "T2 Minimum found at " << mint2_x << "," << mint2_y << "( or in lVu, kuu, ldu) = " << mint2_lVu << ", " << mint2_kuu << ", " << mint2_ldu  <<", val=" << mint2 << std::endl;
   }
   else { // Probably then use the Asimov
		
         ldu.setVal(1);lVu.setVal(1);kuu.setVal(1);
	 double dnll2 = 2*spline->getVal();
	 mint1 = dnll2;
	 mint2 = dnll2;	
   }


   
   TGraph *type1_0p1 = (TGraph*)gr21Dspline_tanB(spline, ldu, lVu, kuu, 1, mint1, 0.1);
   TGraph *type2_0p1 = (TGraph*)gr21Dspline_tanB(spline, ldu, lVu, kuu, 2, mint2, 0.1);


   type1_0p1->SetName("type1_cbma0p1");
   type2_0p1->SetName("type2_cbma0p1");
   type1_0p1->Write();
   type2_0p1->Write();

   TGraph * gr_type1 = (TGraph*)gr2contour(spline, ldu, lVu, kuu, 1, 5.99, mint1, 0, 1., 0.01, 0.001);
   TGraph * gr_type2 = (TGraph*)gr2contour(spline, ldu, lVu, kuu, 2, 5.99, mint2, 0, 1., 0.01, 0.001);

   gr_type1->SetName("type1");
   gr_type2->SetName("type2");
   gr_type1->Write();
   gr_type2->Write();

   //gr_type1->Draw("p"); 
   fOut->cd(); 


   type1_minscan->Write();
   type2_minscan->Write();

   gr_ldu->SetMinimum(-2.5);  gr_ldu->SetMaximum(2.5); 
   gr_lVu->SetMinimum(0)   ;  gr_lVu->SetMaximum(3); 
   gr_kuu->SetMinimum(0)   ;  gr_kuu->SetMaximum(3);

   gr2_ldu->SetMinimum(-2.5);  gr2_ldu->SetMaximum(2.5); 
   gr2_lVu->SetMinimum(0)   ;  gr2_lVu->SetMaximum(3); 
   gr2_kuu->SetMinimum(0)   ;  gr2_kuu->SetMaximum(3); 

   gr_ldu->Write(); gr_lVu->Write(); gr_kuu->Write();
   gr2_ldu->Write(); gr2_lVu->Write(); gr2_kuu->Write();

   gr_ku->Write(); 
   gr_kd->Write(); 
   gr_kV->Write(); 
      
   gr2_ku->Write();
   gr2_kd->Write();
   gr2_kV->Write();

   g_FFS->Write();

   gr_beta->Write();
   gr_bma->Write();

   std::cout << "Saved stuff to -> " << fOut->GetName() << std::endl; 
   fOut->Close();
}

