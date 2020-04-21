import ROOT 
fi = ROOT.TFile.Open("fitDiagnosticsCRonlyFit.root")
odir = "postfit_plots" 
ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

dire = fi.Get("shapes_fit_b")
keys = dire.GetListOfKeys()

samples = { 
	"Z(#nu#nu)+jets (Strong)"   :[  ["ZJETS"],       ROOT.kViolet-8  ,1]
,	"Z(#nu#nu)+jets (VBF)"   :[  ["EWKZNUNU"],       ROOT.kMagenta-10,1 ]
,	"Z(ll)+jets (Strong)"   :[  ["DY"],       ROOT.kGreen+3 ,0]
	,"Z(ll)+jets (VBF)"	:[  ["EWKZll"],   ROOT.kGreen-6 ,0]
	,"Z(ll)+jets"		:[  ["EWKZll","DY"],   ROOT.kGreen+3 ,0]
	,"W(l#nu)+jets (Strong)":[  ["WJETS"],    ROOT.kAzure-3 ,1]
	,"W(l#nu)+jets (VBF)"	:[  ["EWKW"],     ROOT.kAzure-9 ,1]
	,"Dibosons"		:[  ["VV"],       ROOT.kGray ,1]
	,"Top"			:[  ["TOP"],      ROOT.kOrange ,1]
	,"QCD"			:[  ["QCD","qcd"],      ROOT.kOrange+4 ,1]
	,"#gamma+jets (Strong)"			:[  ["qcd_gjets"],      ROOT.kPink+2 ,1]
	,"#gamma+jets (VBF)"			:[  ["ewk_gjets"],      ROOT.kRed-10 ,1]
}
signals = {
	"ggH, H#rightarrow inv."	:[  ["GluGluHtoInv"],      ROOT.kTeal+10 ]
	,"qqH, H#rightarrow inv."	:[  ["VBFHtoInv"],         ROOT.kCyan]
}


def getLumi(n):
  if   "2018" in n: return "59.8"
  elif "2017" in n: return "41.5"
  else :return ""

def figureLabel(l):
  ret = ""
  if "photon" in l : return "Photon CR"
  if "MTR" in l : ret+="MTR "
  if "VTR" in l : ret+="VTR "
  if "ZEE" in l : ret+="Double electron CR"
  if "ZMUMU" in l : ret+="Double muon CR"
  if "WENU"  in l : ret+="Single electron CR"
  if "WMUNU" in l : ret+="Single muon CR"
  if "SR" in l : ret+="SR"
  if "signal" in l : ret+="SR"
  return ret

def histversion(h): 
  hn = h.Clone() 
  for b in range(h.GetNbinsX()): 
    hn.SetBinError(b+1,0)
  hn.SetFillColor(0)
  return hn 

def mkStack(dire):
  hs = dire.GetListOfKeys()
  stk = ROOT.THStack("bkg_stack",";nada;Events")
  myhists=[]
  for h in hs: 
    obj = h.ReadObj()
    nam = obj.GetName()
    for s in samples.keys(): 
      if not samples[s][-1]: continue
      if nam in samples[s][0]:
        obj.SetLineColor(1)
        obj.SetLineWidth(0)
        obj.SetFillColor(samples[s][1])
	foundSample=False
	for i in range(len(myhists)): 
	  if myhists[i][1]==s:
	     myhists[i][2].Add(obj)
	     myhists[i][0]+=obj.Integral()
	     foundSample=True
	     print " I already found, ",s," and will add ", obj.GetName()
	     break
        if not foundSample: myhists.append([obj.Integral(),s,obj])

  myhists.sort()
  for h in myhists: 
    stk.Add(h[2])
  myhists.reverse()
  print myhists
  return stk,myhists

