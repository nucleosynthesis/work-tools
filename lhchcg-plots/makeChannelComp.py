#!/usr/bin/env python 
import array
SANDYLINES = []
def sandy_callback(option, opt_str,value,parser):
	SANDYLINES.append(int(value))

SIG2FILES = {}
def siggy_callback(option, opt_str,value,parser):
	key,val = value.split(":")
	SIG2FILES[int(key)] = val

TEXLABELS = {}
def labels_callback(option, opt_str,value,parser):
	key,val = value.split(":")
	TEXLABELS[key] = val  
from optparse import OptionParser
parser=OptionParser()
parser.add_option("","--xl",default="",type='str')
parser.add_option("","--xr",default="",type='str')
parser.add_option("","--labels",default="",type='str')
parser.add_option("","--groups",default="",type='str')
parser.add_option("","--smcen",default="",type='str')
parser.add_option("","--colors",default="",type='str')
parser.add_option("","--negs",default="",type='str')
parser.add_option("","--styles",default="",type='str')
parser.add_option("","--markers",default="",type='str')
parser.add_option("","--widths",default="",type='str')
parser.add_option("","--msizes",default="",type='str')
parser.add_option("","--combined",default="",type='str')
parser.add_option("","--longStyle",default=False,action='store_true')
parser.add_option("","--sm",default="",type='str')
parser.add_option("-b","--batch",default=False,action='store_true')
parser.add_option("","--addnumber",default=-1,type="int")
parser.add_option("-o","--outname",default="",type='str')
parser.add_option("","--status",default="",type='str')
parser.add_option("-s","--smalllabs",default=False,action='store_true')
parser.add_option("","--supersmalllabs",default=False,action='store_true')
parser.add_option("","--legleft",default=False,action='store_true')
parser.add_option("","--legfilled",default=False,action='store_true')
parser.add_option("","--legdown",default=False,action='store_true')
parser.add_option("","--legVerydown",default=False,action='store_true')
parser.add_option("","--legSuperdown",default=False,action='store_true')
parser.add_option("","--intervals",default=False,action='store_true')
parser.add_option("","--noshift",default=False,action='store_true')
parser.add_option("","--line",type='int',action='callback',callback=sandy_callback)
parser.add_option("","--longline",default="False",action='store_true')
parser.add_option("","--sig2files",type='str',action='callback',callback=siggy_callback)
parser.add_option("","--texlabels",type='str',action='callback',callback=labels_callback)
#parser.add_option("","--negs",type='str',action='callback',callback=negs_callback)
(options,args)=parser.parse_args()

if len(options.labels): options.labels=options.labels.split(",")
if len(options.groups): 
	options.groups=options.groups.split(",")
else: options.groups = ["file %d"%p for p in range(len(args)) ]
if options.smcen: options.smcen = options.smcen.split(",")
import ROOT as r 
r.gROOT.Reset()

loffiles = args[:]
options.noComb=True

COLORS = []
if not options.colors : 
	COLORS = [int(c) for c in range(len(loffiles))]
else: 
   options.colors = options.colors.split(',')
   for i in options.colors:
	if "r." in i : 
		COLORS.append(getattr(r,i.split(".")[-1]))
	else: COLORS.append(int(i))
	#COLORS = [i+1 for i in range(len(args[:]))]
if len(options.markers) >0 :MARKERS = options.markers.split(",")
else: MARKERS = [20+i for i in range(len(args[:]))]
MARKERS = [int(m) for m in MARKERS]
if len(options.msizes) >0 :MSIZES = options.msizes.split(",")
else: MSIZES = [1.2 for i in range(len(args[:]))]
MSIZES = [float(m) for m in MSIZES]
if len(options.styles) > 0 :STYLES = options.styles.split(",")
else: STYLES = [1 for i in loffiles]
STYLES = [int(m) for m in STYLES]
if len(options.widths) > 0 :WIDTHS = options.widths.split(",")
else: WIDTHS = [0 for i in loffiles]
WIDTHS = [float(m) for m in WIDTHS]

