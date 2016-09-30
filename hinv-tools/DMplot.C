bool isPrelim=false;

double const Mn = 0.93895;
double const Width_SM = 0.00407;
double const v = 174;
double const CV = 1e-36;
/*FIXME*/
double const CLval=90;
double const BRinv = 0.20;

//double const CLval=95;
//double const BRinv = 0.58;

double const Mh = 125;
int const k = 2;
int const numb = Mh*5*k;

double scalar(double *x, double fn)
{
    if(1 < 2*x[0]/Mh) return 0;
    double c1 = (Width_SM*BRinv)/(1.-BRinv);
    double beta = sqrt(1-4*pow(x[0]/Mh,2));
    double c2 = 4*c1*pow(Mn,4)*fn*fn;
    c2 /= v*v*beta*pow(Mh,3)*(x[0]+Mn)*(x[0]+Mn);
    return CV*0.3894*c2*1.0e+9;
}

double fermion(double *x, double fn)
{
    if(1 < 2*x[0]/Mh) return 0;
    double c1 = (Width_SM*BRinv)/(1.-BRinv);
    double beta = sqrt(1-4*pow(x[0]/Mh,2));
    double c2 = c1*8*pow(x[0]*Mn*fn,2)*Mn*Mn;
    c2 /= v*v*pow(beta,3)*pow(Mh,5)*(x[0]+Mn)*(x[0]+Mn);
    return CV*0.3894*c2*1.0e+9;
}

