# No need to edit these after unblinding has already happened 
BLINDFACTOR = 1.
REBINFACTOR = 1

####################### SETTINGS TO DEFINE HARDCODED ############################################################
# ideally we should include ~20% on the V+jets background estimate when doing the QCD, here is where we define it 
from collections import OrderedDict
BKGSYS = OrderedDict()
BKGSYS["Noise"] = 0.20
BKGSYS["Wjets"] = 0.20
BKGSYS["Zjets"] = 0.20
BKGSYS["Rest"]  = 0.00

# for the uncertainties from the fit we throw toys, define here the number to use 
NTOYS=500

# max mjj that we plot (its not really a maximum)
XMAX= 5000 
######################### LEAVE BELOW HERE ALONE ################################################################

# Command line option
from optparse import OptionParser
parser=OptionParser()
parser.add_option("","--function",default=2,type=int, help="Define function to be used for mindphi fit (see top of code for functions, defined in makeFunction)")
parser.add_option("","--ymin",default=0.001,type=float, help="Minimum y-value on plots for resulting m_jj QCD distributions - note, its a log plot")
parser.add_option("","--ymax",default=1000.,type=float, help="Maximum y-value on plots for resulting m_jj QCD distributions - note, its a log plot")
parser.add_option("","--mjj_min",default=200.,type=float, help="Minimum m_jj used in analysis (eg VTR=900, MTR=200) - need this to make histograms correctly")
parser.add_option("","--string",default="",type=str, help="Add a string (eg MTR 2017) to add to plots and also for naming output files")
parser.add_option("","--logy",default=False,action='store_true',help="Log-y scale for the fits (reccomended)")
parser.add_option("","--mkworkspace",default=False,action='store_true',help="Actually produce the workspace for combine at the end - don't run unless you use the reccomended CMSSW version!")
parser.add_option("","--fit_min",default=0. ,type=float,help="Minimum value for the fit range in mindphi(j,MET)")
parser.add_option("","--fit_max",default=1.0,type=float,help="Maximum value for the fit range in mindphi(j,MET)")
parser.add_option("","--sr_cut",default=0.5,type=float,help="Definition of mindphi(j,MET) cut for SR (MTR should be 0.5, VTR should be 1.8) - important to get correct normalisation")
parser.add_option("","--max_blind",default=3.5,type=float,help="Data above this value will be blinded in the mindphi(j,MET) plots - default is not to blind")

parser.add_option("","--label",default="",type=str, help="Add a string (eg MTR 2017) to add to plots and also for naming output files")
(options,args)=parser.parse_args()
if len(args) < 1: sys.exit("Error - run with mkQCD.py inputfile.root [options]")


import sys 
from scipy.optimize import minimize
import array
import numpy

import gc 
gc.disable()

import ROOT

R = ROOT.TRandom3()
origStat = ROOT.gStyle.GetOptStat()
ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
ROOT.gROOT.ForceStyle(0)


fin = ROOT.TFile.Open(args[0])

fout = ROOT.TFile("%s_qcdDD.root"%fin.GetName(),"RECREATE")
wspace = ROOT.RooWorkspace()
wspace.SetName("qcd_wspace")
pdir = fout.mkdir("Plots")
# Remap options
SELECTFUNC = int(options.function) 

ymin = float(options.ymin)
ymax = float(options.ymax)
xmin = float(options.mjj_min)

mystring = options.label
LOGY = int(options.logy)
MINFIT = float(options.fit_min)
MAXFIT = float(options.fit_max)
MAXBLIND = float(options.max_blind)

CUT = float(options.sr_cut)


AllBackgrounds = OrderedDict()
# Don't change this order!
AllBackgrounds["Noise"]= ["HFNoise_CR","HFTemplate_CR"]
AllBackgrounds["Wjets"]= ["WJETS_CR","EWKW_CR"]
AllBackgrounds["Zjets"]= ["ZJETS_CR","EWKZNUNU_CR","EWKZll_CR","DY_CR"]
AllBackgrounds["Rest"] = ["TOP_CR","VV_CR"]

scale_factor = OrderedDict()
scale_factor["Noise"] = 1.
scale_factor["Wjets"] = 1.
scale_factor["Zjets"] = 1.

# should be the same number as the number of scale_factors
nNuisance = 3

def getBackgrounds(fdphi):
  backgrounds  = []
  for bkg in AllBackgrounds.items():
    hsaved = 0
    for hn in bkg[1]:
      #print "Looking  for histogram ",hn, " -> ",bkg[0]
      h = fdphi.Get(hn)
      try: 
        checkname = h.GetName()
        if hsaved==0: hsaved=h.Clone()
        else: hsaved.Add(h)
      except :
        pass
    hsaved.SetName(bkg[0]+"_"+hsaved.GetName())
    backgrounds.append(hsaved)
  return backgrounds

def reformTotal(total,backs,sfs,verb=False):
  if verb: 
    print "Creating (post-fit) total from -> "
    for i  in range(len(backs)): print backs[i].GetName(),sfs[i]
  for b in range(total.GetNbinsX()):
    bi = sum([bkg.GetBinContent(b+1)*sf for bkg,sf in zip(backs,sfs)])
    total.SetBinContent(b+1,bi)

npar=[0]
def makeFunction(name, WHICH,  mini,maxi, prestring=""): 
   """
   0 => the background MC fit function
   1 => the qcd component with exponential form 
   2 => the qcd component with gaussian form
   To make the sum, add the prestring to 1 or 2 
   """
   if WHICH==1:
     ret = ROOT.TF1(name,"[0]*exp(-[1]*x)",mini,maxi); 
     ret.SetParameter(1,2)
     npar[0] = 2

   elif WHICH==2:
     ret = ROOT.TF1(name,"[0]*exp(-1*(x-[1])*(x-[1])/(2*[2]*[2]))",mini,maxi);
     ret.SetParameter(1,-2.)
     ret.SetParameter(2,1.)
     npar[0] = 3
   
   elif WHICH==3:
     ret = ROOT.TF1(name,"[0]*exp(-1*(x-[1])*(x-[1])/(2*[2]*[2]))+[3]*exp(-[4]*x)",mini,maxi);
     ret.SetParameter(1,-2.)
     ret.SetParameter(2,1.)
     ret.SetParameter(3,10.)
     ret.SetParameter(4,-1.)
     npar[0] = 5

   return ret 
