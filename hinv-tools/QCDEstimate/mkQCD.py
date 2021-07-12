# No need to edit these after unblinding has already happened 
BLINDFACTOR = 1.
REBINFACTOR = 1

####################### SETTINGS TO DEFINE HARDCODED ############################################################
# ideally we should include ~10% on the V+jets background estimate when doing the QCD, here is where we define it 
BKGSYS = 1.1

# for the uncertainties from the fit we throw toys, define here the number to use 
NTOYS=1000

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
parser.add_option("","--background_scale_factor",default=1.0,type=float,help="Scale the other backgrounds (eg from what we learn in the post fit)") 

parser.add_option("","--label",default="",type=str, help="Add a string (eg MTR 2017) to add to plots and also for naming output files")
(options,args)=parser.parse_args()
if len(args) < 1: sys.exit("Error - run with mkQCD.py inputfile.root [options]")


import ROOT
import sys 
import array 
import gc 
gc.disable()

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


npar=[0]
def makeFunction(name, WHICH,  mini,maxi, prestring=""): 
   """
   0 => the background MC fit function
   1 => the qcd component with exponential form + flat tail 
   2 => the qcd component with gaussian form
   3 => experimental (not very good)
   To make the sum, add the prestring to 1 or 2 
   """
   if WHICH==0: 
     ret = ROOT.TF1(name,"[0]*exp(-[1]*x)*(1+[2]*x+[3]*x*x)",mini,maxi);

   elif WHICH==1:
     ret = ROOT.TF1(name,"%s[0]*exp(-[1]*x)"%prestring,mini,maxi); 
     npar[0] = 2

   elif WHICH==2:
     ret = ROOT.TF1(name,"%s[0]*exp(-1*(x-[1])*(x-[1])/(2*[2]*[2]))"%prestring,mini,maxi);
     ret.SetParameter(1,-2.)
     ret.SetParameter(2,1.)
     npar[0] = 3

   elif WHICH==3:
     ret = ROOT.TF1(name,"%s[0]*(1./[1])*(-TMath::Power(x/[2],[1])+TMath::Power((1-x)/[2],[1]))"%prestring,mini,maxi);
     npar[0] = 3

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

def binFunction(h, f,xmin=-999,xmax=-999): 
  
  hnew = h.Clone(); hnew.SetName("%s_fitted_%s"%(h.GetName(),f.GetName()))
  for i in range(1,h.GetNbinsX()+1):
    bc =  h.GetBinCenter(i)
    bw = h.GetBinWidth(i)

    valued = f.Integral(h.GetBinLowEdge(i), h.GetBinLowEdge(i)+bw)
    if xmin>=-900 and bc < xmin : valued = 0 
    if xmax>=-900 and bc > xmax : valued = 0 
    if valued < 0: hnew.SetBinContent(i,0)
    else: hnew.SetBinContent(i,valued/bw)
  hnew.SetLineColor(f.GetLineColor())
  hnew.SetLineWidth(2)
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
  #copies.append(cans)
  #ROOT.SetOwnership( cans, False )
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
total_bkg = fdphi.Get("BackgroundSum_CR")

#allow option to scale
total_bkg.Scale(options.background_scale_factor)

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
f_bkg = makeFunction("bkg",0,MINFIT,MAXFIT)  # could consider something else like a polynomial added?
f_bkg.SetParameter(0,total_bkg.GetBinContent(1))
bkg_fit_res = total_bkg.Fit("bkg","RNS")

f_total = makeFunction("total",SELECTFUNC,MINFIT,MAXFIT,"%g*exp(-%g*x)*(1+%g*x+%g*x*x)+"%(f_bkg.GetParameter(0),f_bkg.GetParameter(1),f_bkg.GetParameter(2),f_bkg.GetParameter(3)))
f_total.SetParameter(4,data.GetBinContent(1)-total_bkg.GetBinContent(1))
data_fit_res = data.Fit("total","RNS")
#sys.exit()
f_qcd = makeFunction("qcd",SELECTFUNC,MINFIT,ROOT.TMath.Pi())

for i in range(npar[0]): f_qcd.SetParameter(i,f_total.GetParameter(i))
norm_qcd = f_qcd.Integral(CUT,ROOT.TMath.Pi())/BINWIDTH

# R average 
if f_qcd.Integral(0,CUT) > 0:
   R_average = f_qcd.Integral(CUT,ROOT.TMath.Pi())/f_qcd.Integral(0,CUT)
else:
   R_average = f_qcd.Integral(CUT,ROOT.TMath.Pi())
print ("<R>=N(QCD>%.1f)/N(QCD<%.1f) = "%(CUT,CUT), R_average)

f_qcd.SetLineWidth(2)
f_bkg.SetLineWidth(2)
f_total.SetLineWidth(2)
f_qcd.SetLineStyle(2)
f_bkg.SetLineStyle(2)
f_total.SetLineStyle(2)

f_qcd.SetLineColor(ROOT.kRed)
f_bkg.SetLineColor(ROOT.kBlue)
f_total.SetLineColor(1)

# ------------------------------------------------------------------------- end of 1. 
def makeToyData(data,sys=0): # can add a normalisation syst too!
  data_t = data.Clone(); data_t.SetName("%s_toy_%g"%(data.GetName(),R.Uniform(0,1)))
  for b in range(1,data.GetNbinsX()+1): 
    #if data_t.GetBinCenter(b)>MAXFIT: continue 
    data_t.SetBinContent(b,data_t.GetBinContent(b)+R.Gaus(0,data_t.GetBinError(b)))
    #data_t.SetBinError(b,data_t.GetBinContent(b)**0.5)
  # scale by a random systematic - log normal 
  if sys>0:
    sf = R.Gaus(0,1) 
    #print " data_t scaled by " , sys**sf
    data_t.Scale(sys**(sf))
  return data_t