def getSignals(dire): 
  hs = dire.GetListOfKeys()
  myhists=[]
  for h in hs: 
    obj = h.ReadObj()
    nam = obj.GetName()
    for s in signals.keys(): 
      if nam in signals[s][0]: 
        obj.SetLineWidth(3)
        obj.SetMarkerStyle(20)
        obj.SetMarkerColor(20)
        obj.SetMarkerColor(signals[s][1])
        obj.SetLineColor(signals[s][1])

        myhists.append([obj.Integral(),s,histversion(obj)])
  
  return myhists
def ratio(d,h): 
  dn = d.Clone()
  hn = h.Clone()
  
  for b in range(h.GetNbinsX()): 
    dc = d.GetY()[b]
    hc = h.GetBinContent(b+1)
    he = h.GetBinError(b+1)
    print he
    dx = d.GetX()[b]
    du = d.GetErrorYhigh(b)
    dd = d.GetErrorYlow(b)
    dxu = d.GetErrorXhigh(b)
    dxd = d.GetErrorXlow(b)
    dn.SetPoint(b,dx,dc/hc)
    dn.SetPointError(b,dxd,dxu,dd/hc,du/hc)
    
    hn.SetBinContent(b+1,1.)
    hn.SetBinError(b+1,he/hc)
    #hn.SetBinError(b+1,0.51)
  hn.SetMinimum(0.75)
  hn.SetMaximum(1.25)
  return dn,hn
  

def findMaxBin(h): 
  maxc = -1000000
  for i in range(h.GetNbinsX()):
    xb = h.GetBinContent(i+1)
    if xb>maxc: maxc=xb
  return maxc