def rebin(h,bins):

  hbinned = hnew.Clone();  hnew.SetName(hnew.GetName() + "_rebinned")
  hbinned = hnew.Rebin(len(bins)-1,hnew.GetName() + "_rebinned",array.array('d',bins))
  return hbinned

def makehist(h): 
  hnew = h.Clone(); hnew.SetName("%s_hist"%h.GetName())
  hnew.GetYaxis().SetTitle("Events/GeV")
  for b in range(1,h.GetNbinsX()+1): 
    bc = h.GetBinContent(b)
    bw = h.GetBinWidth(b)
    be = h.GetBinError(b)
    hnew.SetBinContent(b,bc/bw)
    hnew.SetBinError(b,be/bw)
  
  return hnew

def makebinned(h): 
  hnew = h.Clone(); hnew.SetName("%s_counts"%h.GetName())
  hnew.GetYaxis().SetTitle("Events")
  for b in range(1,h.GetNbinsX()+1): 
    bc = h.GetBinContent(b)
    bw = h.GetBinWidth(b)
    be = h.GetBinError(b)
    hnew.SetBinContent(b,bc*bw)
    hnew.SetBinError(b,be*bw)
  
  return hnew

def binFunction(h, f,xmin=-999,xmax=-999,addhist=None): 
  
  hnew = h.Clone(); hnew.SetName("%s_fitted_%s"%(h.GetName(),f.GetName()))
  for i in range(1,h.GetNbinsX()+1):
    bc =  h.GetBinCenter(i)
    bw = h.GetBinWidth(i)

    valued = f.Integral(h.GetBinLowEdge(i), h.GetBinLowEdge(i)+bw)
    if xmin>=-900 and bc < xmin : valued = 0 
    if xmax>=-900 and bc > xmax : valued = 0 
    if valued < 0: hnew.SetBinContent(i,0)
    else: hnew.SetBinContent(i,valued/bw)
    hnew.SetBinError(i,0)
  hnew.SetLineColor(f.GetLineColor())
  hnew.SetLineWidth(2)
  if addhist!=None: hnew.Add(addhist)
  return hnew 

def chopHistogram(h, xmin=-999,xmax=-999): 
  
  hnew = h.Clone(); hnew.SetName("%s_choopedup"%(h.GetName()))
  for i in range(1,h.GetNbinsX()+1):
    bc =  h.GetBinCenter(i)
    bw = h.GetBinWidth(i)

    valued = h.GetBinContent(i) 
    #print valued, h.GetBinLowEdge(i), bw
    if xmin>=-900 and bc < xmin : valued = 0 
    if xmax>=-900 and bc > xmax : valued = 0 
    if valued < 0: hnew.SetBinContent(i,0)
    else: hnew.SetBinContent(i,valued)
    #if f.Eval(h.GetBinCenter(i)) < 0 : hnew.SetBinContent(i,0)
    #else: hnew.SetBinContent(i,f.Eval(h.GetBinCenter(i)))
  #hnew.SetLineWidth(2)
    hnew.SetBinError(i,h.GetBinError(i))
  return hnew 
      
    
def fixHistogram(h): 
  
  bins = []
  vals = []
  errs = []

  for b in range(1,h.GetNbinsX()+1): 
    if h.GetBinLowEdge(b)<options.mjj_min: 
      continue
    bins.append(h.GetBinLowEdge(b))
    # Use garwood interval for 0 entries (otherwise, will be 0) 
    if h.GetBinContent(b)>0 : 
     vals.append(h.GetBinContent(b))
     errs.append(h.GetBinError(b))
    else: 
     #print "Bin content = ", b, h.GetBinContent(b)
     vals.append(0)
     errs.append(1.8) 
 

  bins.append(h.GetBinLowEdge(h.GetNbinsX()+1))
  # if "VTR" in mystring:
  #   bm1 = bins[-1]
  #   bins = bins[0:-2]; bins.append(bm1)
  #   vals[-2]+=vals[-1]
  #   errs[-2] = (errs[-2]**2+errs[-1]**2)**0.5

  hnew = ROOT.TH1F("%s_fixed"%h.GetName(),"",len(bins)-1,array.array('d',bins))
  for b in range(1,hnew.GetNbinsX()+1): 
    hnew.SetBinContent(b,vals[b-1])
    hnew.SetBinError(b,errs[b-1])
  return hnew

copies = []
def copyAndStoreCanvas(name,can,fi):
  cans = can.Clone();
  cans.SetName(name)
  for obj in cans.GetListOfPrimitives():
    try : obj.SetName(obj.GetName()+name)
    except: pass
    copies.append(obj)
  fi.WriteTObject(cans)
  cans.SaveAs("%s.pdf"%name)
  cans.SaveAs("%s.png"%name)

def storeInputs(indir,outdir):
  inputs = indir.GetListOfKeys()
  for k in inputs:
    obj = k.ReadObj()
    nam = k.GetName() 
    if obj.InheritsFrom(ROOT.TDirectory.Class()): 
      newdir = outdir.mkdir(obj.GetName())
      storeInputs(obj,newdir)
    else: 
      #print " Writing ", nam, " to ", outdir
      outdir.WriteTObject(obj,nam)
