#!/usr/bin/env python 
import sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-f","--fitfile",action='store_true',default=False,help="A ROOT file (mu fit) to add lines")
parser.add_option("-o","--out",help="Output naming")
parser.add_option("-p","--poi",default="r",help="POI")
(options,args) = parser.parse_args()

import ROOT
ROOT.gROOT.SetBatch(1)

def findQuantile(pts,cl):
	#gr is a list of r,nll
        if cl<0 : 
		minNll = pts[0][1]
		minP=pts[0][0]
		for p in pts: 
		 if p[1]<minNll:
			minP = p[0]
			minNll = p[1]
		return minP,minP
	# start by walking along the variable and check if crosses a CL point
	crossbound = [ pt[1]<=cl for pt in pts ]
	rcrossbound = crossbound[:]
	rcrossbound.reverse()

	minci = 0
	maxci = len(crossbound)-1
	min = pts[0][0]
	max = pts[maxci][0]

	for c_i,c in enumerate(crossbound): 
		if c : 
			minci=c_i
			break
	
	for c_i,c in enumerate(rcrossbound): 
		if c : 
			maxci=len(rcrossbound)-c_i-1
			break

	if minci>0: 
		y0,x0 = pts[minci-1][0],pts[minci-1][1]
		y1,x1 = pts[minci][0],pts[minci][1]
		min = y0+((cl-x0)*y1 - (cl-x0)*y0)/(x1-x0)
		
	if maxci<len(crossbound)-1: 
		y0,x0 = pts[maxci][0],pts[maxci][1]
		y1,x1 = pts[maxci+1][0],pts[maxci+1][1]
		max = y0+((cl-x0)*y1 - (cl-x0)*y0)/(x1-x0)

	return min,max

def findMinAndError(file):

 MAXNLL = 25	
 f = ROOT.TFile(file)
 tree = f.Get("limit")

 res = []
 for i in range(tree.GetEntries()):
    tree.GetEntry(i)
    xv = getattr(tree,options.poi)
    if 2*tree.deltaNLL < MAXNLL:
      res.append([xv,2*tree.deltaNLL])

 res.sort()
 minNLL = min([r[1] for r in res])
 for r in res: r[1]-=minNLL
 rfix = []
 for r in res: 
    if r[1]<MAXNLL: rfix.append(r) 
  
 res = rfix[:] 
 if len(res)<5: sys.exit("Not enough points in file %d"%p)
 m,m1 = findQuantile(res,0);
 l,u    = findQuantile(res,1);
 l2,u2  = findQuantile(res,4);
 return m,l,u,l2,u2

##################################################################################
# TEXTBASE
#fi = open(args[0])
fi = ROOT.TFile.Open(args[0])

mu_dict = {}
mus  = []
cats = []

tree = fi.Get("limit")
branches = tree.GetListOfBranches()
for l in branches:
  if "pdfindex_" in l.GetName(): 
    index = l.GetName()
    cat = index[index.find("_")+1:len(index)]  #euch
    cats.append(cat)

print cats


for i in range(tree.GetEntries()):
  tree.GetEntry(i)
  if not (abs(tree.quantileExpected )< 1): continue
  mu = getattr(tree,options.poi)
  mus.append([mu,i])

mus.sort()

nmus = len(mus)
ncats = len(cats)
maxM = max([m[0] for m in mus])
minM = min([m[0] for m in mus])
avediff = (maxM-minM)/nmus

h = ROOT.TH2F("Pdf Index",";%s;category"%options.poi,nmus,minM-avediff/2,maxM+avediff/2,ncats,0,ncats)
# scan the tree 
for i,muT in enumerate(mus):
  tree.GetEntry(muT[1])
  mu = getattr(tree,options.poi)

  h.GetXaxis().SetBinLabel(i+1,"%.2f"%mu)
  for ic, c in enumerate(cats): 
    h.GetYaxis().SetBinLabel(ic+1,c)
    h.SetBinContent(i+1,ic+1,getattr(tree,"pdfindex_%s"%c)+0.001)
    

	
ROOT.gStyle.SetOptStat(0)
c = ROOT.TCanvas("c","c",1500,800)
h.GetXaxis().SetLabelSize(0.03)
h.GetYaxis().SetLabelSize(0.035)
h.GetXaxis().SetLabelFont(42)
h.GetYaxis().SetLabelFont(42)
h.GetXaxis().SetTitleFont(42)
h.GetYaxis().SetTitleFont(42)
h.SetMinimum(-0.1)
h.GetYaxis().SetTitleOffset(1.2)
h.GetXaxis().SetTitleOffset(1.2)

h.Draw("COL")
h.SetMarkerColor(ROOT.kWhite)
ROOT.gStyle.SetPaintTextFormat("2.0f");
h.Draw("TEXTsame")

if options.fitfile:
  print "Adding Lines from Fit"
 # m,l,u,l2,u2   = findMinAndError(options.fitfile)
  m,l,u,l2,u2   = findMinAndError(args[0])

  mline  = ROOT.TLine(m,0,m,ncats)
  lline  = ROOT.TLine(l,0,l,ncats)
  hline  = ROOT.TLine(u,0,u,ncats)
  lline2 = ROOT.TLine(l2,0,l2,ncats)
  hline2 = ROOT.TLine(u2,0,u2,ncats)

  mline.SetLineColor(1); mline.SetLineStyle(1); mline.SetLineWidth(1)
  lline.SetLineColor(1); lline.SetLineStyle(2); lline.SetLineWidth(1)
  hline.SetLineColor(1); hline.SetLineStyle(2); hline.SetLineWidth(1)
  lline2.SetLineColor(1); lline2.SetLineStyle(3); lline2.SetLineWidth(1)
  hline2.SetLineColor(1); hline2.SetLineStyle(3); hline2.SetLineWidth(1)
  mline.Draw()
  lline.Draw()
  hline.Draw()
  lline2.Draw()
  hline2.Draw()

  lat = ROOT.TLatex()
  lat.SetTextFont(42)
  #lat.SetNDC()
  lat.SetTextSize(0.03)

  lat.DrawLatex(m-avediff/2,ncats+0.5,"#hat{#mu}")
  lat.DrawLatex(l-avediff/2,ncats+0.5,"-1#sigma")
  lat.DrawLatex(u-avediff/2,ncats+0.5,"+1#sigma")
  lat.DrawLatex(l2-avediff/2,ncats+0.5,"-2#sigma")
  lat.DrawLatex(u2-avediff/2,ncats+0.5,"+2#sigma")

c.SaveAs("%s.pdf"%options.out)
c.SaveAs("%s.png"%options.out)