# 2. Time to make some toys studies, to get an uncertainty on the integral 
# nice to plot the fit correlation 
Tcov   = data_fit_res.GetCovarianceMatrix()
Tcorr  = data_fit_res.GetCorrelationMatrix()
# we'll use a boostrap 
centralvals = [f_qcd.GetParameter(p) for p in range(npar[0])]
centralerrs = [f_total.GetParError(p) for p in range(npar[0])]
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
cen_ftot = [f_total.Eval(total_bkg.GetBinCenter(i+1)) for i in range(total_bkg.GetNbinsX())]

rms_fbkg = [0. for i in range(total_bkg.GetNbinsX())]
cen_fbkg = [f_bkg.Eval(total_bkg.GetBinCenter(i+1)) for i in range(total_bkg.GetNbinsX())]

for t in range(NTOYS): 
  data_t = makeToyData(data) 
  
  # also randomize the background 
  total_bkg_t = makeToyData(total_bkg,BKGSYS)
  f_bkg_t = makeFunction("bkg_func%d"%(t),0,MINFIT,MAXFIT)
  total_bkg_t.Fit("bkg_func%d"%(t),"RQ")
  
  f_total_toy = makeFunction("total_toy%d"%(t),SELECTFUNC,MINFIT,MAXFIT,"%g*exp(-%g*x)*(1+%g*x+%g*x*x)+"%(f_bkg_t.GetParameter(0),f_bkg_t.GetParameter(1),f_bkg_t.GetParameter(2),f_bkg_t.GetParameter(3)))
  f_total_toy.SetParameter(0,data_t.GetBinContent(1)-total_bkg_t.GetBinContent(1))
  
  data_t.Fit("total_toy%d"%t,"RQ")
  
  for i in range(npar[0]): f_qcd.SetParameter(i,f_total_toy.GetParameter(i))
  norm_qcd_t = f_qcd.Integral(CUT,ROOT.TMath.Pi())/BINWIDTH
  norms.append(ROOT.TMath.Log(norm_qcd_t/norm_qcd)**2)
  for b in range(total_bkg.GetNbinsX()): rms_fqcd[b]+=(f_qcd.Eval(total_bkg.GetBinCenter(b+1))-cen_fqcd[b])**2
  for b in range(total_bkg.GetNbinsX()): rms_fbkg[b]+=(f_bkg_t.Eval(total_bkg.GetBinCenter(b+1))-cen_fbkg[b])**2
  for b in range(total_bkg.GetNbinsX()): rms_ftot[b]+=(f_total_toy.Eval(total_bkg.GetBinCenter(b+1))-cen_ftot[b])**2
  for p in range(npar[0]): allhistogramspars[p].Fill(f_total_toy.GetParameter(p))
  integralhisto.Fill(ROOT.TMath.Log(norm_qcd_t/norm_qcd))


rms = (sum(norms)/len(norms))**0.5
# reset 
for p in range(npar[0]): 
  f_qcd.SetParameter(p,centralvals[p])

rms_fqcd = [(ff/NTOYS)**0.5 for ff in rms_fqcd]
rms_ftot = [(ff/NTOYS)**0.5 for ff in rms_ftot]
rms_fbkg = [(ff/NTOYS)**0.5 for ff in rms_fbkg]

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
pad4 = ROOT.TPad("p4","p4",0.0,0.01,1,0.12)
pad3 = ROOT.TPad("p3","p3",0.0,0.13,1,0.24)
pad2 = ROOT.TPad("p2","p2",0.0,0.25,1,0.36)
pad1 = ROOT.TPad("p1","p1",0.0,0.37,1,0.98)
pad1.SetTicks(1,1)
pad2.SetTicks(1,1)
pad3.SetTicks(1,1)
pad4.SetTicks(1,1)

pad1.SetBottomMargin(0.165)

pad2.SetTopMargin(0)
pad2.SetBottomMargin(0)
pad3.SetTopMargin(0)
pad3.SetBottomMargin(0)
pad4.SetTopMargin(0)
pad4.SetBottomMargin(0)

pad1.SetLeftMargin(0.12)
pad2.SetLeftMargin(0.12)
pad3.SetLeftMargin(0.12)
pad4.SetLeftMargin(0.12)

pad1.SetRightMargin(0.06)
pad2.SetRightMargin(0.06)
pad3.SetRightMargin(0.06)
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
f_total.Draw("lsame")
f_bkg.Draw("lsame")
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
leg.AddEntry(f_bkg,  "f_{B}","L")
leg.AddEntry(f_total,  "f (fit function)","L")
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
lat.SetTextAngle(90);
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

hist_f_total = binFunction(total_bkg,f_total,MINFIT,MAXBLIND); hist_f_total.SetName("total_fit_function")
ratio_data = data.Clone(); ratio_data.SetName("ratio_data")
ratio_data = chopHistogram(ratio_data,MINFIT,MAXBLIND)
ratio_data.Divide(hist_f_total)

hist_f_total_with_errors = hist_f_total.Clone(); hist_f_total_with_errors.SetName("magenta_hist_errors")
hist_f_total_with_errors.SetFillStyle(1001)
hist_f_total_with_errors.SetFillColor(ROOT.kMagenta-9)
for i in range(hist_f_total_with_errors.GetNbinsX()): 
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
ratio_data.GetYaxis().SetNdivisions(0,1,0)
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
pad3.Draw()
pad3.cd()

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
pad3.RedrawAxis()

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
pad4.Draw()
pad4.cd()

