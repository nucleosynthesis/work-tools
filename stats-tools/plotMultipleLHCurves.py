import ROOT

import sys

from optparse import OptionParser
parser=OptionParser()
parser.add_option("-s","--shift",default="1.",type='float')
parser.add_option("-e","--expected",default=False,action="store_true")
parser.add_option("-p","--points",action="store_true")
parser.add_option("-x","--xvar",default="r",type='str')
parser.add_option("-m","--makeplot",default=False,action='store_true')
parser.add_option("-L","--legend",default=False,action='store_true')
(options,args)=parser.parse_args()

def makePlot(c,l,h):
  fout = ROOT.TFile("errors_out.root","RECREATE")
  grC = ROOT.TGraphAsymmErrors()
  grE = grC.Clone()

  for i,c in enumerate(c):
	grC.SetPoint(i,i,c)
	grE.SetPoint(i,i,c)
	grE.SetPointEYlow(i,l[i])
	grE.SetPointEYhigh(i,h[i])
  
  grC.SetTitle("")
  cc = ROOT.TCanvas("cc","",800,800)
  grC.SetName("centre")
  grE.SetName("errors")
  fout.cd()
  grC.Write(); grE.Write()
  fout.Close()


def findQuantile(pts,cl):

	#gr is a list of r,nll
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
	
	
files = args[:]

grs = []
centres = []
lows	= []
highs	= []
names	= []

for p,fn in enumerate(files):
 f = ROOT.TFile(fn)
 names.append(f.GetName())

 tree = f.Get("limit")
 gr = ROOT.TGraph()
 c=0
 res = []

 for i in range(tree.GetEntries()):
  tree.GetEntry(i)
  xv = getattr(tree,options.xvar)
  res.append([tree.r,2*tree.deltaNLL])

 res.sort()
 minNLL = min([r[1] for r in res])
 for r in res: r[1]-=minNLL
	
 m,m1 = findQuantile(res,0);
 l,h  = findQuantile(res,1);

 if  options.expected:
	for r in res: r[0]-=m-options.shift
 	m,m1 = findQuantile(res,0);
	l,h  = findQuantile(res,1);

 for r,nll in res:
	gr.SetPoint(c,r,(nll))
	c+=1
 grs.append(gr.Clone())

 centres.append(m)
 lows.append(m-l)
 highs.append(h-m)

if options.makeplot: 
  makePlot(centres,lows,highs)

c = ROOT.TCanvas("c","c",600,600)
c.SetGridx()
c.SetGridy()
grs[0].GetXaxis().SetTitle("#mu")
grs[0].GetYaxis().SetTitle("-2#Delta Ln(L)")

leg = ROOT.TLegend(0.35,0.7,0.55,0.89)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.SetFillColor(0)

for j,gr in enumerate(grs):
 leg.AddEntry(gr,names[j],"LP")
 gr.SetLineColor(j+1)
 gr.SetLineWidth(2)
 if options.points: 
	gr.SetMarkerColor(j+1)
	gr.SetMarkerStyle(21)
	gr.SetMarkerSize(0.8)
 if j==0: gr.Draw("ALP")
 else : gr.Draw("LP")

if options.legend: leg.Draw()
raw_input()
