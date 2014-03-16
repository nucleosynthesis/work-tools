# make the plot
import ROOT
ROOT.gROOT.SetBatch(1)

f = ROOT.TFile("smallesttoys.root")
ROOT.gROOT.ProcessLine(".x tdrstyle.cc")

gr  = f.Get("pval")
gr1 = f.Get("pval_cent")
grD = f.Get("pval_data")

c = ROOT.TCanvas("c","c",800,800)
c.SetLogy()
c.SetLogx()

MIN = 10E-5
MAX = 1

ROOT.gStyle.SetOptStat(0)
dH = ROOT.TH1F("dH","dH",100,MIN,MAX)
dH.SetMinimum(MIN)
dH.SetMaximum(MAX)
dH.GetXaxis().SetRangeUser(MIN,MAX)
dH.GetYaxis().SetRangeUser(MIN,MAX)
dH.GetYaxis().SetTitleOffset(1.4)
dH.GetXaxis().SetTitleOffset(1.2)
dH.GetYaxis().SetTitleSize(0.04)
dH.GetXaxis().SetTitleSize(0.04)
dH.GetYaxis().SetLabelSize(0.04)
dH.GetXaxis().SetLabelSize(0.04)
dH.GetXaxis().SetTitle("Local p-value")
dH.GetYaxis().SetTitle("Global p-value")
dH.Draw("AXIS")

gr.SetFillColor(ROOT.kYellow)
gr.Draw("E3")

gr1.SetLineColor(1)
gr1.SetLineWidth(2)
gr1.SetMarkerStyle(21)
gr1.SetMarkerSize(0.8)
gr1.Draw("L")

pvaldats = [ROOT.RooStats.SignificanceToPValue(3.0),ROOT.RooStats.SignificanceToPValue(2.0)]
# Fit for extrapolation
fitstring = "x+[0]*TMath::Exp(-1*(RooStats::PValueToSignificance(x)*RooStats::PValueToSignificance(x))/2)"
medfunc = ROOT.TF1("func",fitstring,pvaldats[0],pvaldats[1]);
#gr.Fit(medfunc,"R,M,EX0","Q")
gr.Fit(medfunc,"R,O","Q")
print medfunc.GetParameter(0)
medfunc.SetLineColor(2)
medfunc.SetLineWidth(3)

# Lines for the data
pvaldat = grD.Eval(0)

#TESTING
# ------------
pvalgdat = gr1.Eval(pvaldat)


# Report Extrapolation!!!!
print "for data 125  From Graph-> ", pvaldat, pvalgdat
print "for data 125  From Extrapolation-> ", pvaldat, "%.3f#sigma"%ROOT.RooStats.PValueToSignificance(pvaldat), medfunc.Eval(pvaldat),"%.3f#sigma"%ROOT.RooStats.PValueToSignificance(medfunc.Eval(pvaldat))
print "So trials factor -- ", medfunc.Eval(pvaldat)/pvaldat

#pvaldats = [ROOT.RooStats.SignificanceToPValue(3.),ROOT.RooStats.SignificanceToPValue(2.)]

text = ROOT.TLatex()
text.SetTextColor(ROOT.kBlue)
text.SetTextSize(0.035)
text.SetTextFont(42)

ty = [0 for z in pvaldats]
tx = [0 for z in pvaldats]

for l,pvaldat in enumerate(pvaldats):
 pvalgdat = gr1.Eval(pvaldat)
 ty[l] = ROOT.TLine(pvaldat,MIN,pvaldat,pvalgdat)
 tx[l] = ROOT.TLine(MIN,pvalgdat,pvaldat,pvalgdat)

 tx[l].SetLineColor(4)
 ty[l].SetLineColor(4)
 tx[l].SetLineWidth(1)
 ty[l].SetLineWidth(1)

 tx[l].Draw()
 ty[l].Draw()
 text.DrawLatex(pvaldat,MIN,"%.1f#sigma"%ROOT.RooStats.PValueToSignificance(pvaldat))
 text.DrawLatex(MIN,pvalgdat,"%.1f#sigma"%ROOT.RooStats.PValueToSignificance(pvalgdat))

mytext= ROOT.TLatex()
mytext.SetTextSize(0.03)
mytext.SetTextFont(42)
mytext.SetNDC()
#mytext.DrawLatex(0.16,0.22,"#splitline{CMS Private}{Global Significance  at m_{H} = 125 GeV ")
mytext.DrawLatex(0.16,0.96,"CMS Private")
mytext.DrawLatex(0.65,0.7,"#splitline{H #rightarrow ZZ #rightarrow 4l}{LEE m_{H} #epsilon [110,145]}")


ROOT.gStyle.SetOptFit(0)

leg = ROOT.TLegend(0.16,0.84,0.39,0.94)
leg.SetFillColor(10)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.SetTextSize(0.03)
leg.AddEntry(medfunc,"p_{global} = p_{local} + %.2f e^{-Z^{2}/2}"%medfunc.GetParameter(0),"L")

medfunc.Draw("Lsame")
leg.Draw()
c.SaveAs("test.pdf")