bkg_ratio = total_bkg.Clone(); bkg_ratio.SetName("background_MC_ratio")
bkg_fit_h = binFunction(total_bkg,f_bkg,MINFIT,MAXBLIND); bkg_fit_h.SetName("bkg_fit_h")
bkg_ratio = chopHistogram(bkg_ratio,MINFIT,MAXBLIND)
bkg_ratio.Divide(bkg_fit_h)
bkg_fit_h_with_errors = bkg_fit_h.Clone(); bkg_fit_h_with_errors.SetName("magenta_hist_errors")
bkg_fit_h_with_errors.SetFillStyle(1001)
bkg_fit_h_with_errors.SetFillColor(ROOT.kBlue-9)
for i in range(bkg_fit_h_with_errors.GetNbinsX()): 
  bkg_fit_h_with_errors.SetBinError(i+1,rms_fbkg[i])
bkg_fit_h_with_errors.Divide(bkg_fit_h)
bkg_fit_h_with_errors.SetMarkerSize(0)

bkg_axis = ratio_data.Clone() 
bkg_axis.GetYaxis().SetTitle("Oth. bkg/f_{B}")
bkg_axis.GetYaxis().SetTitleSize(0.15)
bkg_axis.GetYaxis().SetTitleOffset(0.25)
bkg_axis.GetXaxis().SetTitleSize(0.2)
bkg_axis.SetMaximum(1.24)
bkg_axis.SetMinimum(0.76)
bkg_axis.Draw("axis")
bkg_fit_h_with_errors.Draw("E2same")
bkg_ratio.Draw("pe0lsame")
pad4.RedrawAxis()

# finally draw a line 
lmaxp4 = ROOT.TLine(MAXFIT,bkg_axis.GetMinimum(),MAXFIT,bkg_axis.GetMaximum())
lmaxp4.SetLineColor(1)
lmaxp4.SetLineStyle(3)
lmaxp4.Draw()
if MINFIT>0: 
 lminp4 = ROOT.TLine(MINFIT,bkg_axis.GetMinimum(),MINFIT,bkg_axis.GetMaximum())
 lminp4.SetLineColor(1)
 lminp4.SetLineStyle(3)
 lminp4.Draw()
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
background_plot = (fin.Get("VV_CR")).Clone(); background_plot.SetName("non_QCD_backgrounds")
for bkg_plot in ["TOP_CR","DY_CR","EWKZll_CR","EWKZNUNU_CR","ZJETS_CR","EWKW_CR","WJETS_CR","HFTemplate_CR"]:
 background_plot.Add((fin.Get(bkg_plot)).Clone())
background_plot.Scale(options.background_scale_factor)
cMass = ROOT.TCanvas("cmass","cmass",680,540)
cMass.cd()
data_plot = fixHistogram(data_plot)
background_plot = fixHistogram(background_plot)

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

qcdFromFile = fin.Get("BackgroundSubtractedData_CR"); 
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

# use the exact same cuts to compare with for Method A
# UNCOMMENT NEXT 4 LINES TO USE TIGHTER CUT FOR TRANSFER FACTOR
#qcdMethodAFromFileR  = qcdMCFromFile_safety.Clone(); qcdMethodAFromFileR.SetName("FinalQCD_SRMC")
#qcdMethodAFromFileR.Divide(fin.Get("QCDMC_CR"))
#qcdMethodAFromFile = qcdFromFile_safety.Clone(); qcdMethodAFromFile.SetName("hellno")
#qcdMethodAFromFile.Multiply(qcdMethodAFromFileR)

# use the relaxed cut version to compare with for Method A
# COMMENT NEXT  LINE TO USE TIGHTER CUT FOR TRANSFER FACTOR

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
# 5. Closure in QCD MC A)
# I want to take the Region A and use it to predict region B!
# and start from there being the "data"

data_fake  = fdphi.Get("DATA_A")
#data_fake  = fdphi.Get("QCD_A")

data_fake.GetXaxis().SetTitle("min#Delta#phi(j,p_{T}^{miss})")
data_fake.SetLineWidth(2)
data_fake.SetMarkerSize(0.6)
data_fake.GetXaxis().SetRangeUser(0,3.2)
data_fake.SetLineColor(ROOT.kGreen+2)
data_fake.SetMarkerColor(ROOT.kGreen+2)
data_fake.SetMarkerStyle(20)
data_fake.SetMarkerSize(0.6)

background_fake = fdphi.Get("BackgroundSum_A")
background_fake.SetLineColor(ROOT.kBlue)
background_fake.SetMarkerColor(ROOT.kBlue)
background_fake.SetMarkerStyle(4)
background_fake.SetMarkerSize(0.6)
#data_fake.Add(background_fake)

qcd_dphi_fake = fdphi.Get("QCD_A"); qcd_dphi_fake.SetName("QCD_REGION_A")
qcd_dphi_fake.SetLineColor(ROOT.kRed)
qcd_dphi_fake.SetMarkerColor(ROOT.kRed)
qcd_dphi_fake.SetMarkerStyle(4)
qcd_dphi_fake.SetMarkerSize(0.6)

# make the same functions but for the fake data now (in Region A)

f_bkg_fake = makeFunction("bkg_fake",0,MINFIT,MAXFIT)  # could consider something else like a polynomial added?
f_bkg_fake.SetParameter(0,background_fake.GetBinContent(1))
bkg_fit_fake_res = background_fake.Fit("bkg_fake","RNS")
f_total_fake = makeFunction("total_fake",SELECTFUNC,MINFIT,MAXFIT,"%g*exp(-%g*x)*(1+%g*x+%g*x*x)+"%(f_bkg_fake.GetParameter(0),f_bkg_fake.GetParameter(1),f_bkg_fake.GetParameter(2),f_bkg_fake.GetParameter(3)))
f_total_fake.SetParameter(0,data_fake.GetBinContent(1)-background_fake.GetBinContent(1))
data_fit_res = data_fake.Fit("total_fake","RNS")
f_qcd_fake = makeFunction("qcd_fake",SELECTFUNC,MINFIT,ROOT.TMath.Pi())
for i in range(npar[0]): f_qcd_fake.SetParameter(i,f_total_fake.GetParameter(i))
norm_qcd_fake = f_qcd_fake.Integral(CUT,ROOT.TMath.Pi())/BINWIDTH

