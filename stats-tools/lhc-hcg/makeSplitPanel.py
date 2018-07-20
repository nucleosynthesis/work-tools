# script to make the 5x5 summary plot for LHC-HXSWG couplings paper

#!/usr/bin/env python 
import array
import sys

import ROOT as r 

from optparse import OptionParser
parser=OptionParser()
parser.add_option("","--xl",default="",type='str')
parser.add_option("","--xr",default="",type='str')
parser.add_option("","--labels",default="",type='str')
parser.add_option("","--panellabels",default="",type='str')
parser.add_option("","--colors",default="1",type='str')
parser.add_option("","--styles",default="1",type='str')
parser.add_option("","--markers",default="20",type='str')
parser.add_option("","--widths",default="0.0005",type='str')
parser.add_option("","--msizes",default="0.75",type='str')
parser.add_option("","--lhc",default="",type='str')
parser.add_option("","--dashes",default="",type='str')
parser.add_option("","--status",default="",type='str')
parser.add_option("","--sm",default="",type='str')
parser.add_option("-o","--outname",default="",type='str')

(options,args)=parser.parse_args()
loffiles=[1]

#options.panellabels = "BR^{#gamma#gamma},BR^{ZZ},BR^{WW},BR^{#tau#tau},BR^{bb}"
#options.labels = "#sigma_{ggF},#sigma_{VBF},#sigma_{WH},#sigma_{ZH},#sigma_{ttH}"
options.labels = "#gamma#gamma,ZZ,WW,#tau#tau,bb"
options.panellabels = "ggF,VBF,WH,ZH,ttH"

options.labels = options.labels.split(",")
options.panellabels = options.panellabels.split(",")
options.dashes = [int(d) for d in ((options.dashes).split(','))]


r.gStyle.SetOptStat(0)
r.gROOT.SetBatch(1)

# reverse so order goes from top to bottom 
# now make a gigantic canvas 
ppergraph = 5 #len(loffiles)/options.groups
ccsize = 0
TEXsize = 0.033
#TEXsize = 0.036

XRANGE=[
	 [-0.9,1.9]
	,[-0.9,1.9]
	,[-5.9,8.9]
	,[-5.9,8.9]
	,[-5.9,8.9]
       ]

alllb = range(0,ppergraph+1,1)
DD = 1.
alllb.append(ppergraph+DD)
#xtitle = "#mu"

dummyHists = []
for i in range(0,5):
 bins = array.array('d',alllb)
 xbins = array.array("d",[ float(XRANGE[i][0]),float(XRANGE[i][1])])
 dummyHist = r.TH2F("dummy",";;",1,xbins,ppergraph+1,bins) 
 dummyHist.GetYaxis().SetLabelSize(0.15)
 dummyHist.GetYaxis().SetLabelOffset(0.02)
 dummyHist.GetXaxis().SetLabelSize(0.08)
 dummyHist.GetXaxis().SetNdivisions(010)
 dummyHist.GetXaxis().SetLabelOffset(-0.01)
 dummyHist.GetXaxis().SetTickLength(0.01)
 dummyHists.append(dummyHist.Clone())

canv = r.TCanvas("c","c",800,ppergraph*90) 
ccsize = ppergraph*90
smallsize = 0.06
TEXsize = 0.0313

catGraph1sig   = [r.TGraphAsymmErrors() for i in range(0,5)]

fig = r.TFile.Open(options.lhc)
tr = fig.Get("restree")
np = tr.GetEntries()
grsave = []
grIndex =0 

smboxes = [[] for i in range(0,5)]
drawboxes = [[] for i in range(0,5)]
for p in range(tr.GetEntries()):
 grIndex = p//5
 print grIndex, len(catGraph1sig)
 tr.GetEntry(p)
 point = [tr.r,tr.r_d,tr.r_u,tr.r_nl,tr.r_nu]
 pIndex = 5-(p%5)-1
 yshift=0.5

 dummyHist = dummyHists[grIndex]
 
 if p in options.dashes: 
   catGraph1sig[grIndex].SetPoint(pIndex,-999,pIndex+yshift)
   catGraph1sig[grIndex].SetPointError(pIndex,0,0,0,0)
   bWIDT =  (dummyHist.GetYaxis().GetBinWidth(pIndex+1))/2
   bCEN  =  dummyHist.GetYaxis().GetBinCenter(pIndex+1)
   HATCHBOX = r.TBox(dummyHist.GetXaxis().GetXmin(),bCEN-bWIDT,dummyHist.GetXaxis().GetXmax(),bCEN+bWIDT)
   HATCHBOX.SetFillStyle(3344)
   HATCHBOX.SetFillColor(r.kGray)
   drawboxes[grIndex].append(HATCHBOX)
   
 else:
  catGraph1sig[grIndex].SetPoint(pIndex,point[0],pIndex+yshift)
  catGraph1sig[grIndex].SetPointError(pIndex,point[1],point[2],float(options.widths)/2,float(options.widths)/2)
 if options.labels : binLabel =  options.labels[p%5]
 else: binLabel = "Yo"
 print "Setting ", pIndex+1
 dummyHist.GetYaxis().SetBinLabel(pIndex+1,binLabel)

 catGraph1sig[grIndex].SetLineColor(int(options.colors))
 catGraph1sig[grIndex].SetLineWidth(1)
 catGraph1sig[grIndex].SetLineStyle(int(options.styles))
 catGraph1sig[grIndex].SetLineWidth(1)
 catGraph1sig[grIndex].SetMarkerStyle(int(options.markers))
 catGraph1sig[grIndex].SetMarkerSize(float(options.msizes))
 catGraph1sig[grIndex].SetMarkerColor(int(options.colors))

