import ROOT 
import math
ROOT.gROOT.SetBatch(True)


# usual crap of defining a color/file name etc 
import configure as cfg

variables = cfg.variables.copy()

for var in cfg.variables.keys():
  cfig = cfg.variables[var]
  for sample in cfg.order: 
    variables[var][-2].append(ROOT.TH1F(var+sample,";%s;Arbitrary Units"%cfig[0],cfig[1],cfig[2],cfig[3]))
    variables[var][-2][-1].SetLineWidth(2)
    variables[var][-2][-1].SetLineColor(1)
    variables[var][-2][-1].SetFillColor(cfg.samples[sample][2])
  
  for signal in cfg.signals.keys():
    variables[var][-1].append(ROOT.TH1F(var+signal,";%s;Arbitrary Units;"%cfig[0],cfig[1],cfig[2],cfig[3]))
    variables[var][-1][-1].SetLineWidth(3)
    variables[var][-1][-1].SetLineColor(cfg.signals[signal][2])


def preselection(tr):
     if tr.missing_momentum < 200 : return False
     if tr.nelectrons>0: return False
     if tr.nmuons>0:     return False
     if tr.njets < 2:    return False
     nbtags = 0.001+max([tr.jet1_bT,0]) +max([tr.jet2_bT,0]) +max([tr.jet3_bT,0]) +max([tr.jet4_bT,0])
     if nbtags < 2 : return False
     return True


 # now loop through each sample and fill our histograms 
for i,sample in enumerate(cfg.order):
   counter = 0
   for j,f in enumerate(cfg.samples[sample][0]): 
    fi = ROOT.TFile.Open(f)
    tr = fi.Get(cfg.treeName)
    w =  (cfg.samples[sample][1][j]/tr.GetEntries())*cfg.L
    for ev in range(tr.GetEntries()):
     tr.GetEntry(ev)

     if not preselection(tr): continue
     #print "Passy"
     cfg.doAnalysis(tr,-2,i,w)
     counter+=1
   print "Total of %d MC events for %s"%(counter,sample)


 # now loop through each sample and fill our histograms 
for i,sample in enumerate(cfg.signals): 
   for j,f in enumerate(cfg.signals[sample][0]): 
    fi = ROOT.TFile.Open(f)
    tr = fi.Get("events")
    w = cfg.signalScale*(cfg.signals[sample][1][j]/tr.GetEntries())*cfg.L
    for ev in range(tr.GetEntries()):
     tr.GetEntry(ev)

     if not preselection(tr): continue 
     cfg.doAnalysis(tr,-1,i,w)

# now make the stacks?

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
    h.Draw("histsame")
    leg.AddEntry(h,cfg.signals.keys()[i],"F")

  if cfig[4]: 
  	c.SetLogy(); 
  	stk.SetMinimum(0.01)
	stk.SetMaximum(100*stk.GetMaximum())
  else: stk.SetMinimum(0)
  
  stk.GetYaxis().SetTitleOffset(1.3)
  leg.Draw()
  c.RedrawAxis()
  c.SaveAs("%s.pdf"%var)
  c.SaveAs("%s.png"%var)

 

  