f_qcd_fake.SetLineWidth(2)
f_bkg_fake.SetLineWidth(2)
f_total_fake.SetLineWidth(2)
f_qcd_fake.SetLineStyle(2)
f_bkg_fake.SetLineStyle(2)
f_total_fake.SetLineStyle(2)

f_qcd_fake.SetLineColor(ROOT.kRed)
f_bkg_fake.SetLineColor(ROOT.kBlue)
f_total_fake.SetLineColor(1)

print (" Total closure (fit) -> ", norm_qcd_fake)
norms_fake = []
centralvals = [f_qcd_fake.GetParameter(p) for p in range(npar[0])]
rms_fqcd2 = [0. for i in range(background_fake.GetNbinsX())]
cen_fqcd2 = [f_qcd_fake.Eval(background_fake.GetBinCenter(i+1)) for i in range(background_fake.GetNbinsX())]

rms_ftot2 = [0. for i in range(background_fake.GetNbinsX())]
cen_ftot2 = [f_total_fake.Eval(background_fake.GetBinCenter(i+1)) for i in range(background_fake.GetNbinsX())]

rms_fbkg2 = [0. for i in range(background_fake.GetNbinsX())]
cen_fbkg2 = [f_bkg_fake.Eval(background_fake.GetBinCenter(i+1)) for i in range(background_fake.GetNbinsX())]

# and make some toys too !
for t in range(NTOYS): 
  data_t = makeToyData(data_fake) 
  
  # also randomize the background 
  background_fake_t = makeToyData(background_fake)
  f_bkg_t = makeFunction("bkg_func_faketime%d"%(t),0,MINFIT,MAXFIT)
  background_fake_t.Fit("bkg_func_faketime%d"%(t),"RQ")
  f_total_toy = makeFunction("total_toy_faketime%d"%(t),SELECTFUNC,MINFIT,MAXFIT,"%g*exp(-%g*x)*(1+%g*x+%g*x*x)+"%(f_bkg_t.GetParameter(0),f_bkg_t.GetParameter(1),f_bkg_t.GetParameter(2),f_bkg_t.GetParameter(3)))

  f_total_toy.SetParameter(0,data_t.GetBinContent(1)-background_fake_t.GetBinContent(1))
  data_t.Fit("total_toy_faketime%d"%t,"RQ")
  
  for i in range(npar[0]): f_qcd_fake.SetParameter(i,f_total_toy.GetParameter(i))
  norm_qcd_t_fake = f_qcd_fake.Integral(CUT,ROOT.TMath.Pi())/BINWIDTH
  if norm_qcd_t_fake < 0: continue
  norms_fake.append(ROOT.TMath.Log(norm_qcd_t_fake/norm_qcd_fake)**2)
  for b in range(background_fake_t.GetNbinsX()): 
    #if abs(cen_fqcd2[b] - f_qcd.Eval(background_fake_t.GetBinCenter(b+1))) > 500 : continue # print " vals ", b+1, cen_fqcd2[b], f_qcd.Eval(background_fake.GetBinCenter(b+1))
    rms_fqcd2[b]+=(f_qcd_fake.Eval(background_fake_t.GetBinCenter(b+1))-cen_fqcd2[b])**2
  for b in range(background_fake_t.GetNbinsX()): 
    #if abs(cen_ftot2[b] - f_qcd.Eval(background_fake_t.GetBinCenter(b+1))) > 500 : continue # print " vals ", b+1, cen_fqcd2[b], f_qcd.Eval(background_fake.GetBinCenter(b+1))
    rms_ftot2[b]+=(f_total_toy.Eval(background_fake.GetBinCenter(b+1))-cen_ftot2[b])**2
  for b in range(background_fake_t.GetNbinsX()): 
    rms_fbkg2[b]+=(f_bkg_t.Eval(background_fake.GetBinCenter(b+1))-cen_fbkg2[b])**2

if ( len(norms_fake) > 0 ):
   rms_fake = (sum(norms_fake)/len(norms_fake))**0.5
else:
   rms_fake = 0

# reset 
for p in range(npar[0]): 
  f_qcd_fake.SetParameter(p,centralvals[p])

rms_fqcd2 = [(ff/len(rms_fqcd2))**0.5 for ff in rms_fqcd2]
rms_ftot2 = [(ff/len(rms_ftot2))**0.5 for ff in rms_ftot2]
rms_fbkg2 = [(ff/len(rms_fbkg2))**0.5 for ff in rms_fbkg2]
hf_qcd2 = binFunction(background_fake,f_qcd_fake) 
hf_qcd2.SetName("fake_qcd_errorband_fakefits")
hf_qcd2.SetLineColor(2)
hf_qcd2.SetFillColor(ROOT.kRed-9)
hf_qcd2.SetMarkerSize(0)
#hf_qcd2.SetFillStyle(3001)
for i in range(hf_qcd2.GetNbinsX()): 
  hf_qcd2.SetBinError(i+1,rms_fqcd2[i])
  #print "Fake data ->", i+1, rms_fqcd2[i]


# and plot the stuff
if LOGY: 
    data_fake.SetMaximum(data_fake.GetBinContent(1)*50)
    data_fake.SetMinimum(0.1)
else: data_fake.SetMaximum(data_fake.GetBinContent(1)*1.8)

