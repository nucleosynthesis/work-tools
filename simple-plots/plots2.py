#!/usr/bin/python 

import ROOT 
import math
import sys
import os
import gc 
import fnmatch
import array
gc.disable()

cfg_file = sys.argv[1]
mode = sys.argv[2]
job = -1
if len(sys.argv)>3:
  job = int(sys.argv[3])

ALLOWEDMODES =  ["MKHISTOS","PLOTHISTOS","COUNTJOBS","MERGEJOBS"]
if mode not in ALLOWEDMODES : sys.exit("Option not allowed, please choose one of %s"%",".join(ALLOWEDMODES))
print "Will run in mode", mode
if mode=="MKHISTOS":
 MKHISTOS=True
 PLOTHISTOS=False
 COUNTJOBS=False
 MERGEJOBS=False
if mode=="PLOTHISTOS":
 MKHISTOS=False
 PLOTHISTOS=True
 COUNTJOBS=False
 MERGEJOBS=False
if mode=="COUNTJOBS":
 MKHISTOS=False
 PLOTHISTOS=False
 COUNTJOBS=True
 MERGEJOBS=False
if mode=="MERGEJOBS":
 MKHISTOS=False
 PLOTHISTOS=False
 COUNTJOBS=False
 MERGEJOBS=True
 
sys.path.append(os.path.dirname(os.path.expanduser(cfg_file)))

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

cfg = __import__(cfg_file)
print "Imported config file"
os.system('mkdir -p %s'%(cfg.odir)) 

cfg.RUNLOOPCOUNTER=0

def ratio(d,h):
  dn = d.Clone(d.GetName()+"_ratio_hist")
  hn = h.Clone(h.GetName()+"_ratio_hist")
  #ROOT.SetOwnership( dn, True )
  #ROOT.SetOwnership( hn, True )

  for b in range(h.GetNbinsX()):
    dc = d.GetBinContent(b+1)
    hc = h.GetBinContent(b+1)
    he = h.GetBinError(b+1)
    de = d.GetBinError(b+1)
    if hc>0 : 
      ratio = dc/hc
      ratio_e  = de/hc
      ratio_he = he/hc
    else: 
      ratio = 1
      ratio_e =0
      ratio_he=0
   
    dn.SetBinContent(b+1,ratio)
    dn.SetBinError(b+1,ratio_e)

    hn.SetBinContent(b+1,1.)
    hn.SetBinError(b+1,ratio_he)

    #hn.SetBinError(b+1,0.51)
  hn.SetMinimum(0)
  hn.SetMaximum(2.05)
  hn.SetLineColor(ROOT.kBlue+1)
  dn.SetFillColor(0)
  
  return dn,hn

def histversion(h):
  hn = h.Clone()
  for b in range(h.GetNbinsX()):
    hn.SetBinError(b+1,0)
  hn.SetFillColor(0)
  return hn
def findMaxBin(h): 
  maxc = -1000000
  for i in range(h.GetNbinsX()):
    xb = h.GetBinContent(i+1)
    if xb>maxc: maxc=xb
  return maxc

variables = cfg.variables.copy()

