#!/usr/bin/env python 

# Plots multiple 1D NLL curves from trees (eg like the one from combine)
# The guess is that these will be NLL curves and hence, will report 1sigma errors, clean max nll, reset to 0 etc
# Pass tree 

import numpy
import sys
import array


from optparse import OptionParser
parser=OptionParser()
parser.add_option("-b","--batch",default=False,action="store_true",help="dont forward plots")
parser.add_option("-x","--xvar",default="r",type='str',help="x variable in tree")
parser.add_option("-y","--yvar",default="MH",type='str',help="y variable in tree")
parser.add_option("-o","--outnames",default="",type='str')
parser.add_option("-v","--verbose",default=False,action='store_true')
parser.add_option("-c","--contz",default=False,action='store_true',help="add for first file, the colz")
parser.add_option("-L","--legend",default=False,action='store_true',help="make a legend with file names")
parser.add_option("","--xl",default="",type='str')
parser.add_option("","--yl",default="",type='str')
parser.add_option("","--xr",default="-2,2",type='str')
parser.add_option("","--yr",default="-2,2",type='str')
parser.add_option("","--zr",default="0,10",type='str')
parser.add_option("","--cl",default="1",type='float',help="does nothing for now!")
parser.add_option("","--coloroffset",default=1,type='int')
parser.add_option("","--labels",default="",type='str')
(options,args)=parser.parse_args()


import ROOT
import array

def set_palette(ncontours=999):
    style=1
    if (style==1):
     # default palette, looks cool
     stops = [0.00, 0.34, 0.61, 0.84, 1.00]
     red   = [0.00, 0.00, 0.77, 0.85, 0.90]
     green = [0.00, 0.81, 1.00, 0.20, 0.00]
     blue  = [0.51, 1.00, 0.12, 0.00, 0.00]

     st = array.array('d', stops)
     re = array.array('d', red)
     gr = array.array('d', green)
     bl = array.array('d', blue)
    elif (style==3):
     
     red   = [ 0.00, 0.00, 0.00] 
     blue  = [ 1.00, 0.50, 0.00] 
     green = [ 0.00, 0.00, 0.00] 
     stops = [ 0.00, 0.50, 1.00] 
     st = array.array('d', stops)
     re = array.array('d', red)
     gr = array.array('d', green)
     bl = array.array('d', blue)

    elif (style==2):
     # blue palette, looks cool
     stops = [0.00, 0.34, 0.61, 0.84, 1.00]
     red   = [1.00, 0.84, 0.61, 0.34, 0.00]
     green = [1.00, 0.84, 0.61, 0.34, 0.00]
     blue  = [1.00, 0.84, 0.61, 0.34, 0.00]

     st = array.array('d', stops)
     re = array.array('d', red)
     gr = array.array('d', green)
     bl = array.array('d', blue)

    npoints = len(st)
    ROOT.TColor.CreateGradientColorTable(npoints, st, re, gr, bl, ncontours)
    ROOT.gStyle.SetNumberContours(ncontours)

set_palette(ncontours=255);


nam = options.outnames if options.outnames else options.xvar+"_"+options.yvar
if options.outnames: outtxt= open("%s.txt"%nam,"w")


if not options.xl : options.xl = options.xvar
if not options.yl : options.yl = options.yvar

if len(options.labels): options.labels=options.labels.split(",")
print options.labels
options.xr = options.xr.split(",")
options.yr = options.yr.split(",")
options.zr = options.zr.split(",")


ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(options.batch)
#ROOT.gROOT.ProcessLine(".L ~/scratch0/tools/stats-tools/scanLH2D.C")
#from ROOT import scanLH2D
# Save a tree of all the runs 

def scanLH2D(limit, x, y, xbf, g):

  #g = ROOT.TGraph2D() 
  #g.SetName("WHatever")
 
  n = limit.GetEntries()
  #rV = ROOT.Double
  #rF = ROOT.Double 
  #deltaNLL = ROOT.Double 
  #quant = ROOT.Double

  #limit.SetBranchAddress(y,rV);
  #limit.SetBranchAddress(x,rF);
  #limit.SetBranchAddress("deltaNLL",deltaNLL);
  #limit.SetBranchAddress("quantileExpected",quant);
  
  c=0;
  datanotfound = True;
  for i in range(n):
   limit.GetEntry(i)

   rF = getattr(limit,x)
   rV = getattr(limit,y)
   rV = ROOT.TMath.Exp(rV)
   quant = limit.quantileExpected
   deltaNLL = limit.deltaNLL
   if 2*deltaNLL > float(options.zr[1]): deltaNLL=0.5*float(options.zr[1])+1
   if options.verbose: print "Add point %d, x=%.3g, y=%.3g, z=%.3g"%(i,rF,rV,deltaNLL)
   #print rV, rF, deltaNLL, quant
   if (abs(quant-1)<0.001) :
	if (datanotfound == False): continue
	xbf[0] = rF; 
	xbf[1] = rV;
	datanotfound=False;
   elif (quant > -1):
        g.SetPoint(c,rF,rV,2*deltaNLL);
	c+=1;

  #h =  g.GetHistogram();
  #h.SetName("newName");
  return g