c4 = ROOT.TCanvas("c","c",600,680)
c4.SetTopMargin(0.01)
padf4 = ROOT.TPad("pf4","p4",0.0,0.01,1,0.12)
padf3 = ROOT.TPad("pf3","p3",0.0,0.13,1,0.24)
padf2 = ROOT.TPad("pf2","p2",0.0,0.25,1,0.36)
padf1 = ROOT.TPad("pf1","p1",0.0,0.37,1,0.98)
padf1.SetTicks(1,1)
padf2.SetTicks(1,1)
padf3.SetTicks(1,1)
padf4.SetTicks(1,1)

padf1.SetBottomMargin(0.165)

padf2.SetTopMargin(0)
padf2.SetBottomMargin(0)
padf3.SetTopMargin(0)
padf3.SetBottomMargin(0)
padf4.SetTopMargin(0)
padf4.SetBottomMargin(0)


padf1.SetLeftMargin(0.12)
padf2.SetLeftMargin(0.12)
padf3.SetLeftMargin(0.12)
padf4.SetLeftMargin(0.12)

padf1.SetRightMargin(0.06)
padf2.SetRightMargin(0.06)
padf3.SetRightMargin(0.06)
padf4.SetRightMargin(0.06)

padf2.SetRightMargin(0.06)
padf3.SetRightMargin(0.06)
padf4.SetRightMargin(0.06)

padf1.Draw()
padf1.cd()

data_fake.Draw()
f_total_fake.Draw("lsame")
#hf_qcd2.Draw("E3same")
f_bkg_fake.Draw("lsame")
f_qcd_fake.Draw("lsame")
background_fake.Draw("pelsame")
qcd_dphi_fake.Draw("pelsame")
data_fake.Draw("pelsame")
leg = ROOT.TLegend(0.14,0.76,0.89,0.89)
leg.SetNColumns(2)
leg.SetBorderSize(0)
leg.AddEntry(data_fake,"Data (Region A+B)","PEL")
leg.AddEntry(qcd_dphi_fake,"Multijet MC","PEL")
leg.AddEntry(background_fake,"Other Backgrounds","PEL")
leg.AddEntry(f_bkg_fake,"f_{B} (closure)","L")
leg.AddEntry(f_total_fake,"Fit function (f, closure)","L")
leg.AddEntry(f_qcd_fake,"Multijet extrapolation (f_{QCD}, closure)","L")
leg.AddEntry(plainhist,"N(MJ)>%.1f = (%.2f#pm%.2f)#times%.1f"%(CUT,norm_qcd_fake,rms_fake*norm_qcd_fake,1./BLINDFACTOR),"L")

# finally draw a line 
lmax = ROOT.TLine(MAXFIT,data_fake.GetMinimum(),MAXFIT,data_fake.GetMaximum())
lmax.SetLineColor(1)
lmax.SetLineStyle(3)
lmax.Draw()
if MINFIT>0: 
 lmin = ROOT.TLine(MINFIT,data_fake.GetMinimum(),MINFIT,data_fake.GetMaximum())
 lmin.SetLineColor(1)
 lmin.SetLineStyle(3)
 lmin.Draw()
lat.DrawLatex(0.62,0.92,"(%.1f #times total lumi.)"%(BLINDFACTOR))
lcut = ROOT.TLine(CUT,data_fake.GetMinimum(),CUT,data_fake.GetMaximum())
lcut.SetLineColor(2)
lcut.SetLineStyle(3)
lcut.Draw()

osize = lat.GetTextSize()
lat.SetTextAngle(90);
lat.SetTextSize(0.02)
lat.SetNDC(False)
if LOGY:
    lat.DrawLatex(CUT-0.02,2.*data_fake.GetMinimum(),"Control region")
    lat.DrawLatex(CUT+0.08,2.*data_fake.GetMinimum(),"Signal region") 
else:
    lat.DrawLatex(CUT-0.02,0.8*data_fake.GetMaximum(),"Control region")
    lat.DrawLatex(CUT+0.08,0.8*data_fake.GetMaximum(),"Signal region")
lat.SetTextAngle(0)
lat.SetTextSize(osize)
lat.SetNDC(True)
leg.Draw()
lat.DrawLatex(0.12,0.92,"%s Region A+B"%(mystring))
padf1.SetLogy(LOGY)

c4.cd()
padf2.Draw()
padf2.cd()

hist_f_total_fake = binFunction(background_fake,f_total_fake,MINFIT,MAXBLIND); hist_f_total_fake.SetName("total_fit_function_fake")

ratio_fake_data = data_fake.Clone(); ratio_fake_data.SetName("ratio_fake_data")
ratio_fake_data = chopHistogram(ratio_fake_data,MINFIT,MAXBLIND)
ratio_fake_data.Divide(hist_f_total_fake)

hist_f_total_fake_with_errors = hist_f_total_fake.Clone(); hist_f_total_fake_with_errors.SetName("fake_green_hist_errors")
hist_f_total_fake_with_errors.SetFillStyle(1001)
hist_f_total_fake_with_errors.SetFillColor(ROOT.kGreen-9)
for i in range(hist_f_total_fake_with_errors.GetNbinsX()): 
  hist_f_total_fake_with_errors.SetBinError(i+1,rms_ftot2[i])
hist_f_total_fake_with_errors.Divide(hist_f_total_fake)
hist_f_total_fake_with_errors.SetMarkerSize(0)