for var in cfg.variables.keys():
  cfig = cfg.variables[var]
  if cfig[1]=="BINS":
    cfig[3]=array.array('d',cfig[3])
  for sample in cfg.order:
    if MKHISTOS: 
      if cfig[1]=="BINS": variables[var][-2].append(ROOT.TH1F(var+sample,";%s;Events"%cfig[0],cfig[2],cfig[3]))
      else: variables[var][-2].append(ROOT.TH1F(var+sample,";%s;Events"%cfig[0],cfig[1],cfig[2],cfig[3]))
      variables[var][-2][-1].SetLineWidth(2)
      variables[var][-2][-1].SetLineColor(1)
      variables[var][-2][-1].SetFillColor(cfg.samples[sample][2])
      variables[var][-2][-1].GetYaxis().SetTitleSize(0.05)
      variables[var][-2][-1].GetXaxis().SetTitleSize(0.05)
    else: variables[var][-2].append(var+sample) 
  for signal in cfg.signals.keys():
    if MKHISTOS: 
      if cfig[1]=="BINS": variables[var][-1].append(ROOT.TH1F(var+signal,";%s;Events;"%cfig[0],cfig[2],cfig[3]))
      else: variables[var][-1].append(ROOT.TH1F(var+signal,";%s;Events;"%cfig[0],cfig[1],cfig[2],cfig[3]))
      variables[var][-1][-1].Sumw2()
      variables[var][-1][-1].SetLineWidth(4)
      variables[var][-1][-1].SetMarkerStyle(20)
      variables[var][-1][-1].SetMarkerSize(0.8)
      variables[var][-1][-1].SetMarkerColor(cfg.signals[signal][2])
      variables[var][-1][-1].SetLineColor(cfg.signals[signal][2])
      variables[var][-1][-1].GetYaxis().SetTitleSize(0.05)
      variables[var][-1][-1].GetXaxis().SetTitleSize(0.05)
    else: variables[var][-1].append(var+signal)
  if MKHISTOS:
    if cfig[1]=="BINS": variables[var][-3].append(ROOT.TH1F(var+"data",";%s;Events;"%cfig[0],cfig[2],cfig[3]))
    else: variables[var][-3].append(ROOT.TH1F(var+"data",";%s;Events;"%cfig[0],cfig[1],cfig[2],cfig[3]))
    variables[var][-3][-1].Sumw2()
    variables[var][-3][-1].SetLineWidth(4)
    variables[var][-3][-1].SetMarkerStyle(20)
    variables[var][-3][-1].SetMarkerSize(0.8)
    variables[var][-3][-1].SetMarkerColor(1)
    variables[var][-3][-1].SetLineColor(1)
    variables[var][-3][-1].GetYaxis().SetTitleSize(0.05)
    variables[var][-3][-1].GetXaxis().SetTitleSize(0.05)
  else: variables[var][-3].append(var+"data") 

 
# now loop through each sample and fill our histograms 
def runLoop(config_list, obj, label, mark):
 preselected=0
 for i,sample in enumerate(config_list):
   cfg.RUNLOOPCOUNTER+=1
   if COUNTJOBS: continue
   if job>-1:
    print "counter = ", cfg.RUNLOOPCOUNTER, "job = ", job
    if int(job)!=int(cfg.RUNLOOPCOUNTER): continue 
    else: 
      print "Running job, id = %d"%cfg.RUNLOOPCOUNTER
   print "Processing sample", sample
   counter = 0
   sumW    = 0
   for j,f in enumerate(obj[sample][0]): 
    fi = ROOT.TFile.Open(f)
    print " .. file",fi.GetName()
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

    print " .. has %d entries"%tr.GetEntries()

    for ev in range(tr.GetEntries()):
    # if ( ev%2000==0 ) : sys.stdout.write("\b+")
    # elif ev%1000==0   : sys.stdout.write("\bx")
    # if ( ev%2000==0 or ev%1000==0): sys.stdout.flush(); 

     tr.GetEntry(ev)
     ###################3 Take every 5th event which is preseleced !!!!! ####################, might be better to take event number and modulo it ?
     #preselected+=1
     #if tr.isData==1 and preselected%5!=0 : continue   
     if hasattr(cfg,"BLIND") :
      if cfg.BLIND==True :
      	if tr.isData==1 and (tr.event)%5!=0: continue  
     # assume its blind to be safe
     else: 
      if tr.isData==1 and (tr.event)%5!=0: continue  
     ##############################################################################################################################################
     if sample=="QCD" and tr.LHE_HT < 300 : continue # this is dodgy, why can't i get the sample in the preselection?
     # continue 
     if not cfg.preselection(tr): continue
     ps = cfg.doAnalysis(tr,mark,i,w) 
     if ps>cfg.minWeight:
        counter+=1
	sumW += ps
    fi.Close()
   print "Total of %d MC events (%g weighted) for %s"%(counter,sumW,sample)

def checkAllFilesExist(samp):
 if job>-1 : 
   print " no check in batch mode"
   return 
 for i,sample in enumerate(samp):
   print "Check Files --> ",sample
   for j,f in enumerate(samp[sample][0]):
    print " .. look for file ",f,
    if not os.path.exists(f): sys.exit("No File exists - %s"%f)
    print " .. ok!"
   print " .. sample OK!"