# -----------------------------------------------------------------------------------------------
# 0. save the inputs
fdirInput = fout.mkdir("Inputs")
storeInputs(fin,fdirInput)
# 1. First we are going to make a fit of the min deltaPhi distribution (below MAXFIT)
fdphi = fin.Get("MetNoLep_CleanJet_mindPhi")#ROOT.TFile.Open(fdphi_name)

data  = fdphi.Get("MET_CR")
qcd_dphi = fdphi.Get("QCD_CR")
backgrounds_mdphi = getBackgrounds(fdphi)

total_bkg = fdphi.Get("BackgroundSum_CR")

# we need to clean up a bit the data, for bins > 1.5, lets blind it 
data.GetXaxis().SetTitle("min#Delta#phi(j,p_{T}^{miss})")
for b in range(1,data.GetNbinsX()+1): 
  if data.GetBinCenter(b)>MAXBLIND: 
    data.SetBinContent(b,0)
    data.SetBinError(b,0)

BINWIDTH=data.GetBinWidth(1)
data.SetLineWidth(2)
data.SetMarkerSize(0.6)
data.SetLineColor(1)
data.SetMarkerColor(1)
data.SetMarkerStyle(20)
data.GetXaxis().SetRangeUser(0,3.2)
qcd_dphi.SetLineColor(ROOT.kRed)
qcd_dphi.SetMarkerColor(ROOT.kRed)
qcd_dphi.SetMarkerStyle(4)
qcd_dphi.SetMarkerSize(0.6)

total_bkg.SetLineColor(ROOT.kBlue)
total_bkg.SetMarkerColor(ROOT.kBlue)
total_bkg.SetMarkerStyle(4)
total_bkg.SetMarkerSize(0.6)

data_forChi2   = []
data_e_forChi2   = []
data_x_forChi2 = []

@numpy.vectorize
def chi2_1b(x,d,dd):
  #print 0.5*((x-d)/dd)**2
  #if x-d > 100*dd : return 1E20
  return 0.5*(((x-d)/dd)**2)

def chi2(v): 
  d  = numpy.asarray(data_forChi2)
  dd = numpy.asarray(data_e_forChi2)
  return sum(chi2_1b(numpy.asarray(v),d,dd))
  #return sum([chi2_1b(vi,di,ddi) for vi,di,ddi in zip(v,d,dd)])

def minimised(params,args):
  #f           = args[0]
  f = args[0]
  fc = f[0]
  np_noise = params[0]
  np_wjets = params[1]
  np_zjets = params[2]

  for i,p in enumerate(params[nNuisance:]):
    f[1].SetParameter(i,p)

  # loop ovr the bins to get values
  v = [ f[1].Eval(x)+\
      (1.+BKGSYS["Noise"]*np_noise)*fc[0][i] \
  +   (1.+BKGSYS["Wjets"]*np_wjets)*fc[1][i] \
  +   (1.+BKGSYS["Zjets"]*np_zjets)*fc[2][i] \
  +   fc[3][i] \
    for i,x in enumerate(data_x_forChi2) ]
  
  gauss_chi2_np = chi2_1b(np_noise,0,1)+chi2_1b(np_wjets,0,1)+chi2_1b(np_zjets,0,1)
  
  return chi2(v) + gauss_chi2_np

def simfit(data,f,f_c,doerrs=1):
  # by definition data is fit with f_c+f, f_c are the backgrounds
  init = [ 0. for i in range(nNuisance)] #f_c.GetParameter(i) for i in range(f_c.GetNumberFreeParameters()) ] 
  init.extend([f.GetParameter(i) for i in range(f.GetNumberFreeParameters())])
 
  #bounds = [ (min([0.2*c,4*c]),max([0.25*c,4*c])) for c in init]

  del data_x_forChi2[:]
  del data_forChi2[:]
  del data_e_forChi2[:]

  for b in range(1,data.GetNbinsX()+1):
    x = data.GetBinCenter(b)
    if x < MINFIT: continue 
    if x > MAXFIT: continue 
    
    y = data.GetBinContent(b)
    e = data.GetBinError(b)
    data_forChi2.append(y)
    data_e_forChi2.append(e)
    data_x_forChi2.append(x)

  bins_content_fc = [ [bkgh.GetBinContent(bkgh.FindBin(x)) for x in data_x_forChi2] for bkgh in f_c]
  arg_structure = [[bins_content_fc,f]]
  mle = minimize(minimised,init,args=arg_structure,method="BFGS")

  if doerrs : 
    hess_inv = mle.hess_inv #numpy.linalg.inv(mle.hess)
    diage = [(hess_inv[i][i])**0.5 for i in range(len(mle.x))]

  else: diage=[0 for i in range(len(mle.x))]
  if mle.x[-1]<0 : mle.x[-1]=0.0001

  for i,p in enumerate(mle.x[nNuisance:]):
    f.SetParameter(i,p)
    f.SetParError(i,diage[i])
  
  return mle.x

f_total = makeFunction("total",SELECTFUNC,MINFIT,MAXFIT)
f_total.SetParameter(0,data.GetBinContent(1)-total_bkg.GetBinContent(1))

bestfit = simfit(data,f_total,backgrounds_mdphi,1)
background_scalefactors_fromfit = bestfit[0:3]
print "Fitted parameters", bestfit

scale_factor["Noise"] = (1.+background_scalefactors_fromfit[0]*BKGSYS["Noise"])
scale_factor["Wjets"] = (1.+background_scalefactors_fromfit[1]*BKGSYS["Wjets"])
scale_factor["Zjets"] = (1.+background_scalefactors_fromfit[2]*BKGSYS["Zjets"])

background_scalefactors_fromfit =  [scale_factor["Noise"],scale_factor["Wjets"],scale_factor["Zjets"],1.]

reformTotal(total_bkg,backgrounds_mdphi,background_scalefactors_fromfit,verb=True)

f_qcd = makeFunction("qcd",SELECTFUNC,MINFIT,ROOT.TMath.Pi())