ratio_fake_data.GetYaxis().SetTitle("Fake data/f")
ratio_fake_data.GetYaxis().SetTitleSize(0.15)
ratio_fake_data.GetYaxis().SetTitleOffset(0.25)
ratio_fake_data.GetYaxis().SetLabelSize(0.12)
ratio_fake_data.GetXaxis().SetLabelSize(0.12)
ratio_fake_data.GetXaxis().SetTitleSize(0.24)
ratio_fake_data.GetXaxis().SetTitleOffset(0.8)
ratio_fake_data.GetXaxis().SetLabelOffset(0.08)
ratio_fake_data.GetYaxis().SetNdivisions(0,1,0)
ratio_fake_data.SetMinimum(0.51)
ratio_fake_data.SetMaximum(1.49)
ratio_fake_data.Draw("PEL")
#hist_extrap_qcd_with_errors.Draw("histsame")
hist_f_total_fake_with_errors.Draw("E2same")
ratio_fake_data.Draw("PELsame")
padf2.RedrawAxis()
# finally draw a line 
lmaxpf2 = ROOT.TLine(MAXFIT,ratio_fake_data.GetMinimum(),MAXFIT,ratio_fake_data.GetMaximum())
lmaxpf2.SetLineColor(1)
lmaxpf2.SetLineStyle(3)
lmaxpf2.Draw()
if MINFIT>0: 
 lminpf2 = ROOT.TLine(MINFIT,ratio_fake_data.GetMinimum(),MINFIT,ratio_fake_data.GetMaximum())
 lminpf2.SetLineColor(1)
 lminpf2.SetLineStyle(3)
 lminpf2.Draw()


c4.cd()
padf3.Draw()
padf3.cd()

qcd_dphi_fake_ratio = qcd_dphi_fake.Clone(); qcd_dphi_fake_ratio.SetName("qcd_mc_ratio_fakefit")
hf_qcd2_noerrors = hf_qcd2.Clone(); hf_qcd2_noerrors.SetName("hf_qcd2_noerrors")
for b in range(hf_qcd2_noerrors.GetNbinsX()): hf_qcd2_noerrors.SetBinError(b+1,0)
hf_qcd2.Divide(hf_qcd2_noerrors)
qcd_dphi_fake_ratio.Divide(hf_qcd2_noerrors)
qcd_axis2 = ratio_fake_data.Clone() 
qcd_axis2.GetYaxis().SetTitle("Multijet MC/f_{QCD}")
qcd_axis2.GetYaxis().SetTitleSize(0.15)
qcd_axis2.GetYaxis().SetTitleOffset(0.25)
qcd_axis2.GetXaxis().SetTitleSize(0.2)
qcd_axis2.SetMaximum(5)
qcd_axis2.SetMinimum(-3)
qcd_axis2.Draw("axis")
hf_qcd2.Draw("E2same")
qcd_dphi_fake_ratio.Draw("pe0lsame")
padf3.RedrawAxis()

# finally draw a line 
lmaxpf3 = ROOT.TLine(MAXFIT,qcd_axis2.GetMinimum(),MAXFIT,qcd_axis2.GetMaximum())
lmaxpf3.SetLineColor(1)
lmaxpf3.SetLineStyle(3)
lmaxpf3.Draw()
if MINFIT>0: 
 lminpf3 = ROOT.TLine(MINFIT,qcd_axis2.GetMinimum(),MINFIT,qcd_axis2.GetMaximum())
 lminpf3.SetLineColor(1)
 lminpf3.SetLineStyle(3)
 lminpf3.Draw()


c4.cd()
padf4.Draw()
padf4.cd()

bkg_ratio = background_fake.Clone(); bkg_ratio.SetName("background_MC_ratio2")
bkg_fit_h = binFunction(background_fake,f_bkg_fake,MINFIT,MAXBLIND); bkg_fit_h.SetName("bkg_fit_h2")
bkg_ratio = chopHistogram(bkg_ratio,MINFIT,MAXBLIND)
bkg_ratio.Divide(bkg_fit_h)
bkg_fit_h_with_errors = bkg_fit_h.Clone(); bkg_fit_h_with_errors.SetName("magenta_hist_errors_fake")
bkg_fit_h_with_errors.SetFillStyle(1001)
bkg_fit_h_with_errors.SetFillColor(ROOT.kBlue-9)
for i in range(bkg_fit_h_with_errors.GetNbinsX()): 
  bkg_fit_h_with_errors.SetBinError(i+1,rms_fbkg2[i])
bkg_fit_h_with_errors.Divide(bkg_fit_h)
bkg_fit_h_with_errors.SetMarkerSize(0)

bkg_axis = ratio_data.Clone() 
bkg_axis.GetYaxis().SetTitle("Oth. bkg/f_{B}")
bkg_axis.GetYaxis().SetTitleSize(0.15)
bkg_axis.GetYaxis().SetTitleOffset(0.25)
bkg_axis.GetXaxis().SetTitleSize(0.2)
bkg_axis.SetMaximum(1.24)
bkg_axis.SetMinimum(0.76)
bkg_axis.Draw("axis")
bkg_fit_h_with_errors.Draw("E2same")
bkg_ratio.Draw("pe0lsame")


padf4.RedrawAxis()
# finally draw a line 
lmaxpf4 = ROOT.TLine(MAXFIT,bkg_axis.GetMinimum(),MAXFIT,bkg_axis.GetMaximum())
lmaxpf4.SetLineColor(1)
lmaxpf4.SetLineStyle(3)
lmaxpf4.Draw()
if MINFIT>0: 
 lminpf4 = ROOT.TLine(MINFIT,bkg_axis.GetMinimum(),MINFIT,bkg_axis.GetMaximum())
 lminpf4.SetLineColor(1)
 lminpf4.SetLineStyle(3)
 lminpf4.Draw()


#c4.SaveAs("%s_qcdDD_fakefit.pdf"%fin.GetName())
copyAndStoreCanvas("%s_qcdDD_fakefit"%fin.GetName(),c4,pdir)


