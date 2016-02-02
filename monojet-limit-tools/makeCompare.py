import ROOT
ROOT.gStyle.SetOptStat(0)

f13TeV = ROOT.TFile.Open("fout-limits.root")
f8TeV = ROOT.TFile.Open("pseudoscalar_8TeV.root")

gr8TeV10 = f8TeV.Get("ps_10_8TeV"); gr8TeV10.SetMarkerColor(ROOT.kGreen+3); gr8TeV10.SetLineColor(ROOT.kGreen+3)
gr8TeV25 = f8TeV.Get("ps_25_8TeV"); gr8TeV25.SetMarkerColor(ROOT.kBlue)   ; gr8TeV25.SetLineColor(ROOT.kBlue)
gr8TeV50 = f8TeV.Get("ps_50_8TeV"); gr8TeV50.SetMarkerColor(ROOT.kRed)    ; gr8TeV50.SetLineColor(ROOT.kRed)

gr13TeV10 = f13TeV.Get("CentralExpected10/pseudoscalar_mMED_mDM10"); gr13TeV10.SetMarkerColor(ROOT.kGreen+3); gr13TeV10.SetLineColor(ROOT.kGreen+3)
gr13TeV25 = f13TeV.Get("CentralExpected25/pseudoscalar_mMED_mDM25"); gr13TeV25.SetMarkerColor(ROOT.kBlue)   ; gr13TeV25.SetLineColor(ROOT.kBlue)
gr13TeV50 = f13TeV.Get("CentralExpected50/pseudoscalar_mMED_mDM50"); gr13TeV50.SetMarkerColor(ROOT.kRed)    ; gr13TeV50.SetLineColor(ROOT.kRed)

gr13TeV10.SetMarkerSize(1.2)
gr13TeV25.SetMarkerSize(1.2)
gr13TeV50.SetMarkerSize(1.2)
gr13TeV10.SetMarkerStyle(23)
gr13TeV25.SetMarkerStyle(23)
gr13TeV50.SetMarkerStyle(23)

leg = ROOT.TLegend(0.2,0.7,0.5,0.89)
leg.SetFillColor(0)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.AddEntry(gr13TeV10,"EXO-15-003 m_{DM}=10 GeV ","pl")
leg.AddEntry(gr13TeV25,"EXO-15-003 m_{DM}=25 GeV ","pl")
leg.AddEntry(gr13TeV50,"EXO-15-003 m_{DM}=50 GeV ","pl")

leg2 = ROOT.TLegend(0.55,0.7,0.85,0.89)
leg2.SetFillColor(0)
leg2.SetBorderSize(0)
leg2.SetTextFont(42)
leg2.AddEntry(gr8TeV10,"EXO-12-055 m_{DM}=10 GeV ","pl")
leg2.AddEntry(gr8TeV25,"EXO-12-055 m_{DM}=25 GeV ","pl")
leg2.AddEntry(gr8TeV50,"EXO-12-055 m_{DM}=50 GeV ","pl")

hist = ROOT.TH1F("dummy",";m_{MED} (GeV);#mu_{up} 90%CL",1,40,700);
hist.SetMaximum(100)
can = ROOT.TCanvas();

hist.Draw("axis")

gr8TeV10.Draw("pl")
gr8TeV25.Draw("pl")
gr8TeV50.Draw("pl")

gr13TeV10.Draw("pl")
gr13TeV25.Draw("pl")
gr13TeV50.Draw("pl")

can.SetLogy()

line = ROOT.TLine(hist.GetXaxis().GetXmin(), 1, hist.GetXaxis().GetXmax(),1)
line.SetLineColor(1);
line.SetLineWidth(3)
line.SetLineStyle(2)
line.Draw()

leg.Draw()
leg2.Draw()

raw_input()
