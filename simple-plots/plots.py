import ROOT 
import math
import sys
import os

cfg_file = sys.argv[1]
sys.path.append(os.path.dirname(os.path.expanduser(cfg_file)))

ROOT.gROOT.SetBatch(True)

cfg = __import__(cfg_file)
print "Imported config file"
os.system('mkdir -p %s'%(cfg.odir)) 

variables = cfg.variables.copy()

for var in cfg.variables.keys():
  cfig = cfg.variables[var]
  for sample in cfg.order:
    print var, sample
    print var+sample
    variables[var][-2].append(ROOT.TH1F(var+sample,";%s;Events"%cfig[0],cfig[1],cfig[2],cfig[3]))
    variables[var][-2][-1].SetLineWidth(2)
    variables[var][-2][-1].SetLineColor(1)
    variables[var][-2][-1].SetFillColor(cfg.samples[sample][2])
    variables[var][-2][-1].GetYaxis().SetTitleSize(0.05)
    variables[var][-2][-1].GetXaxis().SetTitleSize(0.05)
  
  for signal in cfg.signals.keys():
    variables[var][-1].append(ROOT.TH1F(var+signal,";%s;Events;"%cfig[0],cfig[1],cfig[2],cfig[3]))
    variables[var][-2][-1].Sumw2()
    variables[var][-1][-1].SetLineWidth(4)
    variables[var][-1][-1].SetMarkerStyle(20)
    variables[var][-1][-1].SetMarkerSize(0.8)
    variables[var][-1][-1].SetMarkerColor(cfg.signals[signal][2])
    variables[var][-1][-1].SetLineColor(cfg.signals[signal][2])
    variables[var][-1][-1].GetYaxis().SetTitleSize(0.05)
    variables[var][-1][-1].GetXaxis().SetTitleSize(0.05)


# now loop through each sample and fill our histograms 
def runLoop(config_list, obj, label, mark):
 for i,sample in enumerate(config_list):
   counter = 0
   sumW    = 0
   for j,f in enumerate(obj[sample][0]): 
    fi = ROOT.TFile.Open(f)
    try:
      tr = fi.Get(cfg.treeName)
      tr.GetEntries()
    except AttributeError:
      print " No TTree in file %s named %s found!"%(f,cfg.treeName)
      sys.exit()
      
    w =  (obj[sample][1][j]/tr.GetEntries())*cfg.L  # can override this in analysis
    cfg.fName   = f
    cfg.fSample = sample
    cfg.fLabel = label

    for ev in range(tr.GetEntries()):
     tr.GetEntry(ev)

     if not cfg.preselection(tr): continue
     ps = cfg.doAnalysis(tr,mark,i,w) 
     if ps>cfg.minWeight:
        counter+=1
	sumW += ps
   print "Total of %d MC events (%g weighted) for %s"%(counter,sumW,sample)

if not len(cfg.order): runLoop(cfg.samples.keys(),config.samples,"b",-2)
else: runLoop(cfg.order,cfg.samples,"b",-2)
runLoop(cfg.signals.keys(),cfg.signals,"s",-1)

# and dump the files
if hasattr(cfg, 'fout'):
 cfg.fout.cd()
 cfg.oTree_s.Write()
 cfg.oTree_b.Write()

