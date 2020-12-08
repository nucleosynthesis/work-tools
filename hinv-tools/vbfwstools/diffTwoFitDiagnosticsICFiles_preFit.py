import ROOT 
ROOT.gStyle.SetOptStat(0)
# give me two fitDiagnostic files, same format, i'll plot them ...  

import sys

f1n = sys.argv[1]
f2n = sys.argv[2]
outname = sys.argv[3]

f1 = ROOT.TFile.Open(f1n)
f2 = ROOT.TFile.Open(f2n)

dire = f1.Get("shapes_prefit")
keys = dire.GetListOfKeys()

c = 0
can = ROOT.TCanvas()
can.Print("%s.pdf["%outname,"pdf")
for k in keys:
  ko = k.ReadObj()
  
  for h in ko.GetListOfKeys():
    h1 = h.ReadObj()
    name = h1.GetName()
    h1.SetName("tmp")
    if "total" in name: continue
    h2 = f2.Get("shapes_prefit/%s/%s"%(ko.GetName(),name))
    
    leg = ROOT.TLegend(0.5,0.8,0.89,0.89)
    leg.SetBorderSize(0)
    leg.AddEntry(h1,f1.GetName(),"L")
    leg.AddEntry(h2,f2.GetName(),"L")

    h1.SetTitle(h2.GetName()+" "+ko.GetName())
    h1.SetLineColor(1)
    h2.SetLineColor(2)
    h1.SetLineWidth(2)
    h2.SetLineColor(2)
    can.Clear()
    h1.GetYaxis().SetTitle("Events/Bin Width")
    h1.Draw("")
    h2.Draw("same")
    leg.Draw()

    c+=1
    can.Print("%s.pdf"%outname,"pdf")

can.Print("%s.pdf]"%outname,"pdf")