for i in range(npar[0]): 
 f_qcd.SetParameter(i,f_total.GetParameter(i))
 print "qcd tail parameter ",i, f_qcd.GetParameter(i)

print  "fitted background scale factors are -> " 
for k in scale_factor.keys():
  print k,scale_factor[k]

norm_qcd = f_qcd.Integral(CUT,ROOT.TMath.Pi())/BINWIDTH

# R average 
if f_qcd.Integral(0,CUT) > 0:
   R_average = f_qcd.Integral(CUT,ROOT.TMath.Pi())/f_qcd.Integral(0,CUT)
else:
   R_average = f_qcd.Integral(CUT,ROOT.TMath.Pi())
print ("<R>=N(QCD>%.1f)/N(QCD<%.1f) = "%(CUT,CUT), R_average)

f_qcd.SetLineWidth(2)
f_total.SetLineWidth(2)
f_qcd.SetLineStyle(2)
f_total.SetLineStyle(2)

f_qcd.SetLineColor(ROOT.kRed)
f_total.SetLineColor(1)

# ------------------------------------------------------------------------- end of 1. 
def makeToyData(data,sys=-1): # can add a normalisation syst too!
  data_t = data.Clone(); data_t.SetName("%s_toy_%g"%(data.GetName(),R.Uniform(0,1)))
  for b in range(1,data.GetNbinsX()+1): 
    #if data_t.GetBinCenter(b)>MAXFIT: continue 
    data_t.SetBinContent(b,data_t.GetBinContent(b)+R.Gaus(0,data_t.GetBinError(b)))
  if sys>0:
    rnd = R.Gaus(0,1) 
    data_t.Scale(1+rnd*sys)
  return data_t

# 2. Time to make some toys studies, to get an uncertainty on the integral 
# nice to plot the fit correlation 
# we'll use a boostrap 
centralvals = [f_total.GetParameter(p) for p in range(npar[0])]
centralerrs = [f_total.GetParError(p)  for p in range(npar[0])]
integralhisto = ROOT.TH1F("h_integral",";Log(N(MJ>%.1f))/N_{0});Entries"%CUT,100,-3,3) #norm_qcd*0.1,norm_qcd*3.0)

rxmin = centralvals[0]-0.05*centralerrs[0]
rxmax = centralvals[0]+0.05*centralerrs[0]
rymin = centralvals[1]-30*centralerrs[1]
rymax = centralvals[1]+30*centralerrs[1]
paramtoys     = ROOT.TH2F("h_toys",";p_{0};p_{1}",30,rxmin,rxmax,30,rymin,rymax)
allhistogramspars = [ROOT.TH1F("par_%d"%p,";p_%d = %g#pm%g;"%(p,centralvals[p],centralerrs[p]),30,centralvals[p]-3.*centralerrs[p],centralvals[p]+3.*centralerrs[p]) for p in range(npar[0])]
norms=[]

rms_fqcd = [0. for i in range(total_bkg.GetNbinsX())]
cen_fqcd = [f_qcd.Eval(total_bkg.GetBinCenter(i+1)) for i in range(total_bkg.GetNbinsX())]

rms_ftot = [0. for i in range(total_bkg.GetNbinsX())]
cen_ftot = [f_qcd.Eval(total_bkg.GetBinCenter(i+1)) + total_bkg.GetBinContent(i+1) for i in range(total_bkg.GetNbinsX())]

for t in range(NTOYS): 
  if t%10==0: print "Toy %d"%t
  data_t = makeToyData(data) 
  
  # also randomize the background 
  total_bkg_t = total_bkg.Clone(); total_bkg_t.SetName("total_b_t")
  backgrounds_t = []
  for i,bkg in enumerate(backgrounds_mdphi): 
     backgrounds_t.append(makeToyData(bkg,BKGSYS[BKGSYS.keys()[i]]))

  f_total_toy = makeFunction("total_toy%d"%(t),SELECTFUNC,MINFIT,MAXFIT)
  for i in range(f_total.GetNumberFreeParameters()): f_total_toy.SetParameter(i,f_total.GetParameter(i))

  bkgscale_t = simfit(data_t,f_total_toy,backgrounds_t,0)
  #print " in toy ", t
  #print "random yield - ", total_bkg_t.Integral(), " / orig ", total_bkg_t.Integral()/total_bkg.Integral()
  #print " scale-from-fit - ", 1+BKGSYS*bkgscale_t[0]

  background_scalefactors_fromfit_t = [ 
    (1+bkgscale_t[0]*BKGSYS["Noise"]),
    (1+bkgscale_t[1]*BKGSYS["Wjets"]),
    (1+bkgscale_t[1]*BKGSYS["Zjets"]),
    1.
  ]

  reformTotal(total_bkg_t,backgrounds_t,background_scalefactors_fromfit_t)
  
  for i in range(npar[0]): f_qcd.SetParameter(i,f_total_toy.GetParameter(i))
 
  norm_qcd_t = f_qcd.Integral(CUT,ROOT.TMath.Pi())/BINWIDTH
  norms.append(ROOT.TMath.Log(norm_qcd_t/norm_qcd)**2)
  for b in range(total_bkg.GetNbinsX()): 
   rms_fqcd[b]+=(f_qcd.Eval(total_bkg.GetBinCenter(b+1))-cen_fqcd[b])**2
  
  for b in range(total_bkg.GetNbinsX()): 
   total_t_f = f_qcd.Eval(total_bkg.GetBinCenter(b+1))+total_bkg_t.GetBinContent(b+1)
   rms_ftot[b]+=(total_t_f-cen_ftot[b])**2

  for p in range(f_total.GetNumberFreeParameters()): allhistogramspars[p].Fill(f_total_toy.GetParameter(p))
  integralhisto.Fill(ROOT.TMath.Log(norm_qcd_t/norm_qcd))