for var in variables: 
  
  c = ROOT.TCanvas("c_%s"%var,"",700,600)
  cfig = variables[var]
  if len(cfg.samples)+len(cfg.signals)  >6: #)>4: 
    leg = ROOT.TLegend(0.50,0.62,0.87,0.86)
    leg.SetNColumns(2)
  else: leg = ROOT.TLegend(0.68,0.59,0.87,0.88)
  #if len(cfg.signals)>2: #+len(cfg.signals))>4: 
  #  legS = ROOT.TLegend(0.7,0.73,0.89,0.88)
  #  legS.SetNColumns(2)
  #else: legS = ROOT.TLegend(0.70,0.59,0.89,0.88)

  leg.SetFillColor(ROOT.kWhite)
  leg.SetBorderSize(0)
  #legS.SetFillColor(0)
  #legS.SetBorderSize(0)

  stk = ROOT.THStack("bkg stack",";%s;Events"%cfig[0])
  for i,h in enumerate(variables[var][-2]):
   stk.Add(h)

  for i in range(len(variables[var][-2])-1,-1,-1):
   leg.AddEntry(variables[var][-2][i],cfg.order[i],"F")

  stk.Draw("hist")
  for i,h in enumerate(variables[var][-1]):
    h.Scale(cfg.signalScale)
    h.Draw("histsame")
    h.SetLineWidth(2)
    h.SetLineColor(kWhite)
    h.Draw("histsame")

    #for b in range(h.GetNbinsX()): h.SetBinError(b+1,0)
    #h.Draw("Psame")
    if cfg.signalScale!=1: label = cfg.signals.keys()[i]+" x%g"%cfg.signalScale
    else: label = cfg.signals.keys()[i]

  leg_hists = []
  if not hasattr(cfg,"sig_order"): cfg.sig_order = cfg.signals.keys()
  for k in cfg.sig_order:
    lh = ROOT.TH1F(k,k,1,0,1)
    lh.SetMarkerColor(cfg.signals[k][-1])
    lh.SetLineColor(cfg.signals[k][-1])
    lh.SetLineWidth(4)
    lh.SetMarkerStyle(20)
    lh.SetMarkerSize(0.8)
    leg_hists.append(lh)
    leg.AddEntry(lh,k,"L")

  if cfig[4]: 
  	c.SetLogy(); 
  	stk.SetMinimum(max(0.1*stk.GetMinimum(),1))
	stk.SetMaximum(80*stk.GetMaximum())
  else: 
  	stk.SetMinimum(0)
	stk.SetMaximum(1.2*stk.GetMaximum())
  
  stk.GetYaxis().SetTitleOffset(1.16)
  stk.GetYaxis().SetTitleSize(0.045)
  stk.GetXaxis().SetTitleSize(0.045)
  stk.GetYaxis().SetLabelSize(0.04)
  stk.GetXaxis().SetLabelSize(0.04)
  leg.Draw()
  #legS.Draw()
  c.RedrawAxis()
  lat = ROOT.TLatex()
  lat.SetNDC()
  lat.SetTextSize(0.042)
  lat.SetTextFont(42)
  lat.DrawLatex(0.1,0.92,"#bf{CMS Phase-2} #it{Simulation Preliminary}")
  if not hasattr(cfg,"Label"): cfg.Label = ""
  lat.DrawLatex(0.14,0.8,cfg.Label)
  #lat.DrawLatex(0.62,0.92,"%d fb^{-1} (14#scale[0.75]{ }TeV)"%cfg.L)
  lat.DrawLatex(0.68,0.92,"%d ab^{-1} (14#scale[0.75]{ }TeV)"%3)
  arrows =[]
  if hasattr(cfg,"cut_markers"): 
   #maxi = stk.GetStack().Last().GetBinContent(stk.GetXaxis().FindBin(cfg.cut_markers[-1]))*1.5
   maxi = stk.GetStack().Last().GetBinContent(stk.GetXaxis().FindBin(cfg.cut_markers[-1]))*10
   for cutmarker in cfg.cut_markers: 
     #AR = ROOT.TArrow(cutmarker,stk.GetMinimum(),cutmarker,stk.GetMinimum()*1.4,0.02,"<|");
     AR = ROOT.TLine(cutmarker,stk.GetStack().Last().GetYaxis().GetXmin(),cutmarker,maxi);
     AR.SetLineWidth(3)
     AR.SetLineStyle(2)
     AR.Draw()
     arrows.append(AR)

  c.SetTicky()
  c.SetTickx()
  c.RedrawAxis()
  c.SaveAs("%s/%s.pdf"%(cfg.odir,var))
  c.SaveAs("%s/%s.png"%(cfg.odir,var))

 

  