TGraph *MakeGraph(int Type, double fn)
{

    Double_t x[numb], y[numb];
    Int_t n = numb;
    for (Int_t i=0; i<n; i++) {
        x[i] = i*0.1*1/k;
        if(Type == 0) 	y[i] = scalar(&x[i], fn);
        else if (Type == 1)  y[i] = fermion(&x[i], fn);
        else 	         y[i] = 0;
    }
    TGraph *gr = new TGraph(n,x,y);
    gr->GetXaxis()->SetLimits(1,1000);
    //gr->GetXaxis()->SetLimits(5,100000);
    return gr;
}
void DMplot()
{

    TCanvas *canv = new TCanvas("canv", "limits canvas", 800., 680.);
	gStyle->SetCanvasDefH(600); //Height of canvas
	gStyle->SetCanvasDefW(640); //Width of canvas
	gStyle->SetCanvasDefX(0);   //POsition on screen
	gStyle->SetCanvasDefY(0);

	gStyle->SetPadLeftMargin(0.14);//0.16);
	gStyle->SetPadRightMargin(0.165);//0.02);
	gStyle->SetPadTopMargin(0.085);//0.02);
	gStyle->SetPadBottomMargin(0.12);//0.02);

	  // For g axis titles:
	gStyle->SetTitleColor(1, "XYZ");
	gStyle->SetTitleFont(42, "XYZ");
	gStyle->SetTitleSize(0.045, "Z");
	gStyle->SetTitleSize(0.055, "XY");
	gStyle->SetTitleXOffset(1.0);//0.9);
	gStyle->SetTitleYOffset(1.15); // => 1.15 if exponents

	// For g axis labels:
	gStyle->SetLabelColor(1, "XYZ");
	gStyle->SetLabelFont(42, "XYZ");
	gStyle->SetLabelOffset(0.007, "XYZ");
	gStyle->SetLabelSize(0.04, "XYZ");

	// Legends
	gStyle->SetLegendBorderSize(0);
	gStyle->SetLegendFillColor(kWhite);
	gStyle->SetLegendFont(42);
    TPad* t1d = new TPad();
    t1d = new TPad("t1d","t1d", 0.0, 0.0, 1.0, 1.0);
    t1d->Draw();
    t1d->SetTicky();
    t1d->SetTickx();
    t1d->SetRightMargin(0.03);
    t1d->cd();

    //t1d->SetGridx(1);
    //t1d->SetGridy(1);
    t1d->SetLogy();
    t1d->SetLogx();

    //double const fn = 0.629;//0.326;
    TGraph *h_scalar_min = MakeGraph(0,0.260);
    TGraph *h_scalar_lat = MakeGraph(0,0.326);
    TGraph *h_scalar_max = MakeGraph(0,0.629);
    TGraph *h_fermion_min = MakeGraph(1,0.260);
    TGraph *h_fermion_lat = MakeGraph(1,0.326);
    TGraph *h_fermion_max = MakeGraph(1,0.629);

//////////////////////////////////////////////////

    // Get LUX bound 
    //TGraph *z1 = new TGraph("LUX_90CL.dat","%lg %lg");
    //
    TFile *fi_LUX2015 = TFile::Open("LUX_latest_2015.root");
    TGraph *z12015 =(TGraph*) fi_LUX2015->Get("LUX_2015");
    TFile *fi_LUX2016 = TFile::Open("LUX_latest_2016.root");
    TGraph *z12016 =(TGraph*) fi_LUX2016->Get("LUX_2016");

    z12015->SetLineWidth(3);
    z12015->SetLineColor(kGreen+2);
//    z12015->SetLineStyle(2);
    z12016->SetLineWidth(3);
    //z12016->SetLineStyle(2);
    z12016->SetLineColor(kGreen+2);

//    TLegend *leg2 = new TLegend(0.65, 0.15, 0.93, 0.42);
    TLegend *leg2 = new TLegend(0.70, 0.15, 0.97, 0.42);
    leg2->SetFillColor(0);
    leg2->SetBorderSize(0);
    //leg2->AddEntry(z1,"LUX(90\%CL)","L");
//////////////////////////////////////////////////
//  CDMS/ CRESST TOO
    TFile *CDMS_2016f = TFile::Open("CDMS_2016.root");
    TGraph *SCDMS = (TGraph*)CDMS_2016f->Get("CDMS_2016");

    TFile *CRESST2_2016f = TFile::Open("CRESST_2.root");
    TGraph *CRESST2 = (TGraph*)CRESST2_2016f->Get("CRESST_2_2016");

    TFile *PANDAX_2016f = TFile::Open("PANDAX.root");
    TGraph *PANDAX = (TGraph*)PANDAX_2016f->Get("PANDAX");

    SCDMS->SetLineColor(kAzure+7); SCDMS->SetLineStyle(9); SCDMS->SetLineWidth(3);
    CRESST2->SetLineColor(kMagenta+2); CRESST2->SetLineStyle(7); CRESST2->SetLineWidth(3);
    PANDAX->SetLineColor(kMagenta+2); PANDAX->SetLineStyle(4); PANDAX->SetLineWidth(3);
	
//
//

    h_scalar_min->SetTitle("");
    h_scalar_min->SetMinimum(2.0e-47);
    h_scalar_min->SetMaximum(1.0e-39);
    //h_scalar_min->SetMinimum(0.6e-46);
    //h_scalar_min->SetMaximum(1.0e-42);
    h_scalar_min->SetLineColor(4);
    h_scalar_min->SetLineStyle(2);
    h_scalar_min->SetLineWidth(3);
    h_scalar_min->GetXaxis()->SetTitleOffset(1.03);
    h_scalar_min->GetXaxis()->SetTitle("DM mass [GeV]");
    h_scalar_min->GetYaxis()->SetTitle("DM-nucleon cross section [cm^{2}]");
    h_scalar_lat->SetLineColor(4);
    h_scalar_lat->SetLineStyle(1);
    h_scalar_lat->SetLineWidth(3);
    h_scalar_max->SetLineColor(4);
    h_scalar_max->SetLineStyle(2);
    h_scalar_max->SetLineWidth(3);


    h_fermion_min->SetLineColor(kRed);
    h_fermion_min->SetLineStyle(2);
    h_fermion_min->SetLineWidth(3);
    h_fermion_lat->SetLineColor(kRed);
    h_fermion_lat->SetLineStyle(1);
    h_fermion_lat->SetLineWidth(3);
    h_fermion_max->SetLineColor(kRed);
    h_fermion_max->SetLineStyle(2);
    h_fermion_max->SetLineWidth(3);


    //h_scalar_lat->SetFillStyle(3005);
    //h_scalar_lat->SetLineWidth(-402);

    h_scalar_min->Draw("AL");
    h_scalar_lat->Draw("L");
    h_scalar_max->Draw("L");

    h_fermion_min->Draw("L");
    h_fermion_lat->Draw("L");
    h_fermion_max->Draw("L");
    z12016->Draw("L");
    //z12015->Draw("L");
    //CRESST2->Draw("C");
    SCDMS->Draw("C");
    PANDAX->Draw("C");

    //leg2->Draw();
    TLatex *lat = new TLatex(); lat->SetTextSize(0.025);
    lat->SetTextFont(42);
    lat->SetTextColor(kGreen+2);
    lat->SetTextAngle(15);
    //lat->DrawLatex(130,z1->Eval(130)*1.5,"LUX #it{Phys. Rev. Lett.} #bf{116} (2016)");


    //lat->DrawLatex(130,z12015->Eval(130)*1.5,"LUX (2015)");
    lat->DrawLatex(130,z12016->Eval(130)*0.5,"LUX (2016)");
    
    lat->SetTextColor(SCDMS->GetLineColor());
    lat->SetTextAngle(344);
    //lat->SetFillColor(kWhite);
    lat->DrawLatex(5,SCDMS->Eval(5)*1.5,"CDMSlite (2015)");
    
    lat->SetTextColor(kBlue);
    lat->SetTextAngle(330);
    lat->DrawLatex(13,h_scalar_lat->Eval(13)*1.5,"Scalar DM");

    lat->SetTextColor(kRed);
    lat->SetTextAngle(4);
    lat->DrawLatex(5,h_fermion_lat->Eval(5)*1.5,"Fermion DM");


    lat->SetTextColor(kMagenta+2);
    lat->SetTextAngle(15);
    lat->DrawLatex(130,PANDAX->Eval(130)*1.25,"PandaX-II (2016)");

	TLatex * tex = new TLatex();
	tex->SetNDC();
	tex->SetTextFont(42);
	tex->SetLineWidth(2);
	tex->SetTextSize(0.04);
	tex->DrawLatex(0.265,0.93,"4.9 fb^{-1} (7 TeV) + 19.7 fb^{-1} (8 TeV) + 2.3 fb^{-1} (13 TeV)");
  	tex->SetTextFont(42);
	tex->SetTextSize(0.06);
        TLegend *legBOX; 
	if (isPrelim)	{
   		legBOX = new TLegend(0.16,0.83,0.38,0.89);
		legBOX->SetFillColor(kWhite);
		legBOX->SetLineWidth(0);
		legBOX->Draw();
		tex->DrawLatex(0.17, 0.84, "#bf{CMS} #it{Preliminary}");
	} else {
   		legBOX = new TLegend(0.16,0.83,0.28,0.89);
		legBOX->SetFillColor(kWhite);
		legBOX->SetLineWidth(0);
		//legBOX->Draw();
		tex->DrawLatex(0.14, 0.93, "#bf{CMS}");
	}
  tex->SetTextSize(0.045);
  tex->DrawLatex(0.67,0.84,Form("B(H #rightarrow inv.) < %.2f",BRinv));
  tex->DrawLatex(0.72,0.78,"90% CL limits");
  canv->SetTicky(1);
  canv->SetTickx(1);
  canv->SaveAs("limitsDM.pdf"); 

}