if COUNTJOBS: 
  # note that it won't do anything except add to the counter 
  checkAllFilesExist(cfg.samples)
  if hasattr(cfg, 'data'):  
   checkAllFilesExist(cfg.data)
   runLoop(cfg.data,cfg.data,"d",-3)
  if not hasattr(cfg, 'order'): 
    if len(cfg.samples.keys()): runLoop(cfg.samples.keys(),cfg.samples,"b",-2)
  else: 
    runLoop(cfg.order,cfg.samples,"b",-2)
  checkAllFilesExist(cfg.signals)
  runLoop(cfg.signals.keys(),cfg.signals,"s",-1)
  print "Total number of jobs is %d"%cfg.RUNLOOPCOUNTER
  print ".. run with added option  '1...%d'"%cfg.RUNLOOPCOUNTER
  

if MKHISTOS:
  checkAllFilesExist(cfg.samples)
  checkAllFilesExist(cfg.signals)
  if hasattr(cfg,'data'): checkAllFilesExist(cfg.data)

  if hasattr(cfg, 'data'):  runLoop(cfg.data,cfg.data,"d",-3)
  if not hasattr(cfg, 'order'): 
    if len(cfg.samples.keys()): runLoop(cfg.samples.keys(),cfg.samples,"b",-2)
  else: 
    runLoop(cfg.order,cfg.samples,"b",-2)
  runLoop(cfg.signals.keys(),cfg.signals,"s",-1)

  # and dump the files
  if hasattr(cfg, 'fout'):
   cfg.fout.cd()
   cfg.oTree_s.Write()
   cfg.oTree_b.Write()

if MERGEJOBS: 
  for var in variables.keys(): 
   files = fnmatch.filter(os.listdir('%s'%cfg.odir),"%s_job*.root"%(var))
   files = ["%s/%s"%(cfg.odir,fi) for fi in files]
   out = "%s/%s.root"%(cfg.odir,var)
   #print "hadd -f %s %s"%(out," ".join(files))
   os.system("hadd -f %s %s"%(out," ".join(files)))
  
if MKHISTOS:
  for var in variables.keys(): 
   if job>-1 : ofile = ROOT.TFile("%s/%s_job%d.root"%(cfg.odir,var,job),"RECREATE")
   else: ofile = ROOT.TFile("%s/%s.root"%(cfg.odir,var),"RECREATE")
   for i,h in enumerate(variables[var][-2]):
    ofile.WriteTObject(h)
   for i,h in enumerate(variables[var][-1]):
    ofile.WriteTObject(h) 
   if hasattr(cfg, 'data'):
    for h in variables[var][-3] : ofile.WriteTObject(h)
   ofile.Close()