qcdFromFakeFile = fin.Get("QCDMC_CR")
integralfake = qcdFromFakeFile.Integral()
if integralfake > 0:
   qcdFromFakeFile.Scale(norm_qcd_fake/integralfake);
qcdClosure = fixHistogram(qcdFromFakeFile)
qcdClosure = makehist(qcdClosure)

fillfakeH = qcdClosure.Clone();fillfakeH.SetName("fakedatanormerror")
for b in range(fillfakeH.GetNbinsX()): 
  fillfakeH.SetBinError(b+1, fillfakeH.GetBinContent(b+1)*rms_fake)
#  print b, fillfakeH.GetBinContent(b+1), fillfakeH.GetBinContent(b+1)*rms
fillfakeH.SetFillColor(ROOT.kGreen)
fillfakeH.SetFillStyle(3001)

# also make alternative templates for shape variations 
transfer_factor_qcd_mc   = fin.Get("BackgroundSubtractedData_B")
transfer_factor_qcd_mc_d = fin.Get("BackgroundSubtractedData_A")
if ( transfer_factor_qcd_mc.Integral() > 0):
   transfer_factor_qcd_mc.Scale(1./transfer_factor_qcd_mc.Integral())
if ( transfer_factor_qcd_mc_d.Integral() > 0):
   transfer_factor_qcd_mc_d.Scale(1./transfer_factor_qcd_mc_d.Integral())
transfer_factor_qcd_mc.Divide(transfer_factor_qcd_mc_d)

transfer_factor_qcd_mc.Fit("pol1")
qcdH_shape_up = qcdH.Clone(); qcdH_shape_up.SetName("qcd_DD_shapeUncertaintyUp")
qcdH_shape_dn = qcdH.Clone(); qcdH_shape_dn.SetName("qcd_DD_shapeUncertaintyDown")
for b in range(1,qcdH.GetNbinsX()+1): 
  dijet_M = qcdH.GetBinCenter(b)
  content_b = qcdH.GetBinContent(b)
  if ( transfer_factor_qcd_mc.Integral() > 0):
     ratio_b = transfer_factor_qcd_mc.GetFunction("pol1").Eval(dijet_M)
     if ratio_b < 1.e-8 : ratio_b = 1.e-8
     qcdH_shape_up.SetBinContent(b,content_b*ratio_b)
     qcdH_shape_dn.SetBinContent(b,content_b*(1./ratio_b))
     qcdH_shape_up.SetBinError(b,0)
     qcdH_shape_dn.SetBinError(b,0)
  else:
     qcdH_shape_up.SetBinContent(b,0)
     qcdH_shape_dn.SetBinContent(b,0)
     qcdH_shape_up.SetBinError(b,0)
     qcdH_shape_dn.SetBinError(b,0)
     
if ( qcdH_shape_up.Integral() > 0):
   qcdH_shape_up.Scale(qcdH.Integral("width")/qcdH_shape_up.Integral("width"))
if ( qcdH_shape_dn.Integral() > 0):
   qcdH_shape_dn.Scale(qcdH.Integral("width")/qcdH_shape_dn.Integral("width"))

qcdH_shape_up.SetLineColor(4); qcdH_shape_up.SetLineStyle(2); qcdH_shape_up.SetFillStyle(0)
qcdH_shape_dn.SetLineColor(4); qcdH_shape_dn.SetLineStyle(2); qcdH_shape_dn.SetFillStyle(0)


cD = ROOT.TCanvas("cD","cD",600,420)
cD.cd()
cD.SetBottomMargin(0.15)
cD.SetLeftMargin(0.12)
qcdH.Draw("histPE")
fillH.Draw("sameE2")
qcdH.Draw("histPE0same")
qcdMCH.Draw("histPE0same")
qcdMethodA.Draw("histsame")
#fillH.SetLineColor(ROOT.kMagenta)
#leg2.AddEntry(qcdClosure,"Closure test in QCD MC","PEL")
#leg2.AddEntry(fillfakeH,"#pm norm uncert. (from fake data fit)","F")


#cD.cd()
qcdH_shape_up.Draw("histsame")
qcdH_shape_dn.Draw("histsame")
leg2.AddEntry(qcdH_shape_up,"up/down shape uncertainty","L")
leg2.Draw()

#qcdH.SetMinimum(0.00001)
#fillH.SetMinimum(0.0001)
cD.SetLogy()
cD.RedrawAxis()
lat.DrawLatex(0.62,0.92,"(%.1f #times total lumi.)"%(BLINDFACTOR))
lat.DrawLatex(0.12,0.92,mystring)
#cD.SaveAs("%s_qcdDD.pdf"%fin.GetName())
copyAndStoreCanvas("%s_qcdDD"%fin.GetName(),cD,pdir)

cT = ROOT.TCanvas("cT","cT",600,420)
cT.cd()
ROOT.gStyle.SetOptFit(1111)
ROOT.gStyle.SetOptStat(1)
transfer_factor_qcd_mc.GetYaxis().SetTitle("m_{jj} shape in B / m_{jj} shape in A")
transfer_factor_qcd_mc.Draw("pel")
if ( transfer_factor_qcd_mc.Integral() > 0):
   transfer_factor_qcd_mc.GetFunction("pol1").SetLineColor(1);
   transfer_factor_qcd_mc.GetFunction("pol1").Draw("same");
copyAndStoreCanvas("%s_qcdDD_fitTransferForShapeSys"%fin.GetName(),cT,pdir)
ROOT.gStyle.SetOptFit(0)
ROOT.gStyle.SetOptStat(0)

cF = cD.Clone(); cF.SetName("cF")
qcdH.Draw("axis")
qcdClosure.SetLineColor(ROOT.kGreen+2)
qcdClosure.SetLineWidth(2)
qcdClosure.SetMarkerColor(ROOT.kGreen+2)
qcdClosure.SetMarkerStyle(20)
qcdClosure.SetMarkerSize(0.8)
fillfakeH.Draw("sameE2")
qcdClosure.Draw("histPEsame")

