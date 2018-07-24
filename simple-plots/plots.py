import ROOT 
import math
import sys
import os

cfg_file = sys.argv[1]
sys.path.append(os.path.dirname(os.path.expanduser(cfg_file)))

ROOT.gROOT.SetBatch(True)

# usual crap of defining a color/file name etc 
cfg = __import__(cfg_file)
#import cfg_file as cfg

#import configure as cfg
print "Imported config file"

variables = cfg.variables.copy()

for var in cfg.variables.keys():
  cfig = cfg.variables[var]
  for sample in cfg.order:
    print var, sample
    print var+sample
    variables[var][-2].append(ROOT.TH1F(var+sample,";%s;Arbitrary Units"%cfig[0],cfig[1],cfig[2],cfig[3]))
    variables[var][-2][-1].SetLineWidth(2)
    variables[var][-2][-1].SetLineColor(1)
    variables[var][-2][-1].SetFillColor(cfg.samples[sample][2])
  
  for signal in cfg.signals.keys():
    variables[var][-1].append(ROOT.TH1F(var+signal,";%s;Arbitrary Units;"%cfig[0],cfig[1],cfig[2],cfig[3]))
    variables[var][-1][-1].SetLineWidth(3)
    variables[var][-1][-1].SetLineColor(cfg.signals[signal][2])


 # now loop through each sample and fill our histograms 
for i,sample in enumerate(cfg.order):
   counter = 0
   sumW    = 0
   for j,f in enumerate(cfg.samples[sample][0]): 
    fi = ROOT.TFile.Open(f)
    tr = fi.Get(cfg.treeName)
    w =  (cfg.samples[sample][1][j]/tr.GetEntries())*cfg.L  # can override this in analysis
    cfg.fName   = f
    cfg.fSample = sample
    cfg.fLabel = "b"

    for ev in range(tr.GetEntries()):
     tr.GetEntry(ev)

     if not cfg.preselection(tr): continue
     ps = cfg.doAnalysis(tr,-2,i,w) 
     if ps>0:
        counter+=1
	sumW += ps
   print "Total of %d MC events (%g weighted) for %s"%(counter,sumW,sample)


 # now loop through each sample and fill our histograms 
for i,sample in enumerate(cfg.signals): 
   counter = 0
   sumW    = 0
   for j,f in enumerate(cfg.signals[sample][0]): 
    fi = ROOT.TFile.Open(f)
    tr = fi.Get(cfg.treeName)
    w = (cfg.signals[sample][1][j]/tr.GetEntries())*cfg.L
    #cfg.setInfo(f,sample,"s")
    cfg.fName   = f
    cfg.fSample = sample
    cfg.fLabel = "s"

    for ev in range(tr.GetEntries()):
     tr.GetEntry(ev)

     if not cfg.preselection(tr): continue
     ps = cfg.doAnalysis(tr,-1,i,w)
     if ps>0:
        counter+=1
	sumW += ps

   print "Total of %d MC events (%g weighted) for %s"%(counter,sumW,sample)

# now make the stacks?

# and dump the files 
cfg.fout.cd()
cfg.oTree_s.Write()
cfg.oTree_b.Write()

for var in variables: 
  
  c = ROOT.TCanvas("c_%s"%var,"",700,600)
  cfig = variables[var]
  leg = ROOT.TLegend(0.7,0.6,0.89,0.89)
  leg.SetFillColor(0)

  stk = ROOT.THStack("bkg stack",";%s;Arbitrary Units"%cfig[0])
  for i,h in enumerate(variables[var][-2]):
   stk.Add(h)
   leg.AddEntry(h,cfg.order[i],"F")

  stk.Draw("hist")
  for i,h in enumerate(variables[var][-1]):
    h.Scale(cfg.signalScale)
    h.Draw("histsame")
    if cfg.signalScale!=1: label = cfg.signals.keys()[i]+" x%g"%cfg.signalScale
    else: label = cfg.signals.keys()[i]
    leg.AddEntry(h,label,"F")

  if cfig[4]: 
  	c.SetLogy(); 
  	stk.SetMinimum(0.01)
	stk.SetMaximum(100*stk.GetMaximum())
  else: stk.SetMinimum(0)
  
  stk.GetYaxis().SetTitleOffset(1.3)
  leg.Draw()
  c.RedrawAxis()
  lat = ROOT.TLatex()
  lat.SetNDC()
  lat.SetTextSize(0.04)
  lat.SetTextFont(42)
  lat.DrawLatex(0.1,0.92,"L = %g fb"%cfg.L)
  c.SaveAs("%s.pdf"%var)
  c.SaveAs("%s.png"%var)

 

  
