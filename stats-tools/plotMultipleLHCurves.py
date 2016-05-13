#!/usr/bin/env python 

# Plots multiple 1D NLL curves from trees (eg like the one from combine)
# The guess is that these will be NLL curves and hence, will report 1sigma errors, clean max nll, reset to 0 etc
# Pass tree 

import numpy
import sys
import array
SANDYLINES = []
def sandy_callback(option, opt_str,value,parser):
	print "add ", value
	SANDYLINES.append(str(value))

from optparse import OptionParser
parser=OptionParser()
parser.add_option("-e","--expected",default=False,action="store_true",help="Run expected")
parser.add_option("-s","--shift",default="1.",type='float',help="run with --expected, move the curve to best fit here")
parser.add_option("-b","--batch",default=False,action="store_true",help="dont forward plots")
parser.add_option("-c","--clean",default=False,action="store_true",help="Spike cleaning if not running absolute NLL")
parser.add_option("-p","--points",action="store_true",help="add markers to curve")
parser.add_option("-r","--result",action="store_true",help="make pretty result")
parser.add_option("-v","--verb",action="store_true",help="Put Results in Legend")
parser.add_option("-V","--VERB",action="store_true",help="spitoutlikelihood")
parser.add_option("-x","--xvar",default="r",type='str',help="x variable in tree")
parser.add_option("-o","--outnames",default="",type='str')
parser.add_option("-m","--makeplot",default=False,action='store_true',help="makes a root file with a graph of the best fit and errors per file")
parser.add_option("-L","--legend",default=False,action='store_true',help="make a legend with file names")
parser.add_option("","--runSpline",default=False,action='store_true',help="Create a smoothed spline from input tree to make plot")
parser.add_option("","--nofile",default=False,action='store_true',help="Remove filename from Legend")
parser.add_option("","--Title",default="",type='str')
parser.add_option("","--absNLL",default=False,action='store_true')
parser.add_option("","--xl",default="",type='str')
parser.add_option("","--xr",default="",type='str')
parser.add_option("","--yr",default="",type='str')
parser.add_option("","--ylabel",default="-2#Delta Log(L)",type='str')
parser.add_option("","--cl",default="1",type='float')
parser.add_option("","--coloroffset",default=1,type='int')
parser.add_option("","--null",default=0.,type='float')
parser.add_option("","--labels",default="",type='str')
parser.add_option("","--styles",default="",type='str')
parser.add_option("","--colors",default="",type='str')
parser.add_option("","--dnll",default="",type='str')
parser.add_option("","--relative",default="",type=str)
parser.add_option("","--cut",default="",type='str')
parser.add_option("","--signif",default=False,action='store_true',help="try to calculate significance ->  sqrt[2(nll(min)-nll(option.null))] ")
parser.add_option("","--line",type='string',action='callback',callback=sandy_callback)
parser.add_option("","--lumilab",type='string',default="")
parser.add_option("","--entrylabel",type='string',default="")
(options,args)=parser.parse_args()
if options.entrylabel: options.entrylabel = [float(e) for e in options.entrylabel.split(",")]

nam = options.outnames if options.outnames else options.xvar
if options.outnames: outtxt= open("%s.txt"%nam,"w")

if len(options.labels): options.labels=options.labels.split(",")
import ROOT
import array


ROOT.gROOT.SetBatch(options.batch)
# Save a tree of all the runs 
outTreeFile = ROOT.TFile("%s-tree.root"%nam,"RECREATE")
outTree = ROOT.TTree("restree","restree")

cenV  = array.array('d',[0]) 
errHV = array.array('d',[0]) 
errLV = array.array('d',[0]) 
entlabel = array.array('d',[0])

outTree.Branch("%s"%options.xvar,cenV,"%s/D"%options.xvar)
outTree.Branch("%s_u"%options.xvar,errHV,"%s_u/D"%options.xvar)
outTree.Branch("%s_d"%options.xvar,errLV,"%s_d/D"%options.xvar)
if options.entrylabel: outTree.Branch("entrylabel",entlabel,"entrylabel/D")

if options.runSpline: ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

def makeRelative(gr, value): 
  rel_val = gr.Eval(value)
  x = ROOT.Double()
  y = ROOT.Double()
  if rel_val == 0 : return
  for pt in range(gr.GetN()):
    gr.GetPoint(pt,x,y)
    gr.SetPoint(pt,x,y/rel_val)