if PLOTHISTOS:
  for var in variables.keys(): 
    print "Plotting var = ", var
    print " (%d left)"%len(variables.keys())
    #ROOT.gDirectory.GetList().Print()
    ifile = ROOT.TFile("%s/%s.root"%(cfg.odir,var),"OPEN")
    ROOT.SetOwnership(ifile,False)
    c = ROOT.TCanvas("c_%s"%var,"",880,820)
    pad2 = ROOT.TPad("p1","p1",0.0,0.0,1,0.3)
    pad1 = ROOT.TPad("p2","p2",0.0,0.3,1,0.95)
    pad1.SetBottomMargin(0)
    pad2.SetTopMargin(0.02)
    pad2.SetLeftMargin(0.1)
    pad2.SetBottomMargin(0.5)
    pad1.SetLeftMargin(0.1)
    pad1.SetRightMargin(0.2)
    pad2.SetRightMargin(0.2)
    pad1.Draw()
    pad1.cd()

    cfig = variables[var]
    leg = ROOT.TLegend(0.81,0.2,0.99,0.89)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetBorderSize(0)

    stk = ROOT.THStack("background_stack"+var,";%s;Events"%cfig[0])
    btot = ifile.Get(variables[var][-2][0]).Clone("total_background"+var)
    if hasattr(cfg,"globalPlotScale"): btot.Scale(cfg.globalPlotScale)
    #print "For my VAR ", variables[var][-2]
    ordered_hists = []
    for i,h0 in enumerate(variables[var][-2]):
     h = ifile.Get(h0)
     if hasattr(cfg,"globalPlotScale"): h.Scale(cfg.globalPlotScale)
     ordered_hists.append(h)
     #h.SetFillColor(cfg.samples[sample][2])

     if i>0: 
       btot.Add(h)
     stk.Add(h)
    
    ordered_hists.reverse()
    if hasattr(cfg,"data"):
      datatot = ifile.Get(cfig[-3][0])
      for dh in cfig[-3][1:-1]: datatot.Add(ifile.Get(dh.GetName()))
    else: 
      datatot = btot.Clone()

    datatot.SetMarkerStyle(20)
    datatot.SetMarkerSize(0.8)
    datatot.SetMarkerColor(ROOT.kBlack)
    datatot.SetLineWidth(1)

    for i,h in enumerate(ordered_hists):
     leg.AddEntry(h,cfg.order[len(cfg.order)-1-i],"F")

    ordered_hists = [0] 
    maxi = findMaxBin(datatot)
    stk.SetMaximum(max(1,1.2*maxi))
    if cfig[4]: 
	  stk.SetMinimum(max(0.001*stk.GetMinimum(),0.001))
	  stk.SetMaximum(10*stk.GetMaximum())
	  pad1.SetLogy(); 
    else: 
	  stk.SetMinimum(0)
	  #stk.SetMaximum(1.2*stk.GetMaximum())
    
    stk.Draw("hist")
    for i,h0 in enumerate(variables[var][-1]):
      h = ifile.Get(h0)
      h.Scale(cfg.signalScale)
      if hasattr(cfg,"globalPlotScale"): h.Scale(cfg.globalPlotScale)
      h.SetLineWidth(2)
      h.Draw("histsame")
      if cfg.signalScale!=1: label = cfg.signals.keys()[i]+" x%g"%cfg.signalScale
      else: label = cfg.signals.keys()[i]

    datatot.Draw("pelsame")
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

   
    #ofile.WriteTObject(stk)
    stk.GetYaxis().SetTitleOffset(1.14)
    stk.GetYaxis().SetTitleSize(0.045)
    stk.GetXaxis().SetTitleSize(0.045)
    stk.GetYaxis().SetLabelSize(0.04)
    stk.GetXaxis().SetLabelSize(0.04)
    pad1.RedrawAxis()
    lat = ROOT.TLatex()
    lat.SetNDC()
    lat.SetTextSize(0.042)
    lat.SetTextFont(42)
    lat.DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}")
    if not hasattr(cfg,"Label"): cfg.Label = ""
    lat.DrawLatex(0.14,0.8,cfg.Label)
    lat.DrawLatex(0.64,0.92,"%.1f fb^{-1} (13#scale[0.75]{ }TeV)"%((1./1000)*float(cfg.L)))
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

    pad1.SetTicky()
    pad1.SetTickx()
    pad1.RedrawAxis()

    c.cd()
    pad2.Draw()
    pad2.cd()
    datatot_r,hr = ratio(datatot,btot)
    hr.SetTitle("")
    hr.GetYaxis().SetTitle("Ratio")
    hr.GetYaxis().SetTitleSize(0.1)
    hr.GetYaxis().SetTitleOffset(0.5)
    hr.GetYaxis().SetLabelSize(0.08)
    hr.GetXaxis().SetLabelSize(0.08)
    hr.GetXaxis().SetTitleSize(0.1)
    hr.GetXaxis().SetTitleOffset(1.4)
    hr.GetXaxis().SetLabelOffset(0.08)
    hr.GetYaxis().SetNdivisions(010)
    hr.SetFillColor(ROOT.kGray)
    hr.Draw("E2")
    hrl = histversion(hr)
    hrl.Draw("histsame")
    datatot_r.Draw("pesame")
    pad2.RedrawAxis()

    c.cd()
    leg.Draw()
    print "Saving histograms for ", "%s/%s.pdf"%(cfg.odir,var)
    c.SaveAs("%s/%s.pdf"%(cfg.odir,var))
    c.SaveAs("%s/%s.png"%(cfg.odir,var))
    #c.SetName("canvas")
    #ofile.WriteTObject(c);
    #for i,h0 in enumerate(variables[var][-3]): ROOT.SetOwnership(h0,False)
    #for i,h0 in enumerate(variables[var][-2]): ROOT.SetOwnership(h0,False)
    #for i,h0 in enumerate(variables[var][-1]): ROOT.SetOwnership(h0,False)
    #ROOT.SetOwnership(stk,False)

    variables.pop(var)

    c = 0
    stk=0
    datatot_r=0
    datatot=0
    btot=0
    hr=0
    leg=0
    pad1=0
    pad2=0
    hrl=0
    ordered_hists=0
    leg_hists=0

    ifile.Close()
    ifile=0
    #print locals() 
  ROOT.gSystem.Exit(0);
  print "Done! Files are saved to %s"%cfg.odir
 

  