if len(options.negs): options.negs = [int(n) for n in options.negs.split(',')] 
else: options.negs = []
# reverse so order goes from top to bottom 
loffiles.reverse()
COLORS.reverse()
MARKERS.reverse()
WIDTHS.reverse()
STYLES.reverse()
MSIZES.reverse()
options.groups.reverse()

def plotMPdfChComp():
  print 'plotting mpdf ChannelComp'
  if not options.noComb: print '\t will assume first file is the global best fit'
  
  points = []

  k=0
  # open the first, it will tell us the number of points in each graph 
  fi = r.TFile.Open(loffiles[0])
  tr = fi.Get("restree")

  ppergraph = tr.GetEntries() #len(loffiles)/options.groups
  ccsize = 0
  TEXsize = 0.033
  #TEXsize = 0.036
  if options.longStyle: 
	canv = r.TCanvas("c","c",1080,1200) 
	ccsize = ppergraph*90
	smallsize = 0.054
	TEXsize = 0.031
  else:
   if ppergraph>3 and ppergraph < 7: 
	canv = r.TCanvas("c","c",480,ppergraph*90) 
	ccsize = ppergraph*90
	smallsize = 0.06
	TEXsize = 0.0313
   elif ppergraph>=7: 
	canv = r.TCanvas("c","c",500,ppergraph*65) 
	ccsize = ppergraph*65
	smallsize = 0.054
	TEXsize = 0.031
   else: 
	canv = r.TCanvas("c","c",420,380) 
	ccsize = 380
	smallsize = 0.035
  if options.supersmalllabs: smallsize*=0.6
  xtitle = "#mu"
  if options.xl: xtitle = options.xl

  XRANGE=[-10,10]
  if options.xr: XRANGE=(options.xr).split(":")
  alllb = range(0,ppergraph+1,1)
  if ppergraph <=3: DD = 0.4
  elif ppergraph <7 : DD = 1.
  else: DD = 1.
  if options.longStyle: 
	DD=1.0
	
  alllb.append(ppergraph+DD)
  spacer=1
  if options.longStyle: 
	alllb.append(ppergraph+DD+DD)
	spacer = 2

  print "ALLL BINS == ", alllb
  bins = array.array('d',alllb)
  xbins = array.array("d",[ float(XRANGE[0]),float(XRANGE[1])])
  print " Arguments ", xbins, ppergraph+spacer, bins
  dummyHist = r.TH2F("dummy_ROOT_SUCKS",";%s;"%xtitle,1,xbins,ppergraph+spacer,bins)
  dummyHist.Draw("axis")
  dummyHist.SetDirectory(0)
  WHITEBOX = r.TBox(dummyHist.GetXaxis().GetXmin()+0.01,ppergraph,dummyHist.GetXaxis().GetXmax()-0.015,ppergraph+spacer*DD-0.02)
  BORDERLINE = r.TLine(dummyHist.GetXaxis().GetXmin(),ppergraph,dummyHist.GetXaxis().GetXmax(),ppergraph)
  
  if options.longStyle: 
	
	dummyHist.GetYaxis().SetTickLength(0.01)
	dummyHist.GetXaxis().SetTickLength(0.015)
	dummyHist.GetYaxis().SetNdivisions(110)
  xtitle = "#sigma/#sigma_{SM}"

  catGraph1sig = [r.TGraphAsymmErrors() for gr in range(len(loffiles))]
  catGraph2sig = [r.TGraphAsymmErrors() for gr in range(len(loffiles))]
  catGraphNsig = [r.TGraphAsymmErrors() for gr in range(len(loffiles))]
  catGraph2Nsig = [r.TGraphAsymmErrors() for gr in range(len(loffiles))]

  lh = 1.2*(0.98-0.78)*(430./float(ccsize))
  lh2 = 1.2*(0.83-0.66)*(430./float(ccsize))
  if len(options.groups) ==1 : 
	lh  = 0.08
	lh2 = 0.08
  if options.longStyle:
        if len(options.groups)>1: 
            leg  =  r.TLegend(0.69,0.8,0.88,0.975)
	else :leg = r.TLegend(0.69,0.975-0.06,0.88,0.975)
  else:
   if options.legleft: 
     if options.legdown:
	leg = r.TLegend(0.30,0.65-lh2,0.552,0.65)
     elif options.legVerydown:
	leg = r.TLegend(0.30,0.5-lh2,0.552,0.5)
     elif options.legSuperdown:
	leg = r.TLegend(0.30,0.38-lh2,0.552,0.38)
     else:
	leg = r.TLegend(0.31,0.865-lh2,0.56,0.865)
   else :
     if options.legdown:
	leg = r.TLegend(0.69,0.65-lh,0.88,0.65)
     elif options.legVerydown: 
	leg = r.TLegend(0.31,0.5-lh2,0.56,0.5)
     else: 
	leg = r.TLegend(0.69,0.98-lh,0.88,0.98)
  leg.SetBorderSize(0)
  if not options.legfilled:
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
  else: 
    leg.SetFillColor(10)
  leg.SetTextSize(0.03)
  leg.SetTextFont(42)
  saveIt = []
  saveIt2 = []
  boxes = []
  boxesnoneg = []

  yvalues = [] # keep track of the order of the points
  for grIndex,fi in enumerate(loffiles):
   dummyHist.Print()
   print "What in the hell?"
   fig = r.TFile.Open(fi)
   tr = fig.Get("restree")
   np = tr.GetEntries()
   grsave = []
   orig_Index = len(loffiles)-grIndex-1 
   for p in range(tr.GetEntries()):
    tr.GetEntry(p)
