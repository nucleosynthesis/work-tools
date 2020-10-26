import ROOT 
import plotRatios_experimental
import sys

BASE_DIRECTORY="../../../fitdiagnostics_perchannel_output/"
#BASE_DIRECTORY="../../../"

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

# inputs are cat Numerator Proc, Denominaor proc, Num Region, Denom Region, ytitle, ymin, ymax, outname
tf2017 = plotRatios_experimental.TFValidator("%s/%s_2017.root"%(BASE_DIRECTORY,sys.argv[1]),"%s/fitDiagnostics%s_2017.root"%(BASE_DIRECTORY,sys.argv[1]))
tf2018 = plotRatios_experimental.TFValidator("%s/%s_2018.root"%(BASE_DIRECTORY,sys.argv[1]),"%s/fitDiagnostics%s_2018.root"%(BASE_DIRECTORY,sys.argv[1]))

tf2017.cat   = sys.argv[1]+"_2017"
tf2017.ZProc = sys.argv[2]
tf2017.WProc = sys.argv[3]
tf2017.ZR = sys.argv[4]
tf2017.WR = sys.argv[5]

tf2018.cat   = sys.argv[1]+"_2018"
tf2018.ZProc = sys.argv[2]
tf2018.WProc = sys.argv[3]
tf2018.ZR = sys.argv[4]
tf2018.WR = sys.argv[5]

ytitle = sys.argv[6]
ymin = sys.argv[7]
ymax = sys.argv[8]
out  = sys.argv[9]

lstr = sys.argv[10]#
clab = sys.argv[11]#

fdummy = ROOT.TFile.Open("%s/fitDiagnostics%s.root"%(BASE_DIRECTORY,tf2017.cat))
hdummy = fdummy.Get("shapes_prefit/%s_SR/qqH_hinv"%tf2017.cat)

data2017 = hdummy.Clone(); data2017.SetName("data2017")
data2018 = hdummy.Clone(); data2018.SetName("data2018")

rata2017  = hdummy.Clone(); rata2017.SetName("ratio2017")
rata2018  = hdummy.Clone(); rata2018.SetName("ratio2018")

ratae2017 = hdummy.Clone(); ratae2017.SetName("ratioe2017")
ratae2018 = hdummy.Clone(); ratae2018.SetName("ratioe2018")

nbins = hdummy.GetNbinsX() 

for b in range(1,nbins+1):

  de2017 = tf2017.calcRdata(b)
  de2018 = tf2018.calcRdata(b)

  data2017.SetBinContent(b,de2017[0])
  data2018.SetBinContent(b,de2018[0])

  data2017.SetBinError(b,de2017[1])
  data2018.SetBinError(b,de2018[1])

  rth2017 = tf2017.calcR(b)
  rth2018 = tf2018.calcR(b)

  rata2017.SetBinContent(b,rth2017)
  rata2017.SetBinError(b,0)
  rata2018.SetBinContent(b,rth2018)
  rata2018.SetBinError(b,0)

  ratae2017.SetBinContent(b,rth2017)
  ratae2018.SetBinContent(b,rth2018)
  ratae2017.SetBinError(b,tf2017.returnRMS(b))
  ratae2018.SetBinError(b,tf2018.returnRMS(b))


data2017.SetMarkerStyle(20)
data2017.SetMarkerSize(1.2)
data2017.SetLineWidth(2)
data2017.SetLineColor(ROOT.kRed+1)
data2017.SetMarkerColor(ROOT.kRed+1)

data2018.SetMarkerStyle(20)
data2018.SetMarkerSize(1.2)
data2018.SetLineWidth(2)
data2018.SetLineColor(ROOT.kBlue+2)
data2018.SetMarkerColor(ROOT.kBlue+2)

rata2017.SetLineColor(ROOT.kRed-4)
rata2017.SetLineWidth(3)
ratae2017.SetLineColor(ROOT.kRed-4)
ratae2017.SetFillColor(ROOT.kRed-9)
ratae2017.SetFillStyle(3001)

rata2018.SetLineColor(ROOT.kAzure-1)
rata2018.SetLineWidth(3)
ratae2018.SetLineColor(ROOT.kAzure-1)
ratae2018.SetFillColor(ROOT.kAzure-4)
ratae2018.SetFillStyle(3001)

c = ROOT.TCanvas("c","c",960,640)
c.SetBottomMargin(0.15)
c.SetRightMargin(0.25)

lat = ROOT.TLegend(0.76,0.62,0.99,0.89)
lat.SetBorderSize(0)
lat.SetTextFont(42)
lat.SetNColumns(2)

dummy_box = ROOT.TH1F("d","d",1,0,1)
dummy_box.SetFillColor(0)
dummy_box.SetLineColor(0)

lat.AddEntry(dummy_box,"2017","F")
lat.AddEntry(dummy_box,"2018","F")
lat.AddEntry(data2017,"Data - bkg","PEL")
lat.AddEntry(data2018,"Data - bkg","PEL")
lat.AddEntry(ratae2017,"Pred. #pm 1#sigma.","LF")
lat.AddEntry(ratae2018,"Pred. #pm 1#sigma.","LF")

# this is the first drawn so set the styles
ratae2017.SetTitle("")
ratae2017.GetYaxis().SetTitleSize(0.06)
ratae2017.GetYaxis().SetTitleOffset(0.8)
ratae2017.GetXaxis().SetTitleSize(0.06)
ratae2017.GetYaxis().SetTitle(ytitle)
ratae2017.SetMinimum(float(ymin))
ratae2017.SetMaximum(float(ymax))
ratae2017.GetXaxis().SetNdivisions(010)

ratae2017.Draw("E2")
rata2017.Draw("histsame")

ratae2018.Draw("E2same")
rata2018.Draw("histsame")

data2017.Draw("PELsame")
data2018.Draw("PELsame")

lat.Draw()

tlat = ROOT.TLatex()
tlat.SetTextFont(42)
tlat.SetNDC()
#tlat.DrawLatex(0.11,0.92,"#bf{CMS} #it{Preliminary}")
tlat.DrawLatex(0.11,0.92,"#bf{CMS}")
tlat.DrawLatex(0.44,0.92,lstr)
tlat.SetTextSize(0.04)
tlat.DrawLatex(0.14,0.83,clab)

c.SetTicky()
c.SetTickx()
c.RedrawAxis()
c.SaveAs("%s.pdf"%out)
c.SaveAs("%s.png"%out)

  