rms = (sum(norms)/len(norms))**0.5
# reset 
for p in range(npar[0]): 
  f_qcd.SetParameter(p,centralvals[p])

rms_fqcd = [(ff/NTOYS)**0.5 for ff in rms_fqcd]
rms_ftot = [(ff/NTOYS)**0.5 for ff in rms_ftot]

hf_qcd = binFunction(data,f_qcd)
hf_qcd.SetName("fake_qcd_errorband")
hf_qcd.SetLineColor(ROOT.kRed)
hf_qcd.SetFillColor(ROOT.kRed-9)
hf_qcd.SetMarkerSize(0)
#hf_qcd.SetFillStyle(3001)
for i in range(hf_qcd.GetNbinsX()): 
  hf_qcd.SetBinError(i+1,rms_fqcd[i])

# and plot the stuff
if LOGY: 
    data.SetMaximum(data.GetBinContent(1)*50)
    data.SetMinimum(0.1)
else: data.SetMaximum(data.GetBinContent(1)*1.8)
c0 = ROOT.TCanvas("c","c",600,680)
c0.SetTopMargin(0.01)
pad4 = ROOT.TPad("p4","p4",0.0,0.01,1,0.18)
pad2 = ROOT.TPad("p2","p2",0.0,0.19,1,0.36)
pad1 = ROOT.TPad("p1","p1",0.0,0.362,1,0.98)
pad1.SetTicks(1,1)
pad2.SetTicks(1,1)
pad4.SetTicks(1,1)

pad1.SetBottomMargin(0.165)

pad2.SetTopMargin(0)
pad2.SetBottomMargin(0)
pad4.SetTopMargin(0)
pad4.SetBottomMargin(0)

pad1.SetLeftMargin(0.12)
pad2.SetLeftMargin(0.12)
pad4.SetLeftMargin(0.12)

pad1.SetRightMargin(0.06)
pad2.SetRightMargin(0.06)
pad4.SetRightMargin(0.06)

pad1.Draw()
pad1.cd()
#c0.SetBottomMargin(0.15)
#c0.SetLeftMargin(0.12)

data.Draw()
#f_total.SetRange(MINFIT,MAXBLIND)
#f_bkg.SetRange(MINFIT,MAXBLIND)
hist_extrap_qcd = binFunction(total_bkg,f_qcd)
hist_extrap_qcd.Add(total_bkg)
hist_extrap_qcd.SetFillColor(0)
hist_extrap_qcd.SetLineColor(ROOT.kMagenta)
hist_extrap_qcd.SetLineWidth(3)


hist_extrap_qcd.Draw("histsame")
f_qcd.Draw("lsame")
total_bkg.Draw("pel0same")
qcd_dphi.Draw("pel0same")
data.Draw("pel0same")
plainhist = ROOT.TH1F("plain","",1,0,1)
plainhist.SetLineColor(0)
leg = ROOT.TLegend(0.14,0.76,0.89,0.89)
leg.SetNColumns(2)
leg.SetBorderSize(0)
leg.SetFillColor(10)
leg.AddEntry(data,     "Data (blind above %.1f)"%MAXBLIND,"PEL")
leg.AddEntry(qcd_dphi, "Multijet MC","PEL")
leg.AddEntry(total_bkg,"Other Backgrounds","PEL")
leg.AddEntry(f_qcd,    "f_{QCD} (multijet extrap. function)","L")
leg.AddEntry(plainhist,"N(MJ)>%.1f = (%.2f#pm%.2f)#times%.1f"%(CUT,norm_qcd,rms*norm_qcd,1./BLINDFACTOR),"L")
leg.AddEntry(hist_extrap_qcd,    "Other backgrounds + f_{QCD}","L")
#if "MTR" in mystring: leg.AddEntry(f1,"fit expo*pol2","L")
#elif "VTR" in mystring: leg.AddEntry(f1,"fit pol2","L")

lat = ROOT.TLatex()
lat.SetNDC()
lat.SetTextFont(42)
lat.DrawLatex(0.12,0.92,"%s"%(mystring))
#c.SetLogy()

# finally draw a line 
lmax = ROOT.TLine(MAXFIT,data.GetMinimum(),MAXFIT,data.GetMaximum())
lmax.SetLineColor(1)
lmax.SetLineStyle(3)
lmax.Draw()
if MINFIT>0: 
 lmin = ROOT.TLine(MINFIT,data.GetMinimum(),MINFIT,data.GetMaximum())
 lmin.SetLineColor(1)
 lmin.SetLineStyle(3)
 lmin.Draw()
lat.DrawLatex(0.62,0.92,"(%.1f #times total lumi.)"%(BLINDFACTOR))
lcut = ROOT.TLine(CUT,data.GetMinimum(),CUT,data.GetMaximum())
lcut.SetLineColor(2)
lcut.SetLineStyle(3)
lcut.Draw()

osize = lat.GetTextSize()
lat.SetTextAngle(90)
lat.SetTextSize(0.02)
lat.SetNDC(False)
if LOGY:
    lat.DrawLatex(CUT-0.02,2.*data.GetMinimum(),"Control region")
    lat.DrawLatex(CUT+0.08,2.*data.GetMinimum(),"Signal region") 
else:
    lat.DrawLatex(CUT-0.02,0.8*data.GetMaximum(),"Control region")
    lat.DrawLatex(CUT+0.08,0.8*data.GetMaximum(),"Signal region")
lat.SetTextAngle(0)
lat.SetTextSize(osize)
lat.SetNDC(True)
leg.Draw()
pad1.SetLogy(LOGY)

c0.cd()
pad2.Draw()
pad2.cd()