if len(options.sm):
	fsm = r.TFile.Open(options.sm)
	tree_c = fsm.Get("restree")
	np = tree_c.GetEntries()
	for p in range(np):
 		grIndex = p//5
 		pIndex = 5-(p%5)-1
 		yshift=0.5
		tree_c.GetEntry(p)
		rl = 1.-tree_c.r_d
		rh = 1.+tree_c.r_u
		print "Theory uncertainty on %s %s = "%(options.panellabels[grIndex],options.labels[p%5]), tree_c.r_d 
	        phwidth = 0.1*dummyHist.GetYaxis().GetBinWidth(pIndex+1)
    		box = r.TBox(rl,pIndex+0.5-phwidth,rh,pIndex+0.5+phwidth)
		box.SetLineColor(1)
		box.SetFillColor(r.kGreen-6)
		if not  p in options.dashes:	smboxes[grIndex].append(box)


allPads = []
for i in range(0,5):
 #if i==0: pad1 = r.TPad("p1","p1",0.+i*0.18,0.005,0.08+i*0.18+0.18,0.92)
 #else: pad1 = r.TPad("p1","p1",0.08+i*0.18,0.005,0.08+i*0.18+0.18,0.92)
 pad1 = r.TPad("p1","p1",0.08+i*0.18,0.005,0.08+i*0.18+0.18,0.92)
 #if i>0: pad1.SetLeftMargin(0)
 #else :pad1.SetLeftMargin(0.34)
 pad1.SetLeftMargin(0)
 pad1.SetRightMargin(0)
 pad1.SetTopMargin(0.02)
 pad1.SetBottomMargin(0.22)
 pad1.SetCanvas(canv)
 pad1.Draw()
 allPads.append(pad1)

allLines = []
allboxes = []
print allPads 

for i in range(0,5):
 allPads[i].cd()
 dummyHists[i].Draw()
 for dr in smboxes[i]: dr.Draw()
 catGraph1sig[i].Draw("5p")
 T = r.TLine(1,0,1,ppergraph)
 T.SetLineStyle(2)
 T.Draw()
 for dr in drawboxes[i]: dr.Draw()
 allLines.append(T)
 allPads[i].RedrawAxis()

canv.cd()
panlatex = r.TLatex()
panlatex.SetNDC()
panlatex.SetTextFont(42)
panlatex.SetTextSize(0.12)

for i in range(0,5):
  allPads[i].cd()
  panlatex.DrawLatex(0.4,0.1,options.panellabels[i])	

#panlatex.SetNDC(Fa)
canv.cd()
panlatex.SetTextSize(0.04)

for i in range(0,5):
  y = 0.2 + 1.1*dummyHists[i].GetYaxis().GetBinCenter(i+1)/10
  panlatex.DrawLatex(0.036,y,options.labels[4-i])	

canv.cd()
WHITEBOX = r.TBox(0.2,0.785,0.86,.9)
WHITEBOX.SetFillColor(10)
WHITEBOX.SetLineColor(1)
WHITEBOX.Draw()
TBORDER = r.TLine(0.08,0.785,0.979,0.785)
TBORDER.SetLineColor(1)
TBORDER.SetLineWidth(1)
TBORDER.Draw()


leg = r.TLegend(0.7,0.80,0.92,0.89)
leg.SetFillColor(0)
leg.SetFillStyle(0)
leg.SetBorderSize(0)
leg.AddEntry(catGraph1sig[0],"Observed #pm1#kern[0.2]{#sigma}","PL")
leg.Draw()

if options.sm:
 grDumm = r.TH1F("noonecares","",1,0,1)
 grDumm.SetFillColor(r.kGreen-6)
 grDumm.SetLineColor(0)
 leg.AddEntry(grDumm,"Th. uncert.","F")	

lat = r.TLatex()
lat.SetTextFont(42)
lat.SetTextSize(0.04)
lat.SetNDC()

#lat.DrawLatex(0.1,0.825,"#splitline{#bf{#it{ATLAS}} and #bf{#it{CMS}} Internal}{#bf{#it{LHC}} Run 1}")
if options.status   == "PRELIMINARY": lat.DrawLatex(0.1,0.825,"#splitline{#bf{#it{ATLAS}} and #bf{#it{CMS}} Preliminary}{#bf{#it{LHC}} Run 1}")
elif options.status == "INTERNAL":    lat.DrawLatex(0.1,0.825,"#splitline{#bf{#it{ATLAS}} and #bf{#it{CMS}} Internal}{#bf{#it{LHC}} Run 1}")
elif options.status == "PAPER":       lat.DrawLatex(0.1,0.825,"#splitline{#bf{#it{ATLAS}} and #bf{#it{CMS}}}{#bf{#it{LHC}} Run 1}")

labelTex = r.TLatex()
labelTex.SetTextFont(42)
labelTex.SetTextSize(0.04)
labelTex.SetNDC()
labelTex.DrawLatex(0.7,0.04,"#sigma #upoint B norm. to SM prediction")
#labelTex.SetTextAngle(90)
#labelTex.DrawLatex(0.02,0.6,"Production Mode")
canv.SaveAs("%s.pdf"%options.outname)
canv.SaveAs("%s.png"%options.outname)
canv.SaveAs("%s.C"%options.outname)
#raw_input()
