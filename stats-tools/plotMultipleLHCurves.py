import numpy
import sys
import array

from optparse import OptionParser
parser=OptionParser()
parser.add_option("-s","--shift",default="1.",type='float',help="with --expected, mve the curve to best fit here")
parser.add_option("-b","--batch",default=False,action="store_true",help="dont forward plots")
parser.add_option("-c","--clean",default=False,action="store_true",help="Spike cleaning if not running absolute NLL")
parser.add_option("-e","--expected",default=False,action="store_true",help="shift curve to have minimum at options.shift")
parser.add_option("-p","--points",action="store_true",help="add markers to curve")
parser.add_option("-r","--result",action="store_true",help="make pretty")
parser.add_option("-x","--xvar",default="r",type='str',help="x variable in tree")
parser.add_option("-o","--outnames",default="",type='str')
parser.add_option("","--absNLL",default=False,action='store_true')

parser.add_option("","--xl",default="",type='str')
parser.add_option("","--xr",default="",type='str')
parser.add_option("","--yr",default="",type='str')
parser.add_option("-T","--Title",default="",type='str')
parser.add_option("","--signif",default=False,action='store_true',help="try to calculate significance")
parser.add_option("-m","--makeplot",default=False,action='store_true',help="makes a root file with a graph of the best fit and errors per file")
parser.add_option("-L","--legend",default=False,action='store_true',help="make a legend with file names")
(options,args)=parser.parse_args()

import ROOT

ROOT.gROOT.SetBatch(options.batch)
def applyRanges(GR):
  if options.xr:
	XRANGE=(options.xr).split(":")
	GR.GetXaxis().SetRangeUser(float(XRANGE[0]),float(XRANGE[1]))
  if options.yr:
	YRANGE=(options.yr).split(":")
	GR.GetYaxis().SetRangeUser(float(YRANGE[0]),float(YRANGE[1]))
  if options.xl:
	GR.GetXaxis().SetTitle(options.xl)

def makePlot(c,l,h):
  fout = ROOT.TFile("errors_out.root","RECREATE")
  grC = ROOT.TGraphAsymmErrors()
  grE = grC.Clone()

  for i,c in enumerate(c):
	grC.SetPoint(i,i,c)
	grE.SetPoint(i,i,c)
	grE.SetPointEYlow(i,l[i])
	grE.SetPointEYhigh(i,h[i])
 
  grE.SetFillColor(ROOT.kGreen+2)
  grC.SetMarkerStyle(20) 
  grC.SetMarkerSize(0.85) 
  grC.SetLineWidth(2)
  grC.SetTitle("")
  cc = ROOT.TCanvas("cc","",800,800)
  grC.SetName("centre")
  grE.SetName("errors")
  fout.cd()
  grC.Write(); grE.Write()
  fout.Close()
  print "Created file errors_out.root with x +/- sig(x) per point"


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

MAXNLL = 25	
MAXDER = 1.0

lat = ROOT.TLatex()
lat.SetTextFont(42)
lat.SetNDC()

files = args[:]