hist_f_total = binFunction(total_bkg,f_total,MINFIT,MAXBLIND,addhist=total_bkg); hist_f_total.SetName("total_fit_function")
ratio_data = data.Clone(); ratio_data.SetName("ratio_data")
for b in range(ratio_data.GetNbinsX()):
  ratio_data.SetBinError(b+1,(ratio_data.GetBinContent(b+1))**0.5)
ratio_data = chopHistogram(ratio_data,MINFIT,MAXBLIND)
ratio_data.Divide(hist_f_total)

hist_f_total_with_errors = hist_f_total.Clone(); hist_f_total_with_errors.SetName("magenta_hist_errors")
hist_f_total_with_errors.SetFillStyle(1001)
hist_f_total_with_errors.SetFillColor(ROOT.kMagenta-9)

print "From toys, error per bin in total ... "
for i in range(hist_f_total_with_errors.GetNbinsX()): 
  print i, hist_f_total_with_errors.GetBinCenter(i+1),rms_ftot[i],rms_ftot[i]/hist_f_total_with_errors.GetBinContent(i+1) 
  hist_f_total_with_errors.SetBinError(i+1,rms_ftot[i])


hist_f_total_with_errors_toSave = hist_f_total_with_errors.Clone(); hist_f_total_with_errors_toSave.SetName("total_background_with_uncertainty_CR")


hist_f_total_with_errors.Divide(hist_f_total)
hist_f_total_with_errors.SetMarkerSize(0)
hist_f_total_with_errors.SetFillColor(ROOT.kGray)

ratio_data.GetYaxis().SetTitle("Data/f")
ratio_data.GetYaxis().SetTitleSize(0.15)
ratio_data.GetYaxis().SetTitleOffset(0.25)
ratio_data.GetYaxis().SetLabelSize(0.12)
ratio_data.GetXaxis().SetLabelSize(0.12)
ratio_data.GetXaxis().SetTitleSize(0.24)
ratio_data.GetXaxis().SetTitleOffset(0.8)
ratio_data.GetXaxis().SetLabelOffset(0.08)
ratio_data.GetYaxis().SetNdivisions(5,1,0)
ratio_data.SetMinimum(0.51)
ratio_data.SetMaximum(1.49)
ratio_data.Draw("PEL")
hist_f_total_with_errors.Draw("E2same")
ratio_data.Draw("PELsame")


# finally draw a line 
lmaxp2 = ROOT.TLine(MAXFIT,ratio_data.GetMinimum(),MAXFIT,ratio_data.GetMaximum())
lmaxp2.SetLineColor(1)
lmaxp2.SetLineStyle(3)
lmaxp2.Draw()
if MINFIT>0: 
 lminp2 = ROOT.TLine(MINFIT,ratio_data.GetMinimum(),MINFIT,ratio_data.GetMaximum())
 lminp2.SetLineColor(1)
 lminp2.SetLineStyle(3)
 lminp2.Draw()

pad2.RedrawAxis()


c0.cd()
pad4.Draw()
pad4.cd()

qcd_dphi_ratio = qcd_dphi.Clone(); qcd_dphi_ratio.SetName("qcd_mc_ratio")
hf_qcd_noerrors = hf_qcd.Clone(); hf_qcd_noerrors.SetName("hf_qcd_noerrors")
for b in range(hf_qcd_noerrors.GetNbinsX()): hf_qcd_noerrors.SetBinError(b+1,0)
hf_qcd.Divide(hf_qcd_noerrors)
qcd_dphi_ratio.Divide(hf_qcd_noerrors)
#for b in range(qcd_dphi.GetNbinsX()): print "qcd ratio ->", qcd_dphi_ratio.GetBinContent(b+1)
qcd_axis = ratio_data.Clone() 
qcd_axis.GetYaxis().SetTitle("Multijet MC/f_{QCD}")
qcd_axis.GetYaxis().SetTitleSize(0.15)
qcd_axis.GetYaxis().SetTitleOffset(0.25)
qcd_axis.GetXaxis().SetTitleSize(0.2)
qcd_axis.SetMaximum(5)
qcd_axis.SetMinimum(-2)
qcd_axis.Draw("axis")
hf_qcd.Draw("E2same")
qcd_dphi_ratio.Draw("pe0lsame")
pad4.RedrawAxis()

# finally draw a line 
lmaxp3 = ROOT.TLine(MAXFIT,qcd_axis.GetMinimum(),MAXFIT,qcd_axis.GetMaximum())
lmaxp3.SetLineColor(1)
lmaxp3.SetLineStyle(3)
lmaxp3.Draw()
if MINFIT>0: 
 lminp3 = ROOT.TLine(MINFIT,qcd_axis.GetMinimum(),MINFIT,qcd_axis.GetMaximum())
 lminp3.SetLineColor(1)
 lminp3.SetLineStyle(3)
 lminp3.Draw()

c0.cd()
#c0.SaveAs("%s_qcdDD_normfit.pdf"%fin.GetName())
copyAndStoreCanvas("%s_qcdDD_normfit"%fin.GetName(),c0,pdir)

# ---------------------------------------------------------------- end of 2
# 3. Draw the toys (hisogram of the norm and correlation matrix)
ROOT.gStyle.SetOptStat(origStat)
cP = ROOT.TCanvas("c","c",420*(npar[0]+1),420)
cP.Divide(npar[0]+1)
cP.cd(1)
integralhisto.Draw()
lat.DrawLatex(0.12,0.925,"N_{MJ} = %.2f(1+%.2f)^{#theta}"%(norm_qcd,rms))
for p in range(1,npar[0]+1): 
  cP.cd(p+1)
  allhistogramspars[p-1].Draw()
  lat.DrawLatex(0.12,0.92,"Mean=%.3f"%allhistogramspars[p-1].GetMean()+", RMS=%.3f"%allhistogramspars[p-1].GetRMS())
#cP.SaveAs("%s_qcdEstimate_toys.pdf"%fin.GetName())
copyAndStoreCanvas("%s_qcdEstimate_toys"%fin.GetName(),cP,pdir)
ROOT.gStyle.SetOptStat(0)

