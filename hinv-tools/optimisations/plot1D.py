import ROOT
import sys

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
infile = sys.argv[1]
miny = float(sys.argv[2])
maxy = float(sys.argv[3])
out = str(sys.argv[4])

fi = ROOT.TFile.Open(infile);
limit = fi.Get("limit")
allgrs = []

markers = [25,26,24,31]
colors = [2,3,4,6,1]

leg = ROOT.TLegend(0.12,0.7,0.89,0.99)
leg.SetNColumns(5)
leg.SetFillColor(0)
leg.SetBorderSize(0)

for i,mjj in enumerate([900,1100,1300,1400]):
  
  for j,detajj in enumerate([3,3.5,4,4.5,5.0]):

    limit.Draw("trackedParam_dphi_jj>>limgr_%g_%g(9,0,3.141)"%(mjj,detajj),"limit*(quantileExpected==0.5 && TMath::Abs(trackedParam_mjj-%g)<10 && TMath::Abs(trackedParam_deta_jj-%g)<0.01)"%(mjj,detajj),"L");

    gr = ROOT.gROOT.FindObject("limgr_%g_%g"%(mjj,detajj)).Clone();
    gr.SetMarkerStyle(markers[i])
    gr.SetLineColor(colors[j])
    gr.SetLineWidth(20)
    gr.SetMarkerColor(colors[j])
    print gr.GetNbinsX()
    allgrs.append(gr.Clone())
    leg.AddEntry(allgrs[-1],"m_{jj}>%g, #Delta#eta(j,j)>%g"%(mjj,detajj),"P")

c = ROOT.TCanvas()

h=ROOT.TH1F("h","",1,0,3.14)
h.SetMaximum(maxy)
h.SetMinimum(miny)
h.Draw("axis")
h.GetXaxis().SetTitle("#Delta#phi(j,j) < X")
h.GetYaxis().SetTitle("95% expected limit on BR(VBF H->invisible)")

for gr in allgrs:
 gr.Draw("Phistsame")
 #gr.Draw("histsame")

leg.Draw()
c.SaveAs(("%s.pdf"%out))
#raw_input()