# and finally get the data-background in region B 
dataB = fixHistogram(fin.Get("BackgroundSubtractedData_B"))
#dataB = fixHistogram(fin.Get("QCD_B"))
dataB = makehist(dataB)
dataB.SetMarkerColor(ROOT.kOrange-6)
dataB.SetLineColor(ROOT.kOrange-6)
dataB.SetMarkerStyle(qcdH.GetMarkerStyle())
dataB.SetMarkerSize(qcdH.GetMarkerSize())
dataB.SetLineWidth(qcdH.GetLineWidth())
dataB.Draw("pel0same")

legAB = ROOT.TLegend(0.14,0.74,0.89,0.89)
legAB.SetNColumns(2)
legAB.SetBorderSize(0)
legAB.AddEntry(qcdClosure,"Closure template (pred. from Region A)","PEL")
legAB.AddEntry(fillfakeH,"#pm norm uncert.","F")
legAB.AddEntry(dataB,"Data-bkg in Region B","L")

lat.DrawLatex(0.62,0.92,"(%.1f #times total lumi.)"%(BLINDFACTOR))
lat.DrawLatex(0.12,0.92,mystring+" Region B")
legAB.Draw()

#cD.SaveAs("%s_qcdDD_closureAB.pdf"%fin.GetName())
copyAndStoreCanvas("%s_qcdDD_closureAB"%fin.GetName(),cF,pdir)


cR = ROOT.TCanvas("cR","cR",600,320)
qcdClosure_ratio = qcdClosure.Clone(); qcdClosure_ratio.SetName("closure")
qcdClosure_ratio.Divide(qcdMCH)
qcdClosure_ratio.Draw()
qcdClosure_ratio.SetMaximum(5)
qcdClosure_ratio.SetMinimum(0)
#cR.SaveAs("%s_qcdDD_closure_ratio.pdf"%fin.GetName())
copyAndStoreCanvas("%s_qcdDD_closure_ratio.pdf"%fin.GetName(),cR,pdir)


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
mcYC = " | ".join(["%9.2f"%((1./BLINDFACTOR)*qcdClosure.GetBinContent(b)*qcdClosure.GetBinWidth(b)) for b in range(1,qcdH.GetNbinsX()+1)]) 
print ("clo.|",mcYC)

# --------------------------------------------------------------- end of 5.
if not options.mkworkspace: 
  print ("Plots stored in ", fout.GetName())
  fout.Close()
  sys.exit()
# 6. Make the histogram for the workspace ! 

rebinned_mjj = [200,400,600,900,1200,1500,2000,2750,5000]
if "VTR" in mystring:
  rebinned_mjj = [900,1200,1500,2000,2750,5000]

# qcdH = rebin(qcdH, rebinned_mjj)
# qcdH_shape_up = rebin(qcdH_shape_up, rebinned_mjj)
# qcdH_shape_down = rebin(qcdH_shape_down, rebinned_mjj)

# make an original histogram (proper hist)
qcdCountHisto = makebinned(qcdH)
if ( qcdCountHisto.Integral() != 0 ):
   qcdCountHisto.Scale((norm_qcd/BLINDFACTOR)/qcdCountHisto.Integral())
fout.WriteTObject(qcdCountHisto)

# make a helpful scale-factor 
histo_background_scale_factor = ROOT.TH1F("bkg_sf","background SF from fit",1,0,1)
histo_background_scale_factor.SetBinContent(1,1.)
fout.WriteTObject(histo_background_scale_factor)

#  Write the total that has the unccertainties 
fout.WriteTObject(hist_f_total_with_errors_toSave)

# and shape uncertainties 

qcdCountH_shape_up = makebinned(qcdH_shape_up); 
if ( qcdCountH_shape_up.Integral() > 0 ):
   qcdCountH_shape_up.Scale((norm_qcd/BLINDFACTOR)/qcdCountH_shape_up.Integral())
qcdCountH_shape_dn = makebinned(qcdH_shape_dn);
if ( qcdCountH_shape_dn.Integral() > 0 ):
   qcdCountH_shape_dn.Scale((norm_qcd/BLINDFACTOR)/qcdCountH_shape_dn.Integral())

#sys.exit()
#fout.cd()
#ROOT.SetOwnership( wspace, True )
lVarFit = ROOT.RooRealVar("mjj_%s"%(mystring.replace(" ","_")),"M_{jj} (GeV)",xmin,5000);

qcd_dh_nominal = ROOT.RooDataHist("QCD_DD","QCD Data-driven",ROOT.RooArgList(lVarFit),qcdCountHisto)
qcd_dh_up      = ROOT.RooDataHist("QCD_DD_Multijet_%s_shapeUncertaintyUp"%((options.label).replace(" ","_"))  ,"QCD Data-driven (shape up)"   ,ROOT.RooArgList(lVarFit),qcdCountH_shape_up)
qcd_dh_down    = ROOT.RooDataHist("QCD_DD_Multijet_%s_shapeUncertaintyDown"%((options.label).replace(" ","_")),"QCD Data-driven (shape down))",ROOT.RooArgList(lVarFit),qcdCountH_shape_dn)

getattr(wspace,"import")(qcd_dh_nominal)
getattr(wspace,"import")(qcd_dh_up)     
getattr(wspace,"import")(qcd_dh_down)   
fout.WriteTObject(wspace)
print ("Plots and workspace stored in ", fout.GetName())

wspace.Delete()
# --------------------------------------------------------------- end of 6.

# 7. And finally the HF histogram for the workspace ! 

# if not "VTR" in mystring:
#    sys.exit()

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