# --------------------------------------------------------------- end of 3.

# 4. Go and get the (background subtracted) histogram from Sam and re-normalise to the yield we just found 
# First make a plot 
data_plot = (fin.Get("MET_CR")).Clone(); data_plot.SetName("data_for_plot")
backgrounds_for_plot = getBackgrounds(fin)
background_plot = backgrounds_for_plot[0].Clone()
reformTotal(background_plot,backgrounds_for_plot,background_scalefactors_fromfit,verb=True)

cMass = ROOT.TCanvas("cmass","cmass",680,540)
cMass.cd()
data_plot = fixHistogram(data_plot)
background_plot = fixHistogram(background_plot)

# make another version of the background subtracted data
qcdFromFile = data_plot.Clone(); qcdFromFile.SetName("BackgroundSubtractedData_CR_afterfit")
qcdFromFile.Add(background_plot,-1)

# ok, now histogram version and plot
data_plot = makehist(data_plot)
background_plot = makehist(background_plot)
#data_plot.GetYaxis().SetTitle("Events/GeV")
data_plot.GetXaxis().SetTitle("M_{jj} (GeV)")
leg_mass = ROOT.TLegend(0.5,0.76,0.89,0.89)
leg_mass.SetBorderSize(0)
data_plot.SetMarkerStyle(20)
data_plot.SetMarkerSize(0.8)
data_plot.SetMarkerColor(1)
data_plot.SetLineColor(1)
data_plot.SetLineWidth(2)
data_plot.Draw("pel")
background_plot.SetFillColor(ROOT.kGray)
background_plot.SetLineColor(1)
background_plot.SetLineWidth(2)
background_plot.Draw("histsame")
data_plot.Draw("pelsame")
leg_mass.AddEntry(data_plot,"Data in QCD CR","PEL")
leg_mass.AddEntry(background_plot,"Non QCD background in QCD CR","F")
leg_mass.Draw()
cMass.SetLogy()
cMass.RedrawAxis()
latmjj = ROOT.TLatex()
latmjj.SetNDC()
latmjj.SetTextFont(42)
latmjj.DrawLatex(0.12,0.92,"%s"%(mystring))
copyAndStoreCanvas("%s_mjj_CR"%fin.GetName(),cMass,pdir)

#qcdFromFile = fin.Get("BackgroundSubtractedData_CR"); 
qcdFromFile_safety = qcdFromFile.Clone(); qcdFromFile_safety.SetName("Safety")
integral = qcdFromFile.Integral()
if integral > 0:
   qcdFromFile.Scale(norm_qcd/integral);
qcdHoriginal = fixHistogram(qcdFromFile)
qcdBinned = qcdHoriginal.Clone(); qcdBinned.SetName("rebin_QCD")
qcdH      = makehist(qcdBinned)

qcdMCFromFile  = fin.Get("QCDMC_SR")
qcdMCFromFile_safety = qcdMCFromFile.Clone(); qcdMCFromFile_safety.SetName("SafetyMC")
qcdMCFromFile.Scale(BLINDFACTOR) 
qcdMCHoriginal = fixHistogram(qcdMCFromFile)
qcdMCBinned    = qcdMCHoriginal.Clone(); qcdMCBinned.SetName("rebin_QCDMC")
qcdMCH         = makehist(qcdMCBinned)


qcdMethodAFromFile  = fin.Get("FinalQCD_SR")
qcdMethodAFromFile.Scale(BLINDFACTOR)
qcdMethodA = fixHistogram(qcdMethodAFromFile)
qcdMethodA = makehist(qcdMethodA)
qcdH.SetMinimum(ymin)
qcdH.SetMaximum(ymax)
qcdH.GetXaxis().SetTitle("m_{jj} (GeV)")
qcdH.GetYaxis().SetTitle("Events/GeV")
qcdH.SetLineColor(1)
qcdH.SetLineWidth(2)
qcdH.SetMarkerColor(1)
qcdH.SetMarkerStyle(20)
qcdH.SetMarkerSize(0.8)

qcdMethodA.SetLineColor(ROOT.kMagenta+1)
qcdMethodA.SetLineWidth(3)
fillH = qcdH.Clone();fillH.SetName("datanormerror")
for b in range(fillH.GetNbinsX()): 
  fillH.SetBinError(b+1, fillH.GetBinContent(b+1)*rms)
#  print b, fillH.GetBinContent(b+1), fillH.GetBinContent(b+1)*rms
fillH.SetFillColor(ROOT.kGray)
fillH.SetLineColor(ROOT.kGray)

qcdMCH.SetLineColor(2)
qcdMCH.SetLineWidth(2)
qcdMCH.SetMarkerColor(2)
qcdMCH.SetMarkerStyle(20)
qcdMCH.SetMarkerSize(0.8)

leg2 = ROOT.TLegend(0.14,0.74,0.89,0.89)
leg2.SetNColumns(2)
leg2.SetBorderSize(0)
leg2.AddEntry(qcdH,"Data driven MJ template in SR (method B)","PEL")
leg2.AddEntry(fillH,"#pm norm uncert.","F")
leg2.AddEntry(qcdMCH,"Multijet MC in SR","PEL")
leg2.AddEntry(qcdMethodA,"Data driven MJ template in SR (method A)","L")

lat.DrawLatex(0.12,0.92,"%s"%(mystring))
# --------------------------------------------------------------- end of 4.
cD = ROOT.TCanvas("cD","cD",600,420)
cD.cd()
cD.SetBottomMargin(0.15)
cD.SetLeftMargin(0.12)
qcdH.Draw("histPE")
fillH.Draw("sameE2")
qcdH.Draw("histPE0same")
qcdMCH.Draw("histPE0same")
qcdMethodA.Draw("histsame")
leg2.Draw()