for k in keys:
  ko = k.ReadObj()
  if "signal" in ko.GetName() or "SR" in ko.GetName(): 
    dh = ko.Get("total_background")
    d = ROOT.TGraphAsymmErrors()
    for i in range(dh.GetNbinsX()): 
      c = dh.GetBinContent(i+1)
      w = dh.GetBinWidth(i+1)
      d.SetPoint(i,dh.GetBinCenter(i+1),c)
      d.SetPointError(i,w/2,w/2,((w*c)**0.5)/w,((w*c)**0.5)/w)
  else: d = ko.Get("data")

  c = ROOT.TCanvas("c","c",820,820)
  pad2 = ROOT.TPad("p1","p1",0.0,0.0,1,0.3)
  pad1 = ROOT.TPad("p2","p2",0.0,0.3,1,0.95)
  pad1.SetBottomMargin(0.01)
  pad1.SetTopMargin(0.05)
  pad2.SetTopMargin(0.02)
  pad2.SetBottomMargin(0.5)
  pad1.SetLeftMargin(0.15)
  pad2.SetLeftMargin(0.15)
  pad1.SetRightMargin(0.1)
  pad2.SetRightMargin(0.1)
  
  
  pad1.Draw()
  pad1.cd()
  h   = ko.Get("total_background")
  h.SetTitle("")
  h.SetLineColor(ROOT.kBlack)
  h.SetFillColor(ROOT.kGray+2)
  h.SetFillStyle(3345)
  hpf = fi.Get("shapes_prefit/%s/total_background"%(ko.GetName()))
  hpf.SetLineWidth(2)
  hpf.SetLineColor(2)
  h.SetLineWidth(2)
  d.SetMarkerStyle(20)
  d.SetLineWidth(2)
  d.SetMarkerSize(1.0)

  # need to edit the samples for Z vs non Z regions 
  if "ZMUMU" in ko.GetName() or "ZEE" in ko.GetName(): 
    samples["Z(ll)+jets (Strong)"][-1]=1
    samples["Z(ll)+jets (VBF)"][-1]=1
    samples["Z(ll)+jets"][-1]=0
  else: 
    samples["Z(ll)+jets (Strong)"][-1]=0
    samples["Z(ll)+jets (VBF)"][-1]=0
    samples["Z(ll)+jets"][-1]=1
  stk,hists = mkStack(fi.Get("shapes_fit_b/%s"%(ko.GetName())))
  
  h.GetYaxis().SetTitle("Events/GeV")
  h.GetXaxis().SetTitle("M_{jj} (GeV)")
  h.GetYaxis().SetTitleOffset(1.14)
  h.GetYaxis().SetTitleSize(0.045)
  h.GetXaxis().SetTitleSize(0.045)
  h.GetYaxis().SetLabelSize(0.04)
  h.GetXaxis().SetLabelSize(0.04)

  maxi = findMaxBin(h)
  h.SetMaximum(max(1,100*maxi))

  h.Draw("E2")
  stk.Draw("histsame")
  h.Draw("E2same")

  hl = histversion(h)
  hpf.Draw("histsame")
  hl.Draw("histsame")
  sigs = getSignals(fi.Get("shapes_prefit/%s"%(ko.GetName())))
  if len(sigs)>0: 
   for s in sigs: 
    s[2].Draw("histsame")
    s[2].Draw("Psame")
  d.Draw("P")

  pad1.RedrawAxis()
  pad1.SetLogy()
  
  leg = ROOT.TLegend(0.54,0.54,0.88,0.90)
  leg.SetFillColor(ROOT.kWhite)
  leg.SetBorderSize(0)


  leg.AddEntry(d,"Data","PEL")
  for lh in hists:
   leg.AddEntry(lh[2],lh[1],"F")
  leg.AddEntry(hpf,"Total background (Pre-fit)","L")
  leg.AddEntry(h,"Total background (Post-fit) #pm 1#sigma","LF")
  if len(sigs)>0: 
   for s in sigs: 
    leg.AddEntry(s[2],s[1],"LP")
  pad1.RedrawAxis()

  c.cd()
  pad2.Draw()
  pad2.cd()
  dr,hr = ratio(d,h)
  drpf,hrpf = ratio(d,hpf)
  drpf.SetMarkerColor(2)
  drpf.SetLineColor(2)

  hr.SetTitle("")
  hr.GetYaxis().SetTitle("Data/prediction")
  hr.SetFillColor(ROOT.kGray+2)
  hr.GetYaxis().SetTitleSize(0.1)
  hr.GetYaxis().SetTitleOffset(0.5)
  hr.GetYaxis().SetLabelSize(0.08)
  hr.GetXaxis().SetLabelSize(0.08)
  hr.GetXaxis().SetTitleSize(0.1)
  hr.GetXaxis().SetTitleOffset(1.6)
  hr.GetXaxis().SetLabelOffset(0.08)
  hr.GetYaxis().SetNdivisions(010)
  hr.Draw("E2")
  hrl = histversion(hr)
  hrl.Draw("histsame")
  drpf.Draw("P")
  dr.Draw("P")
  pad2.SetTicky()
  pad1.SetTicky()
  pad2.RedrawAxis()

  leg2 = ROOT.TLegend(0.18,0.84,0.42,0.96)
  leg2.SetNColumns(2)
  leg2.SetFillColor(ROOT.kWhite)
  leg2.SetBorderSize(0)
  leg2.AddEntry(drpf,"Pre-fit","PEL")
  leg2.AddEntry(dr,"Post-fit","PEL")
  leg2.Draw()

  c.cd()
  leg.Draw()
  lat = ROOT.TLatex()
  lat.SetNDC()
  lat.SetTextSize(0.032)
  lat.SetTextFont(42)
  lat.DrawLatex(0.16,0.93,"#bf{CMS} #it{Preliminary}")
  lat.DrawLatex(0.18,0.88,figureLabel(ko.GetName()))
  #lat.DrawLatex(0.62,0.92,"%d fb^{-1} (14#scale[0.75]{ }TeV)"%cfg.L)
  lat.DrawLatex(0.68,0.93,"%s fb^{-1} (13#scale[0.75]{ }TeV)"%(getLumi(ko.GetName())))
  
   
  c.SaveAs("%s/%s.pdf"%(odir,ko.GetName()))
  c.SaveAs("%s/%s.png"%(odir,ko.GetName()))

