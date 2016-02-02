import ROOT

#signalsFile = ROOT.TFile.Open("signalsPS.root")
signalsFile = ROOT.TFile.Open("signalsVA.root")
work = signalsFile.Get("combinedws")

#mmedS = [10,20,80,90,100,125,150,175,200,300,325,400,525]
mmedS = [60,80,90,100,125,150,175,200,300,325,400,525]

var = work.var("met")
plot = var.frame()
hists = [ROOT.TH1F("h","h",1,0,1) for m in mmedS]

leg = ROOT.TLegend(0.45,0.4,0.89,0.89)
leg.SetFillColor(0)
leg.SetTextFont(42)

for i,m in enumerate(mmedS):
 color = i+1
 if color==10 or color==19: color+=1
 if not work.data("monojet_signal_signal_800%04d0010"%int(m)): continue 
 work.data("monojet_signal_signal_800%04d0010"%int(m)).plotOn(plot,ROOT.RooFit.MarkerColor(color),ROOT.RooFit.LineColor(color))
 hists[i].SetMarkerColor(color)
 hists[i].SetMarkerSize(0.8)
 hists[i].SetMarkerStyle(21)
 leg.AddEntry(hists[i],"m_{MED}=%d"%int(m),"P")

plot.Draw()
leg.Draw()

raw_input()
