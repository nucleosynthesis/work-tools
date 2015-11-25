#!/usr/bin/env python 
from optparse import OptionParser
parser=OptionParser()
parser.add_option("","--xl",default="",type='str')
parser.add_option("","--xr",default="",type='str')
parser.add_option("","--labels",default="",type='str')
parser.add_option("","--groups",default="",type='str')
parser.add_option("","--batch",default=False,action='store_true')
parser.add_option("-o","--outname",default="",type='str')
(options,args)=parser.parse_args()

if len(options.labels): options.labels=options.labels.split(",")
if len(options.groups): 
	options.groups=options.groups.split(",")
else: options.groups = ["file %d"%p for p in range(len(args)) ]

import ROOT as r 

options.noComb=True

def plotMPdfChComp():
  canv = r.TCanvas("c","c",600,900)
  print 'plotting mpdf ChannelComp'
  if not options.noComb: print '\t will assume first file is the global best fit'
  
  points = []
  loffiles = args[:]
  k=0
  # open the first, it will tell us the number of points in each graph 
  fi = r.TFile.Open(loffiles[0])
  tr = fi.Get("restree")

  ppergraph = tr.GetEntries() #len(loffiles)/options.groups

  xtitle = "#mu"
  if options.xl: xtitle = options.xl

  XRANGE=[-10,10]
  if options.xr: XRANGE=(options.xr).split(":")
  dummyHist = r.TH2F("dummy",";%s;"%xtitle,1,float(XRANGE[0]),float(XRANGE[1]),ppergraph,0,ppergraph)
  xtitle = "#sigma/#sigma_{SM}"

  catGraph1sig = [r.TGraphAsymmErrors() for gr in range(len(loffiles))]

  leg = r.TLegend(0.3,0.88,0.98,0.98)
  leg.SetFillColor(10)
  leg.SetTextFont(42)

  for grIndex,fi in enumerate(loffiles): 
   fig = r.TFile.Open(fi)
   tr = fig.Get("restree")
   for p in range(tr.GetEntries()):
    
    tr.GetEntry(p)
    point = [tr.r,tr.r_d,tr.r_u]
    #grIndex = p//ppergraph
    pIndex  = p

    if len(loffiles)==1: yshift=0.5

    elif len(loffiles)%2==0 : # Even
      if grIndex+0.5 > float(len(loffiles))/2: yshift = 0.5 + (grIndex)*(0.2/len(loffiles))
      else: yshift = 0.5 - (grIndex+1)*(0.2/len(loffiles))
    else :
      if grIndex == (len(loffiles)-1)/2 :yshift=0.5
      elif grIndex > float(len(loffiles))/2: yshift = 0.5 + grIndex*0.2/len(loffiles)
      else :yshift = 0.5 - (grIndex+1)*0.2/len(loffiles)

    catGraph1sig[grIndex].SetPoint(pIndex,point[0],pIndex+yshift)
    catGraph1sig[grIndex].SetPointError(pIndex,point[1],point[2],0.,0.)
   
    if options.labels : binLabel =  options.labels[p]
    else: binLabel = "?"
    dummyHist.GetYaxis().SetBinLabel(p+1,binLabel)

   catGraph1sig[grIndex].SetLineColor(grIndex+1)
   catGraph1sig[grIndex].SetLineWidth(2)
   catGraph1sig[grIndex].SetLineWidth(2)
   catGraph1sig[grIndex].SetMarkerStyle(20)
   catGraph1sig[grIndex].SetMarkerColor(grIndex+1)
   catGraph1sig[grIndex].SetMarkerSize(1.2)
   
   leg.AddEntry(catGraph1sig[grIndex],options.groups[grIndex],"L")

  dummyHist.GetYaxis().SetLabelSize(0.05)
  dummyHist.Draw()

  for gr in range(len(loffiles)):
    catGraph1sig[gr].Draw("EPsame")


  r.gStyle.SetOptStat(0)
  cacheErrSize = r.gStyle.GetEndErrorSize()
  cachePadLeft = canv.GetLeftMargin()
  cachePadRight = canv.GetRightMargin()
  r.gStyle.SetEndErrorSize(8.)
  canv.SetLeftMargin(cachePadLeft+0.09); # was 0.18
  canv.SetRightMargin(cachePadRight-0.03); # was 0.05
  canv.SetGridx(True)
  canv.SetGridy(False)
  canv.Modified()
  canv.Update()
  canv.RedrawAxis()
  if len(loffiles)>1: leg.Draw()

  if not options.batch: raw_input("Looks ok?")
  canv.Print('%s.pdf'%options.outname)
  canv.Print('%s.png'%options.outname)
  canv.Print('%s.C'%options.outname)
  canv.SetName(options.outname)
  #outf.cd()
  #canv.Write()
  
  #r.gStyle.SetEndErrorSize(cacheErrSize)
  #canv.SetLeftMargin(cachePadLeft);
  #canv.SetRightMargin(cachePadRight);

plotMPdfChComp()