def makespline(tr): # r,2nll
  MIN = tr.GetMinimum(options.xvar) 
  MAX = tr.GetMaximum(options.xvar)
  rxv   = ROOT.RooRealVar(options.xvar,options.xvar,MIN,MAX)
  args = ROOT.RooArgList(rxv)
  spl   = ROOT.RooSplineND("spl","spl",args,tr,"deltaNLL",0.1,"abs(deltaNLL)>0.0001");
  res = []
  for xx in numpy.arange(MIN,MAX,0.1*(MAX-MIN)/tr.GetEntries()):
    rxv.setVal(xx)
    res.append([xx,2*spl.getVal()])
  return res


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
  fout = ROOT.TFile("%s_errs.root"%nam,"RECREATE")
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
  cc = ROOT.TCanvas("cc","",800,760)
  grC.SetName("centre")
  grE.SetName("errors")
  fout.cd()
  grC.Write(); grE.Write()
  fout.Close()
  print "Created file errors_out.root with x +/- sig(x) per point"

def findQuantile(pts,cl):

	#gr is a list of r,nll
        if cl<=0 : 
		minNll = pts[0][1]
		minP=pts[0][0]
		for p in pts: 
		 if p[1]<0 :continue
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

MAXNLL = 35	
MAXDER = 1.0
OFFSET=options.coloroffset

lat = ROOT.TLatex()
#lat.SetTextFont(42)
lat.SetTextSize(0.015)
lat.SetNDC()

files = args[:]

grs = []
centres = []
lows	= []
highs	= []
names	= []
lowers =  []
uppers =  []
signifs =  []
center=0
extfiles = []


if options.colors: COLORS = options.colors.split(",")
else: COLORS = [i+options.coloroffset for i in range(len(files))] 
if options.styles: STYLES = options.styles.split(",")
else: STYLES = [1 for i in files]

print "NEW RUN ---------------------------------------//"
skipFile = False
for p,fn in enumerate(files):

 if not len(options.labels) : names.append(fn.strip(".root"))
 else: names.append(options.labels[p])
 if ":" not in fn:
   f = ROOT.TFile(fn)
   
   tree = f.Get("limit")
   gr = ROOT.TGraph()
   grEXT = [ROOT.TGraph() for SS in SANDYLINES]
   c=0
   res = []


   for i in range(tree.GetEntries()):
     tree.GetEntry(i)
     try :
	  xv = getattr(tree,options.xvar)
     except :
	 continue
	 skipFile = True
     
     skipPoint=False
     if options.cut!="": 
       for cuts in options.cut.split(","):
         cuts = cuts.split(":")
	 print cuts
         if abs( getattr(tree,cuts[0]) - float(cuts[1])) > 0.001: 
	   skipPoint=True
     if skipPoint: continue
     if options.dnll!="": dnll = getattr(tree,options.dnll)
     else: dnll = 2*tree.deltaNLL 
     if dnll==0 and options.absNLL: continue
     #if abs(tree.quantileExpected)==1: continue
     elif abs(dnll)<0.0001 and dnll > 0: 
     	center = xv
	cenDNLL = dnll
     if options.absNLL: res.append([xv,2*tree.absNLL])
     else :res.append([xv,dnll])
     for jj in range(len(SANDYLINES)): grEXT[jj].SetPoint(i,xv,getattr(tree,'%s'%SANDYLINES[jj]))

   if skipFile: 
	  print "Tree has no attribute ", options.xvar
	  continue

   if options.runSpline: 
     res = makespline(tree)
     res.append([center,cenDNLL])
     #put the best fit in 


   res.sort()

   skipFile=False
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

   #print "Central is at ", center
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
     #print "Keeping LHS point, ", i, lr, idiff, abs(lr[1]-prev)
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
     #print "Keeping RHS point, ", i, rr, idiff, abs(rr[1]-prev)
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

   if nllmin<0: print "Warning, nll Minimum < 0 ?", nllmin
   #print res
   #sys.exit()
   # reset to 0
   #if not options.absNLL:
   # for i in range(len(res)): res[i][1]-=nllmin

   m,m1 = findQuantile(res,0);
   l,h  = findQuantile(res,options.cl);

   if  options.expected:
	  for r in res: r[0]-=m-options.shift
	  m,m1 = findQuantile(res,0);
	  l,h  = findQuantile(res,options.cl);

   for r,nll in res:
	  gr.SetPoint(c,r,(nll))
	  if options.VERB : print "at: ", r, nll
	  c+=1

   gr.SetName(names[p])
   grs.append(gr.Clone())
 else : 
 	tmpfile = ROOT.TFile.Open(fn.split(":")[0])
	gr = tmpfile.Get(fn.split(":")[1])
	res = []
	XP = ROOT.Double()
	YP = ROOT.Double()
 	for n in range(gr.GetN()) :
		gr.GetPoint(n,XP,YP);
		res.append([XP,YP])
	m,m1 = findQuantile(res,0);
	l,h  = findQuantile(res,options.cl);
	extfiles.append(tmpfile)
        gr.SetName(names[p])
        grs.append(gr.Clone())

 centres.append(m)
 lows.append(m-l)
 highs.append(h-m)

 print "%s, %s = %g(%g) -%g +%g  (%g %g) "%(names[p],options.xvar,m,m1,m-l,h-m,l,h)
 if options.outnames: outtxt.write("File %s, %s = %g(%g)  -%g +%g (%g %g) \n"%(fn,options.xvar,m,m1,m-l,h-m,l,h))
 signif = 0
 if options.signif: 
	nll0 = gr.Eval(options.null)
	nllbf = gr.Eval(m)
	signif = (nll0-nllbf)**0.5
	print ".. significance (pval) from %g = "%options.null, signif,ROOT.RooStats.SignificanceToPValue(signif)
	if options.outnames: outtxt.write(".. significance (pval) from %g = \n"%options.null, signif,ROOT.RooStats.SignificanceToPValue(signif))

 cenV[0] = m
 errHV[0]  = h-m
 errLV[0]  = m-l
 if len(options.entrylabel): entlabel[0] = options.entrylabel[p]
 lowers.append(l)
 uppers.append(h)
 signifs.append(signif)
 outTree.Fill()

