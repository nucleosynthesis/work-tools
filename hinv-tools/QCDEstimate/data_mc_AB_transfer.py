
from optparse import OptionParser
parser=OptionParser()
parser.add_option("","--label",default="")
parser.add_option("","--ymin",default=-0.1,type=float, help="Minimum y-value on plots ")
parser.add_option("","--ymax",default=1.0,type=float, help="Maximum y-value on plots ")
(options,args)=parser.parse_args()

import sys
import ROOT 
ROOT.gStyle.SetOptFit(1111)

fi = ROOT.TFile.Open(args[0])

data_A = fi.Get("BackgroundSubtractedData_A")
data_B = fi.Get("BackgroundSubtractedData_B")

qcd_A = fi.Get("QCD_A")
qcd_B = fi.Get("QCD_B")

qcd_B.Divide(qcd_A)
data_B.Divide(data_A)

data_B.SetMarkerSize(0.8)
data_B.SetMarkerStyle(21)
data_B.SetMarkerColor(1)
data_B.SetLineColor(1)
data_B.SetLineWidth(1)

qcd_B.SetMarkerSize(0.8)
qcd_B.SetMarkerStyle(21)
qcd_B.SetMarkerColor(2)
qcd_B.SetLineColor(2)
qcd_B.SetLineWidth(2)

canv = ROOT.TCanvas("c","c",800,600)

data_B.GetYaxis().SetTitle("Ratio B/A")
data_B.GetXaxis().SetTitle("M_{jj} (GeV)")
data_B.SetTitle("")
data_B.SetName("Data")
qcd_B.SetName("QCD Multijet MC")

data_B.Fit("pol1")
data_B.GetFunction("pol1").SetLineColor(1)
data_B.Draw("")
ROOT.gPad.Update()
data_stats = data_B.FindObject("stats"); data_stats.SetName("data_stats")

qcd_B.Fit("pol1")
qcd_B.GetFunction("pol1").SetLineColor(2)
qcd_B.Draw("")
ROOT.gPad.Update()
qcd_stats = qcd_B.FindObject("stats"); qcd_stats.SetName("qcd_stats")

data_B.SetMinimum(options.ymin)
data_B.SetMaximum(options.ymax)
data_B.Draw("")
qcd_B.Draw("same")


data_stats.SetLineColor(1)
qcd_stats.SetLineColor(2)
qcd_stats.SetTextColor(2)
data_stats.Draw()
data_stats.SetX1NDC(0.12); data_stats.SetX2NDC(0.4)
qcd_stats.SetX1NDC(0.6); qcd_stats.SetX2NDC(0.89)
qcd_stats.Draw()

lat = ROOT.TLatex()
lat.SetTextFont(42)
lat.SetTextSize(0.034)
lat.SetNDC()
lat.DrawLatex(0.1,0.96,options.label)

canv.SaveAs("test_%s.pdf"%sys.argv[1])


#raw_input()