grs = []
centres = []
lows	= []
highs	= []
names	= []
lowers =  []
uppers =  []
center=0
print "NEW RUN ---------------------------------------//"
for p,fn in enumerate(files):
 f = ROOT.TFile(fn)
 names.append(f.GetName().strip(".root"))

 tree = f.Get("limit")
 gr = ROOT.TGraph()
 c=0
 res = []

 for i in range(tree.GetEntries()):
  tree.GetEntry(i)
  xv = getattr(tree,options.xvar)
  if 2*tree.deltaNLL ==0 and options.absNLL: continue
  elif abs(tree.deltaNLL)<0.01 : center = xv 
  if options.absNLL: res.append([xv,2*tree.absNLL])
  else :res.append([xv,2*tree.deltaNLL])

 res.sort()

 # remove weird points again
 rfix = []
 cindex = 0
 for i,r in enumerate(res): 
    if options.absNLL: rfix.append(r) 
    else : 
    	if r[1]<MAXNLL:
		rfix.append(r) 

 if options.absNLL : cindex = len(rfix)/2
 else :
    for i,r in enumerate(rfix):
 	if abs(r[0]-center) <0.001: cindex = i

 res = rfix[:]
 # now loop left and right of the " best fit " and remove spikesi
 lhs = rfix[0:cindex]; lhs.reverse()
 rhs= rfix[cindex:-1]
 keeplhs = []
 keeprhs = []

 print "Central is at ", center
 for i,lr in enumerate(lhs): 
   if i==0: 
   	prev = lr[1]
	rprev = lr[0]
	idiff=1
   else:
    diff = abs(lr[0]-rprev) 
    if  not diff > 0: continue
    if (abs(lr[1]-prev)) > MAXDER: 
        idiff+=1
   	continue 
   print "Keeping LHS point, ", i, lr, idiff, abs(lr[1]-prev)
   keeplhs.append(lr)
   prev = lr[1]
   rprev = lr[0]
   idiff=1
 keeplhs.reverse()

 for i,rr in enumerate(rhs):
   if i==0: 
   	prev = rr[1]
	rprev = rr[0]
	idiff=1
   else:
     diff = abs(rr[0]-rprev) 
     if  not diff > 0: continue
     if (abs(rr[1]-prev)) > MAXDER: 
     	idiff+=1
     	continue 
   print "Keeping RHS point, ", i, rr, idiff, abs(rr[1]-prev)
   keeprhs.append(rr)
   prev = rr[1]
   rprev = rr[0]
   idiff=1

 rfix = keeplhs+keeprhs
 rkeep = []
 #now try to remove small jagged spikes
 for i,r in enumerate(rfix):
   if i==0 or i==len(rfix)-1: 
   	rkeep.append(r)
   	continue
   tres = [rfix[i-1][1],r[1],rfix[i+1][1]]
   mean = float(sum(tres))/3.
   mdiff = abs(max(tres)-min(tres))
   if abs(tres[1] - mean) > 0.6*mdiff :continue
   rkeep.append(r)
 rfix=rkeep[:]
 if options.clean : res = rfix[0:] 

 if len(res)<5:
 	print "Not enough points in file %d"%p
	continue
 	# sys.exit("Not enough points in file %d"%p)
 nllmin = min([r[1] for r in res])
 # reset to 0

 if not options.absNLL:
  for i in range(len(res)): res[i][1]-=nllmin

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

 print "File %d, %s = %g(%g)  -%g +%g"%(p,options.xvar,m,m1,m-l,h-m)
 if options.signif: 
	nll0 = gr.Eval(0)
	nllbf = gr.Eval(m)
	signif = (nll0-nllbf)**0.5
	print ".. significance (pval) = ", signif,ROOT.RooStats.SignificanceToPValue(signif)
 lowers.append(l)
 uppers.append(h)

if options.makeplot: 
  makePlot(centres,lows,highs)

c = ROOT.TCanvas("c","c",600,600)
c.SetGridx()
c.SetGridy()


grs[0].GetXaxis().SetTitle("%s"%options.xvar)
grs[0].GetYaxis().SetTitle("-2#Delta Ln(L)")
grs[0].GetYaxis().SetTitleOffset(1.2)

leg = ROOT.TLegend(0.35,0.7,0.55,0.89)
leg.SetTextFont(42)
leg.SetTextSize(0.035)
leg.SetFillColor(0)

allLinesL = []
allLinesU = []

drstring=""

if options.points:drstring+="P"
for j,gr in enumerate(grs):
 leg.AddEntry(gr,names[j],"L")
 if j+1 == 10:
   gr.SetLineColor(50)
   gr.SetMarkerColor(50)
 else:
   gr.SetLineColor(j+1)
   gr.SetMarkerColor(j+1)
 gr.SetLineWidth(2)
 if options.points: 
       if j+1 == 10: gr.SetMarkerColor(50)
       else: gr.SetMarkerColor(j+1)
       gr.SetMarkerStyle(20)
       gr.SetMarkerSize(0.85)
 if j==0:
       applyRanges(gr) 
       gr.Draw("AL"+drstring)
 else : gr.Draw("L"+drstring)

 # add +1 Lines 
 ll = ROOT.TLine(lowers[j],0,lowers[j],gr.Eval(lowers[j]))
 lh = ROOT.TLine(uppers[j],0,uppers[j],gr.Eval(uppers[j]))
 ll.SetLineColor(j+1)
 ll.SetLineStyle(1)
 ll.SetLineWidth(2)
 lh.SetLineColor(j+1)
 lh.SetLineWidth(2) 
 allLinesL.append(ll.Clone())
 allLinesU.append(lh.Clone())
 allLinesL[j].Draw()
 allLinesU[j].Draw()

if options.legend: leg.Draw()

if len(grs)==1:
 allLinesL[0].SetLineColor(2)
 allLinesU[0].SetLineColor(2)

if len(options.Title)>0:
  print "Add title"
  lat.SetTextSize(0.035)
  lat.DrawLatex(0.1,0.92,"%s"%options.Title)

if options.result:
   c.SetGridx(0) 
   c.SetGridy(0) 
   lat.SetTextSize(0.045)
   var = options.xl if options.xl else options.xvar
   lat.DrawLatex(0.4,0.7,"%s = %.2f^{+%.2f}_{-%.2f}"%(var,centres[0],uppers[0]-centres[0],centres[0]-lowers[0]))
   lat.SetTextSize(0.035)
   lat.DrawLatex(0.1,0.92,"CMS Preliminary")

if options.batch:
  nam = options.outnames if options.outnames else options.xvar
  c.SaveAs("%s.pdf"%nam)
  c.SaveAs("%s.png"%nam)
  c.SaveAs("%s.C"%nam)
else:
  raw_input("Done")
