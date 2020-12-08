import ROOT 
import transferFactorSys
import sys

BASE_DIRECTORY="fast_datacard_input_200127"

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

# inputs are cat Numerator Proc, Denominaor proc, Num Region, Denom Region, ytitle, ymin, ymax, outname
tf = transferFactorSys.TFSystematics("%s/test_df_%s_2020v1/all_percategory.root"%(BASE_DIRECTORY,sys.argv[1]))
tf.nbins = int(sys.argv[2])
tf.cat = sys.argv[1]
tf.Xvar= "mjj_"+sys.argv[1]
tf.Numerator  = sys.argv[7]#"WJETS_WMUNU"
tf.Denominator =sys.argv[8]#  "WJETS_SR"

ymin = sys.argv[3]
ymax = sys.argv[4]
lstr =  sys.argv[5] #"41.5 fb^{-1} (13 TeV, 2017)"
clab =  sys.argv[6] #"MTR"
# first draw the central values 


hcentral = ROOT.TH1F("central",";m_{jj} (GeV);%s / %s;"%(tf.Numerator,tf.Denominator),int(tf.nbins),tf.getBins())
for b in range(1,(tf.nbins)+1): 
  hcentral.SetBinContent(b,tf.calcR(b))

hcentral.SetMarkerColor(1)
hcentral.SetMarkerStyle(20)
hcentral.SetLineWidth(2)
hcentral.SetLineColor(1)
hcentral.SetTitle("")
hcentral.GetYaxis().SetTitleSize(0.06)
hcentral.GetYaxis().SetTitleOffset(0.8)
hcentral.GetXaxis().SetTitleSize(0.06)
#hcentral.GetYaxis().SetTitle(ytitle)
#hcentral.SetMinimum(float(ymin))
#hcentral.SetMaximum(float(ymax))
hcentral.SetMinimum(float(ymin))
hcentral.SetMaximum(float(ymax))
hcentral.GetXaxis().SetNdivisions(010)

leg = ROOT.TLegend(0.76,0.1,0.99,0.89)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.AddEntry(hcentral,"Nominal #pm stat","PEL")

# Now the variations 
allpars = tf.list_of_parameters()
allh=[]
icol=1
istyle=0
iter = allpars.createIterator()
allstat = []
while 1:
  tpar = iter.Next() # allpars.at(n)
  if tpar == None : break
  print" found parameter ", tpar.GetName()
  if "ewkqcdratio_stat" in tpar.GetName(): continue # not sure why these should be in there ?
  if "QCDZ_SR_bin" in tpar.GetName() : continue
  #if "_QCDwzratio_" in tpar.GetName(): continue 
  #if "QCDwzratio_stat_bin" in tpar.GetName(): continue

  if "stat_" in tpar.GetName(): 
   allstat.append(tpar)
   continue

  if tpar.isConstant(): continue 
  print " Adding parameter --> ", tpar.GetName()
  up = tf.gimmeHist(tpar,hcentral,1)
  down = tf.gimmeHist(tpar,hcentral,-1)
  colorthis = icol%9+1
  if colorthis == 5 : colorthis = 800
  up.SetLineColor(colorthis)
  down.SetLineColor(colorthis)
  up.SetLineStyle(icol//9+1)
  down.SetLineStyle(icol//9+1)
  allh.append(up)
  allh.append(down)
  leg.AddEntry(allh[-1],tpar.GetName(),"L")
  istyle+=1
  icol+=1

tgStat = ROOT.TGraphAsymmErrors()
tgStat.SetMarkerStyle(20)
tgStat.SetMarkerColor(1)
tgStat.SetMarkerSize(1)

# now we add any stat uncertainties 
for b in range(1,(tf.nbins)+1):
 erru = 0 
 errd = 0 
 for i,spar in enumerate(allstat): 
   up = tf.gimmeHist(spar,hcentral,1)
   dn = tf.gimmeHist(spar,hcentral,-1)
   erru+=(abs(up.GetBinContent(b)-hcentral.GetBinContent(b)))**2
   errd+=(abs(dn.GetBinContent(b)-hcentral.GetBinContent(b)))**2
 hcv = hcentral.GetBinContent(b)
 tgStat.SetPoint(b-1,hcentral.GetBinCenter(b),1)#hcentral.GetBinContent(b))
 tgStat.SetPointError(b-1,0,0,(errd**0.5)/hcv,(erru**0.5)/hcv)

  

c = ROOT.TCanvas("c","c",960,640)
c.SetBottomMargin(0.15)
c.SetRightMargin(0.25)

for h in allh: h.Divide(hcentral)
#tgStat.Divide(hcentral)
hcentral.Divide(hcentral)

hcentral.Draw("histP")
for h in allh: h.Draw("histsame")
tgStat.Draw("pe")
leg.Draw()

tlat = ROOT.TLatex()
tlat.SetTextFont(42)
tlat.SetNDC()
#tlat.DrawLatex(0.11,0.92,"#bf{CMS} #it{Preliminary}")
tlat.DrawLatex(0.11,0.92,"#bf{CMS}")
tlat.DrawLatex(0.44,0.92,lstr)
tlat.SetTextSize(0.04)
tlat.DrawLatex(0.14,0.83,clab)

c.SetTicky()
c.SetTickx()
c.SetGridy()
c.SetGridx()
c.RedrawAxis()
c.SaveAs("%s_%s_%s.pdf"%(tf.cat,tf.Numerator,tf.Denominator))
c.SaveAs("%s_%s_%s.png"%(tf.cat,tf.Numerator,tf.Denominator))

"""


    iter = allpars.createIterator()
    while 1:
     tpar = iter.Next() # allpars.at(n)
     if tpar == None : break

     # ignore theory uncertainties - also of course, ignore scale factors (float params)
     # not even sure of the first 2 but they are constant at least 
     if "TF_syst_fnlo_SF" in tpar.GetName(): continue 
     if "ewkqcdratio_stat" in tpar.GetName(): continue 
     if "QCDwzratioQCDcorrSyst" in tpar.GetName(): continue 
     if "EWKwzratioQCDcorrSyst" in tpar.GetName(): continue 
     if "QCDwzratio_EWK_corr_on_Strong" in tpar.GetName(): continue 
     if "EWKwzratio_EWK_corr_on_Strong_bin" in tpar.GetName(): continue 
     if "QCDwzratio_stat_bin" in tpar.GetName(): continue
     if "QCDZ_SR_bin" in tpar.GetName() : continue
 """