MAXNLL = 35	
OFFSET=options.coloroffset

lat = ROOT.TLatex()
lat.SetTextSize(0.015)
lat.SetNDC()

files = args[:]
allh = []
allg = []
allg2 = []
names = []
BFs = []
print "NEW RUN ---------------------------------------//"
skipFile = False
for p,fn in enumerate(files):

 if not len(options.labels)>0 : names.append(fn.strip(".root"))
 else: names.append(options.labels[p])

 if ":" not in fn:
   f = ROOT.TFile(fn)
   tree = f.Get("limit")
   
   if tree.GetEntries()<=3: skipFile=False
   if skipFile: 
	  print "Tree has no attribute ", options.xvar
	  continue

   #xBF = ROOT.Double()
   #yBF = ROOT.Double()
   xBFs = [0,0]

   g2 = ROOT.TGraph2D()
   g2.SetName(fn+"_graph")
   allg2.append(g2)

   scanLH2D(tree,options.xvar,options.yvar,xBFs,g2)
   h2 = g2.GetHistogram()
   h2.SetName("h2_%d"%p)
   allh.append(h2)
   xBF = xBFs[0]
   yBF = xBFs[1]
   
   print "Best Fit: ", f.GetName(), "X=",xBF,", Y=",yBF

 else : 

   tmpfile = ROOT.TFile.Open(fn.split(":")[0])
   h2 = tmpfile.Get(fn.split(":")[1])
   h2.SetName("h2_%d"%p)
   allh.append(h2)
   xBF = 0
   yBF = 0

 BFs.append([xBF,yBF])
 g = ROOT.TGraph()
 g.SetPoint(0,xBF,yBF)
 allg.append(g)
 skipFile=False

leg = ROOT.TLegend(0.5,0.82,0.99,0.98)
leg.SetTextFont(42)
leg.SetTextSize(0.03)
leg.SetFillColor(0)

c = ROOT.TCanvas("c","c",800,800);

# dummy histogram for axis
dummy = ROOT.TH2F("dum","",10,float(options.xr[0]),float(options.xr[1]),10,float(options.yr[0]),float(options.yr[1]))
dummy.GetXaxis().SetTitle(options.xl)
dummy.GetYaxis().SetTitle(options.yl)
dummy.SetMinimum(float(options.zr[0]))
dummy.SetMaximum(float(options.zr[1]))
dummy.Draw()

addHs = []

lat = ROOT.TLatex()
lat.SetTextFont(42)
lat.SetTextSize(0.03)
lat.SetNDC()

for j,h in enumerate(allh):
 COLOR = j+OFFSET
 if j+1 == 10: OFFSET+=10
# print h
 #h95->SetContourLevel(1,5.99);

 h.SetLineWidth(2)
 h.SetLineColor(COLOR)
 
 h.SetMinimum(float(options.zr[0]))
 h.SetMaximum(float(options.zr[1]))

 #fname = (( (names[j].split("/"))[-1] ).split('.'))[0]
 fname = names[j]
 leg.AddEntry(h,"%s"%(fname),"L")
 if options.contz and j==0 :
 	hc = h.Clone()
 	hc.Draw("sameCOLZ");
 h95 = h.Clone()
 h95.SetContour(2)
 h95.SetLineStyle(2)
 h95.SetContourLevel(1,6.18); #95 %
 h95.Draw("CONT3same");
 h95.SetName(h.GetName()+"_95")
 addHs.append(h95)

 h68 = h.Clone()
 h68.SetLineWidth(3)
 h68.SetContour(2)
 h68.SetContourLevel(1,2.3); #68 %
 h68.Draw("CONT3same");
 allg[j].SetMarkerSize(1.2)
 allg[j].SetMarkerColor(COLOR)
 allg[j].SetMarkerStyle(34)
 allg[j].Draw("P")
 h68.SetName(h.GetName()+"_68")
 addHs.append(h68)
 lat.SetTextColor(COLOR)
 #lat.DrawLatex(0.16,0.86-0.05*j,"(%.2f,%.2f)"%(BFs[j][0],BFs[j][1]))

#leg.Draw()

c.RedrawAxis()

fout = ROOT.TFile("%s.root"%nam,"RECREATE")
for h in allh:
 h.Write()

if options.batch:
  c.SaveAs("%s.pdf"%nam)
  c.SaveAs("%s.png"%nam)
  c.SaveAs("%s.C"%nam)

else:
  raw_input("Done")