# Now set the graphs relative to some point if requested 
if options.relative!="": 
  for j,gr in enumerate(grs):
   makeRelative(gr,float(options.relative))

if options.makeplot: 
  makePlot(centres,lows,highs)


# Now make the plot of the curve
c = ROOT.TCanvas("c","c",600,600)
if options.result: 
  	c.SetLeftMargin(0.13)
  	c.SetBottomMargin(0.13)
	c.SetTicky()
        c.SetTickx()
c.SetGridx()
c.SetGridy()

grs[0].GetXaxis().SetTitle("%s"%options.xvar)
grs[0].GetYaxis().SetTitle("%s"%options.ylabel)
grs[0].GetYaxis().SetTitleOffset(1.3)
grs[0].GetXaxis().SetTitleOffset(1.3)
if options.result: grs[0].GetYaxis().SetTitleSize(0.045)
if options.result: grs[0].GetXaxis().SetTitleSize(0.045)

if options.result:
	LHeight = (0.87-0.75)/2
	LHeight*=len(grs)
	leg = ROOT.TLegend(0.58,0.87-LHeight,0.87,0.87)

else:leg = ROOT.TLegend(0.05,0.72,0.99,0.98)
leg.SetTextFont(42)
leg.SetTextSize(0.03)
leg.SetFillColor(0)
#leg.SetBorderSize(0)

allLinesL = []
allLinesU = []
allExtLines = []
drstring=""