#    try :
#	tr.r_nl
    point = [tr.r,tr.r_d,tr.r_u,tr.r_nl,tr.r_nu]
#    except: 
#      point = [tr.r,tr.r_d,tr.r_u,-999,-999]
    #grIndex = p//ppergraph
    pIndex = np-p-1
    #pIndex  = p

    if len(loffiles)==1 or options.noshift: yshift=0.5

    elif len(loffiles)%2==0 : # Even
      if grIndex+0.5 > float(len(loffiles))/2: yshift = 0.5 + (grIndex)*(0.25/len(loffiles))
      else: yshift = 0.5 - (grIndex+1)*(0.25/len(loffiles))
    else :
      if grIndex == (len(loffiles)-1)/2 :yshift=0.5- (grIndex+1)*0.14/len(loffiles)
      elif grIndex > float(len(loffiles))/2: yshift = 0.5 + grIndex*0.16/len(loffiles)
      else :yshift = 0.5 - (grIndex+1)*0.65/len(loffiles)

      print "Setting grIndex (col), ", grIndex, COLORS[grIndex], yshift 
    
    if pIndex==0: yvalues.append([yshift,grIndex])

    catGraph1sig[grIndex].SetPoint(pIndex,point[0],pIndex+yshift)
    catGraph1sig[grIndex].SetPointError(pIndex,point[1],point[2],float(WIDTHS[grIndex])/2,float(WIDTHS[grIndex])/2)

    if (point[3]==point[4]): centrenegative = -999  # note, don't move it outside yet
    else : centrenegative = (point[3]+point[4])/2
    catGraphNsig[grIndex].SetPoint(pIndex,centrenegative,pIndex+yshift)
    catGraphNsig[grIndex].SetPointError(pIndex,abs(centrenegative-point[3]),abs(centrenegative-point[4]),float(WIDTHS[grIndex])/2,float(WIDTHS[grIndex])/2)

    catGraph1sig[grIndex].SetName("best_fit_%s"%fi.rstrip(".root"))
    if catGraph2sig[grIndex]: catGraph2sig[grIndex].SetName("best_fit_2sig_%s"%fi.rstrip(".root"))
    if catGraphNsig[grIndex]: catGraphNsig[grIndex].SetName("negative_scans_%s"%fi.rstrip(".root"))
    if catGraph2Nsig[grIndex]: catGraph2Nsig[grIndex].SetName("negative_scans_2sig_%s"%fi.rstrip(".root"))

 
    binLabel = "?"
    if len(SIG2FILES.keys()) and orig_Index in SIG2FILES.keys():

      ft = r.TFile.Open(SIG2FILES[orig_Index])
      trt = ft.Get("restree")
      trt.GetEntry(p)
      #try :
	#tr.r_nl
      sig2point = [trt.r,trt.r_d,trt.r_u,trt.r_nl,trt.r_nu]
      #except: 
      # sig2point = [trt.r,trt.r_d,trt.r_u,-999,-999]

      catGraph2sig[grIndex].SetPoint(pIndex,sig2point[0],pIndex+yshift)
      catGraph2sig[grIndex].SetPointError(pIndex,sig2point[1],sig2point[2],float(WIDTHS[grIndex])/10,float(WIDTHS[grIndex])/10)
	
      print "Check if 2-sigma exists " , options.groups[grIndex], options.labels[p], sig2point[3],sig2point[4]
      if sig2point[3]!=sig2point[4]: 
            centrenegative = (sig2point[3]+sig2point[4])/2
            print "Adding -ve 2-sigma range for " , options.groups[grIndex], options.labels[p], abs(centrenegative-sig2point[3]),abs(centrenegative-sig2point[4])
      catGraph2Nsig[grIndex].SetPoint(pIndex,centrenegative,pIndex+yshift)
      #catGraph2Nsig[grIndex].SetPointError(pIndex,abs(centrenegative-sig2point[3]),abs(centrenegative-sig2point[4]),float(WIDTHS[grIndex])/10,float(WIDTHS[grIndex])/10)
      catGraph2Nsig[grIndex].SetPointError(pIndex,abs(centrenegative-sig2point[3]),abs(centrenegative-sig2point[4]),0,0)
            
    else: 
      catGraph2sig[grIndex]=0
      catGraph2Nsig[grIndex]=0

    # check in fact if the parameter can be negative otherwise put a hatched box
    #if icentrenegative < -900 and orig_Index == options.negs:    
    if orig_Index==0 and p in options.negs:
	bWIDT =  (dummyHist.GetYaxis().GetBinWidth(pIndex+1))/2
	bCEN  =  dummyHist.GetYaxis().GetBinCenter(pIndex+1)
	print "THIS GUY IS ", pIndex
	#HATCHBOX = r.TBox(dummyHist.GetXaxis().GetXmin(),dummyHist.GetYaxis().GetBinLowEdge(pIndex),0,dummyHist.GetYaxis().GetBinLowEdge(pIndex+1))
	HATCHBOX = r.TBox(dummyHist.GetXaxis().GetXmin(),bCEN-bWIDT,0,bCEN+bWIDT)
	HATCHBOX.SetFillStyle(3344)
	HATCHBOX.SetFillColor(r.kGray)
	boxesnoneg.append(HATCHBOX)

    if (len(loffiles)-grIndex-1 == 0 and options.addnumber==-1) or (options.addnumber >-1 and options.addnumber==len(loffiles)-grIndex-1): 
	
      if options.labels : binLabel =  options.labels[p]
      if options.addnumber >-1 : binLabel+="=%.2f^{+%.2f}_{-%.2f}"%(point[0],point[2],point[1])

      grsave.append([pIndex+yshift,point])
      if ppergraph<=3: 
	if options.smalllabs:  dummyHist.GetYaxis().SetLabelSize(2*smallsize)
	else: dummyHist.GetYaxis().SetLabelSize(0.1)
      else : 
	if options.smalllabs: 
		dummyHist.GetYaxis().SetLabelSize(smallsize)
	else: dummyHist.GetYaxis().SetLabelSize(0.075)
      dummyHist.GetYaxis().SetBinLabel(pIndex+1,binLabel)

    
    bhalfwidth = 0.15*dummyHist.GetYaxis().GetBinWidth(pIndex+1)/len(loffiles)
    box = r.TBox(dummyHist.GetXaxis().GetXmin(),pIndex+yshift-bhalfwidth,dummyHist.GetXaxis().GetXmax(),pIndex+yshift+bhalfwidth)
    box.SetLineColor(1)
    box.SetFillColor(r.kGreen-6)
    box.SetFillStyle(3001)
    if tr.flag==1: boxes.append(box)
    print options.groups[grIndex], binLabel, point[0],"-"+str(point[1]),"+"+str(point[2])
    
   saveIt.append(grsave)

   catGraph1sig[grIndex].SetLineColor(COLORS[grIndex])
   if not options.longStyle: catGraph1sig[grIndex].SetLineWidth(3)
   catGraph1sig[grIndex].SetLineStyle(STYLES[grIndex])
   if not options.longStyle: catGraph1sig[grIndex].SetLineWidth(3)
   catGraph1sig[grIndex].SetMarkerStyle(MARKERS[grIndex])
   catGraph1sig[grIndex].SetMarkerColor(COLORS[grIndex])
   #catGraph1sig[grIndex].SetFillColor(COLORS[grIndex])
   if options.noshift:
   	catGraph1sig[grIndex].SetFillColor(0)
	catGraph1sig[grIndex].SetFillStyle(0)
   else: 
        catGraph1sig[grIndex].SetFillColor(COLORS[grIndex])

   catGraph1sig[grIndex].SetMarkerSize(MSIZES[grIndex])

   if catGraph2sig[grIndex]!=0:
	   catGraph2sig[grIndex].SetLineColor(COLORS[grIndex])
	   catGraph2sig[grIndex].SetLineWidth(2)
	   catGraph2sig[grIndex].SetLineStyle(STYLES[grIndex])
	   catGraph2sig[grIndex].SetLineWidth(1)
	   catGraph2sig[grIndex].SetMarkerStyle(MARKERS[grIndex])
	   catGraph2sig[grIndex].SetMarkerColor(COLORS[grIndex])
	   if options.noshift:
		catGraph2sig[grIndex].SetFillColor(0)
		catGraph2sig[grIndex].SetFillStyle(0)
	   else: 
		catGraph2sig[grIndex].SetFillColor(COLORS[grIndex])
	   catGraph2sig[grIndex].SetMarkerSize(0)

   catGraphNsig[grIndex].SetLineColor(COLORS[grIndex])
   catGraphNsig[grIndex].SetLineWidth(3)
   catGraphNsig[grIndex].SetLineStyle(STYLES[grIndex])
   catGraphNsig[grIndex].SetLineWidth(3)
   catGraphNsig[grIndex].SetMarkerStyle(20)
   catGraphNsig[grIndex].SetMarkerColor(COLORS[grIndex])
   #catGraphNsig[grIndex].SetFillColor(COLORS[grIndex])
   catGraphNsig[grIndex].SetMarkerSize(0)


   if catGraph2Nsig[grIndex]!=0:
     catGraph2Nsig[grIndex].SetLineColor(COLORS[grIndex])
     catGraph2Nsig[grIndex].SetLineWidth(3)
     catGraph2Nsig[grIndex].SetLineStyle(STYLES[grIndex])
     catGraph2Nsig[grIndex].SetLineWidth(1)
     catGraph2Nsig[grIndex].SetMarkerStyle(20)
     catGraph2Nsig[grIndex].SetMarkerColor(COLORS[grIndex])
     #catGraph2Nsig[grIndex].SetFillColor(COLORS[grIndex])
     catGraph2Nsig[grIndex].SetMarkerSize(0)

  
   #leg.AddEntry(catGraph1sig[grIndex],options.groups[grIndex],"L")

  dummyHist.Draw()
  yvalues.sort(); yvalues.reverse() 
  for y in yvalues:
   leg.AddEntry(catGraph1sig[y[1]],options.groups[y[1]],"PL")
  if len(loffiles)>1: 
   THLINE = r.TH1F("obj","",1,0,1); THLINE.SetLineColor(1); THLINE.SetLineWidth(3)
   TLINE  = r.TH1F("obj","",1,0,1); TLINE.SetLineColor(1); TLINE.SetLineWidth(1)
   if len(options.negs) or options.intervals :leg.AddEntry(THLINE,"1#kern[0.2]{#sigma} interval","L") 
   else: leg.AddEntry(THLINE,"#pm1#kern[0.2]{#sigma}","L") 
   if len(SIG2FILES)>0:
   	if len(options.negs) or options.intervals:leg.AddEntry(TLINE,"2#sigma interval","L") 
   	else: leg.AddEntry(TLINE,"#pm2#sigma","L") 

  #if options.pink : for b in boxes: b.Draw()

  if len(options.combined): 

	fcomb = r.TFile.Open(options.combined)
	tree_c = fcomb.Get("restree")
	tree_c.GetEntry(0)
	XC = tree_c.r
	XCU = tree_c.r_u
	XCD = tree_c.r_d
        print "#mu=%.1f^{+%.1f}_{-%.1f}"%(XC,XCU,XCD)
        CLine = r.TLine(XC,0,XC,ppergraph)
	CLine.SetLineWidth(2)
	CBOX = r.TBox(XC-XCD,0,XC+XCU,ppergraph)
	CBOX.SetFillColor(r.kGray)
	latC = r.TLatex()
	latC.SetNDC()
	CBOX.Draw()
	CLine.Draw()
	latC.SetTextSize(0.04)
	latC.SetTextFont(42)
	#latC.DrawLatex(0.62,0.4,"#mu=%.1f^{+%.1f}_{-%.1f}"%(XC,XCU,XCD))

  smboxes = []
  if len(options.sm):
	fsm = r.TFile.Open(options.sm)
	tree_c = fsm.Get("restree")
	np = tree_c.GetEntries()
	for i in range(np):
		tree_c.GetEntry(i)
		rl = 1.-tree_c.r_d
		rh = 1.+tree_c.r_u
    		pIndex = np-i-1
	        phwidth = 0.3*dummyHist.GetYaxis().GetBinWidth(pIndex+1)
    		box = r.TBox(rl,pIndex+0.5-phwidth,rh,pIndex+0.5+phwidth)
		box.SetLineColor(1)
		box.SetFillColor(r.kGreen-6)
		smboxes.append(box)
		box.Draw()
	grDumm = r.TH1F("noonecares","",1,0,1)
	grDumm.SetFillColor(r.kGreen-6)
	grDumm.SetLineColor(0)
	leg.AddEntry(grDumm,"Th. uncert.","F")	

  if len(options.negs): 
	for b in boxesnoneg : b.Draw()

  if not len(options.smcen) :
	T = r.TLine(1,0,1,ppergraph)
  else : 
	T = r.TLine(1,float(options.smcen[0]),1,float(options.smcen[1]))
  T.SetLineColor(1)
  T.SetLineWidth(2)
  T.SetLineStyle(2)
  T.Draw()

  SANDB = []
  for s in SANDYLINES:
	xxmin = dummyHist.GetXaxis().GetXmin()
	xxmax = dummyHist.GetXaxis().GetXmax()
	#if options.longline:
	#	xxmin = xxmin-0.1*(xxmax-xxmin)
	TT = r.TLine(xxmin,np-s,xxmax,np-s)
	TT.SetLineColor(1)
	TT.SetLineWidth(3)
	TT.SetLineStyle(1)
	#if options.longline: TT.SetLineStyle(3)
	SANDB.append(TT)
	TT.Draw()
 
  for gr in range(len(loffiles)):
    if options.noshift or options.longStyle: catGraph1sig[gr].Draw("5Psame")
    else: 
	catGraph1sig[gr].Draw("5Psame")
	#catGraph1sig[gr].Draw("PZsame")
    if catGraphNsig[gr]!=0:
	catGraphNsig[gr].Draw("5same")
    if catGraph2sig[gr]!=0:
	catGraph2sig[gr].Draw("5same")
    if catGraph2Nsig[gr]!=0:
	catGraph2Nsig[gr].Draw("5same")

    #catGraph1sig[gr].Draw("XPsame")
    #if catGraphNsig[gr] !=0 :
	
  if options.addnumber >-1 and len(options.groups)==1:
    latsmall = r.TLatex()
    latsmall.SetTextAlign(32)
    latsmall.SetTextFont(42)
    latsmall.SetTextSize(0.035)
    latbig = r.TLatex()
    latbig.SetTextAlign(32)
    latbig.SetTextFont(42)
    latbig.SetTextSize(0.04)

    for g,GR in enumerate(saveIt):
     for sav in saveIt:
      point = sav[1]
      y=sav[0]
      #sav2 = saveIt2[s]
      #latbig.DrawLatex(sav2[1],sav2[2], sav2[0])
      latsmall.SetTextColor(COLORS[gr])
      RNGE = dummyHist.GetXaxis().GetXmax() - dummyHist.GetXaxis().GetXmin()
      latsmall.DrawLatex(dummyHist.GetXaxis().GetXmax()-0.1*RNGE,y, "%.2f^{+%.2f}_{-%.2f}"%(point[0],point[2],point[1]))
 
  
  r.gStyle.SetOptStat(0)
  cacheErrSize = r.gStyle.GetEndErrorSize()
  cachePadLeft = canv.GetLeftMargin()
  cachePadRight = canv.GetRightMargin()
  r.gStyle.SetEndErrorSize(8.)
  canv.SetLeftMargin(cachePadLeft+0.16); # was 0.18
  canv.SetRightMargin(cachePadRight-0.06); # was 0.05
  canv.SetTopMargin(0.012); # was 0.05
  canv.SetGridx(False)
  canv.SetGridy(False)
  canv.Modified()
  canv.Update()
  canv.RedrawAxis()

  lat = r.TLatex()
  lat.SetTextFont(42)
  lat.SetTextSize(TEXsize)
  lat.SetNDC()
  WHITEBOX.SetFillColor(10)
  WHITEBOX.Draw()
  if options.longStyle:
   if options.status   == "PRELIMINARY": lat.DrawLatex(0.28,0.935,"#splitline{#bf{#it{ATLAS}} and #bf{#it{CMS}} Preliminary}{#bf{#it{LHC}} Run 1}")
   elif options.status == "INTERNAL":  lat.DrawLatex(0.28,0.935,"#splitline{#bf{#it{ATLAS}} and #bf{#it{CMS}} Internal}{#bf{#it{LHC}} Run 1}")
   elif options.status == "PAPER":     lat.DrawLatex(0.28,0.935,"#splitline{#bf{#it{ATLAS}} and #bf{#it{CMS}}}{#bf{#it{LHC}} Run 1}")
   BORDERLINE.SetLineWidth(1)
   BORDERLINE.Draw()
  else:
   if options.status   == "PRELIMINARY":  lat.DrawLatex(0.28,0.93,"#splitline{#bf{#it{ATLAS}} and #bf{#it{CMS}} Preliminary}{#bf{#it{LHC}} Run 1}")
   elif options.status == "INTERNAL":   lat.DrawLatex(0.28,0.93,"#splitline{#bf{#it{ATLAS}} and #bf{#it{CMS}} Internal}{#bf{#it{LHC}} Run 1}")
   elif options.status == "PAPER":      lat.DrawLatex(0.28,0.93,"#splitline{#bf{#it{ATLAS}} and #bf{#it{CMS}}}{#bf{#it{LHC}} Run 1}")
  #if len(loffiles)>1: 
  leg.Draw()
  if not options.longStyle: canv.RedrawAxis()


  # Finally: 
  if len(TEXLABELS.keys()): 
  	rlat = r.TLatex()
  	rlat.SetTextFont(42)
	rlat.SetTextAngle(90)
  	rlat.SetTextSize(TEXsize*1.5)
  	rlat.SetNDC()
	for LAB in TEXLABELS.keys():
	  x,y = TEXLABELS[LAB].split(",")
	  rlat.DrawLatex(float(x),float(y),LAB)

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