#qcdH.SetMinimum(0.00001)
#fillH.SetMinimum(0.0001)
cD.SetLogy()
cD.RedrawAxis()
lat.DrawLatex(0.62,0.92,"(%.1f #times total lumi.)"%(BLINDFACTOR))
lat.DrawLatex(0.12,0.92,mystring)
#cD.SaveAs("%s_qcdDD.pdf"%fin.GetName())
copyAndStoreCanvas("%s_qcdDD"%fin.GetName(),cD,pdir)

print ("Data driven total (in full lumi) = ", qcdH.Integral("width")/BLINDFACTOR, "+/-", rms*norm_qcd/BLINDFACTOR)
print ("QCD MC total (in full lumi) = ", qcdMCH.Integral("width")/BLINDFACTOR)
bins = " | ".join(["%.4d-%.4d"%((qcdH.GetBinLowEdge(b)),(qcdH.GetBinLowEdge(b+1))) for b in range(1,qcdH.GetNbinsX()+1)])
print ("Bin |",bins)
vals = " | ".join(["%9.2f"%((1./BLINDFACTOR)*qcdH.GetBinContent(b)*qcdH.GetBinWidth(b)) for b in range(1,qcdH.GetNbinsX()+1)]) 
print ("N   |",vals)
errs = " | ".join(["%9.2f"%((1./BLINDFACTOR)*qcdH.GetBinError(b)*qcdH.GetBinWidth(b)) for b in range(1,qcdH.GetNbinsX()+1)]) 
print ("Err |",errs)
mcY  = " | ".join(["%9.2f"%((1./BLINDFACTOR)*qcdMCH.GetBinContent(b)*qcdMCH.GetBinWidth(b)) for b in range(1,qcdH.GetNbinsX()+1)]) 
print ("MC  |",mcY)
mcYE  = " | ".join(["%9.2f"%((1./BLINDFACTOR)*qcdMCH.GetBinError(b)*qcdMCH.GetBinWidth(b)) for b in range(1,qcdH.GetNbinsX()+1)]) 
print ("Err |",mcYE)
# --------------------------------------------------------------- end of 5.
if not options.mkworkspace: 
  print ("Plots stored in ", fout.GetName())
  fout.Close()
  sys.exit()
# 6. Make the histogram for the workspace ! 

# make an original histogram (proper hist)
qcdCountHisto = makebinned(qcdH)
if ( qcdCountHisto.Integral() != 0 ):
   qcdCountHisto.Scale((norm_qcd/BLINDFACTOR)/qcdCountHisto.Integral())
fout.WriteTObject(qcdCountHisto)

#  Write the total that has the unccertainties 
fout.WriteTObject(hist_f_total_with_errors_toSave)

# make a helpful scale-factor for each of the background groups 
AllBackgrounds["Noise"]= ["HFNoise_CR","HFTemplate_CR"]
AllBackgrounds["Wjets"]= ["WJETS_CR","EWKW_CR"]
AllBackgrounds["Zjets"]= ["ZJETS_CR","EWKZNUNU_CR","EWKZll_CR","DY_CR"]
AllBackgrounds["Rest"] = ["TOP_CR","VV_CR"]

for abackground in AllBackgrounds.items():
  for ab  in abackground[1]:
     histo_background_scale_factor = ROOT.TH1F("bkg_sf_%s"%ab,"background SF from fit for %s"%ab,1,0,1)
     if abackground[0] in  scale_factor.keys():
       histo_background_scale_factor.SetBinContent(1,scale_factor[abackground[0]])
     else: histo_background_scale_factor.SetBinContent(1,1.)
     fout.WriteTObject(histo_background_scale_factor)

lVarFit = ROOT.RooRealVar("mjj_%s"%(mystring.replace(" ","_")),"M_{jj} (GeV)",xmin,5000);

qcd_dh_nominal = ROOT.RooDataHist("QCD_DD","QCD Data-driven",ROOT.RooArgList(lVarFit),qcdCountHisto)

getattr(wspace,"import")(qcd_dh_nominal)
fout.WriteTObject(wspace)
print ("Plots and workspace stored in ", fout.GetName())

wspace.Delete()
# --------------------------------------------------------------- end of 6.

# 7. And finally the HF histogram for the workspace ! 

#if not "VTR" in mystring:
#   sys.exit()

def extend(hin):
  bins = []
  # I have to make a new set of bins because for some reason Alp's histograms have 4500 as the last edge

  for b in range(1,hin.GetNbinsX()+1):
    le = hin.GetBinLowEdge(b)
    bins.append(le)
  bins.append(5000) # this is the real end point
  bins=array.array('d',bins)
  print bins
  hnew = ROOT.TH1F(hin.GetName()+"_rbin","rebinned",len(bins)-1,bins)
  for b in range(1,hin.GetNbinsX()+1): hnew.SetBinContent(b,hin.GetBinContent(b))
  hnew.Print()
  return hnew

def convertHisto(label,histI):
  hist = histI
  mystring =  label
  fout = ROOT.TFile("inputs/%s_noiseDD.root"%(mystring.replace(" ","_")),"RECREATE")
  wspace = ROOT.RooWorkspace()
  wspace.SetName("noise_wspace")
  lVarFit = ROOT.RooRealVar("mjj_%s"%(mystring.replace(" ","_")),"M_{jj} (GeV)",xmin,5000);
  qcd_dh_nominal = ROOT.RooDataHist("QCD_noise","QCD noise template",ROOT.RooArgList(lVarFit),hist)
  getattr(wspace,"import")(qcd_dh_nominal)
  fout.WriteTObject(wspace)
  #fout.Close()
  #wspace.Delete()

hftemplate = fin.Get("HFTemplate")
hftemplate = fixHistogram(hftemplate)
convertHisto(mystring,hftemplate)


# --------------------------------------------------------------- end of 7.