if options.points:drstring+="P"
for j,gr in enumerate(grs):
 #COLOR = j+OFFSET
 #if j+1 == 10: OFFSET+=10
 COLOR = int(COLORS[j])
 STYLE = int(STYLES[j])
 if COLOR >= 10 : COLOR+=1
 gr.SetLineColor(COLOR)
 gr.SetMarkerColor(COLOR)
 gr.SetLineWidth(2)
 gr.SetLineStyle(STYLE)
 gr.SetTitle("")
 for jj in range(len(SANDYLINES)): 
 	grEXT[jj].SetMarkerColor(COLOR)
 	grEXT[jj].SetMarkerStyle(20+jj)
 	grEXT[jj].SetMarkerSize(0.9)
 if options.points: 
       gr.SetMarkerColor(COLOR)
       gr.SetMarkerColor(COLOR)
       gr.SetMarkerStyle(20)
       gr.SetMarkerSize(0.85)
 if j==0:
       applyRanges(gr) 
       gr.Draw("AL"+drstring)
 else : gr.Draw("L"+drstring)

 for jj in range(len(SANDYLINES)): grEXT[jj].Draw("p") 
 # add +1 Lines 
 ll = ROOT.TLine(lowers[j],0,lowers[j],gr.Eval(lowers[j]))
 lh = ROOT.TLine(uppers[j],0,uppers[j],gr.Eval(uppers[j]))
 ll.SetLineColor(COLOR)
 ll.SetLineStyle(STYLE)
 lh.SetLineStyle(STYLE)
 ll.SetLineWidth(2)
 lh.SetLineColor(COLOR)
 lh.SetLineWidth(2) 
 allLinesL.append(ll.Clone())
 allLinesU.append(lh.Clone())
 #allLinesL[j].Draw()
 #allLinesU[j].Draw()
 if options.signif:
   lsig = ROOT.TLine(options.null,0,options.null,gr.GetYaxis().GetXmax())
   lsig.SetLineColor(1)
   lsig.SetLineStyle(STYLE)
   lsig.SetLineWidth(2)
   allExtLines.append(lsig)
   allExtLines[-1].Draw()

 if options.verb:
 	#fname = (( (names[j].split("/"))[-1] ).split('.'))[0]

 	fname = names[j]
	if options.nofile: fname = ''
 	if options.signif:
	 leg.AddEntry(gr,"%s, %s=%.3f^{-%.3f}_{+%.3f} (%.1f#sigma)"%(fname ,options.xvar,centres[j],centres[j]-lowers[j],uppers[j]-centres[j],signifs[j]),"L")
 	else:
	 leg.AddEntry(gr,"%s, %s=%.3f -%.3f +%.3f"%( fname,options.xvar,centres[j],centres[j]-lowers[j],uppers[j]-centres[j]),"L")
 else: leg.AddEntry(gr,names[j],"L")
 
 for jj in range(len(SANDYLINES)): leg.AddEntry(grEXT[jj],SANDYLINES[jj],"p")

if options.legend: leg.Draw()

if len(grs)==1:
 allLinesL[0].SetLineColor(2)
 allLinesU[0].SetLineColor(2)

LL = ROOT.TLine(gr.GetXaxis().GetXmin(),options.cl,gr.GetXaxis().GetXmax(),options.cl); LL.SetLineColor(2); LL.SetLineWidth(2)
LL.SetLineStyle(2)
if not options.result: LL.Draw()

if len(options.Title)>0:
  print "Add title"
  lat.SetTextSize(0.025)
  lat.DrawLatex(0.1,0.92,"%s"%options.Title)

if options.result:
   c.SetGridx(0) 
   c.SetGridy(0) 
   lat.SetTextSize(0.045)
   lat.SetTextFont(42)
   var = options.xl if options.xl else options.xvar
   if options.verb: lat.DrawLatex(0.5,0.8,"%s = %.2f^{+%.2f}_{-%.2f}"%(var,centres[0],uppers[0]-centres[0],centres[0]-lowers[0]))
   lat.SetTextSize(0.062)
   #lat.DrawLatex(0.1,0.92,"#bf{CMS} #it{Preliminary}")
   lat.DrawLatex(0.18,0.8,"#bf{CMS}")
   lat.SetTextSize(0.034)
   if options.lumilab!="":
     if len(options.lumilab)<10:
       lat.DrawLatex(0.7,0.92,"%s"%options.lumilab)
     else:
       lat.DrawLatex(0.14,0.92,"%s"%options.lumilab)


if options.batch:
  c.SaveAs("%s.pdf"%nam)
  c.SaveAs("%s.png"%nam)
  c.SaveAs("%s.C"%nam)
else:
  raw_input("Done")

outTreeFile.cd()
outTree.Write()

for gr in grs: 
	name = gr.GetName()
	name = name.replace(" ","_")
	name = name.replace(".","_")
	name = name.replace("(","_")
	name = name.replace(")","_")
	print name
	gr.SetName(name)
	gr.Write()

print "central+errors Results saved in", outTreeFile.GetName()
