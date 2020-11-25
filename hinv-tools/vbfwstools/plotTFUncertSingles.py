import ROOT 
import transferFactorSys
import sys


ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)

tf = transferFactorSys.TFSystematics("%s"%(sys.argv[1]))
# inputs are cat Numerator Proc, Denominator proc, Num Region, Denom Region, ytitle, ymin, ymax, outname
tf.nbins = int(sys.argv[3])
tf.cat = sys.argv[2]
tf.Xvar= "mjj_"+tf.cat
tf.Numerator  = sys.argv[8]#"WJETS_WMUNU"
tf.Denominator =sys.argv[9]#  "WJETS_SR"

ymin = sys.argv[4]
ymax = sys.argv[5]
lstr =  sys.argv[6] #"41.5 fb^{-1} (13 TeV, 2017)"
clab =  sys.argv[7] #"MTR"
# first draw the central values 

#print """
#tf.nbins = %d
#tf.cat = %s
#tf.Xvar= %s
#tf.Numerator  = %s
#tf.Denominator = %s

#ymin = %s
#ymax = %s
#lstr = %s
#clab = %s
#"""%(tf.nbins,tf.cat,tf.Xvar,tf.Numerator,tf.Denominator,ymin,ymax,lstr,clab)

hcentral = ROOT.TH1F("central",";m_{jj} (GeV);%s / %s;"%(tf.Numerator,tf.Denominator),int(tf.nbins),tf.getBins())
for b in range(1,(tf.nbins)+1): 
  hcentral.SetBinContent(b,tf.calcR(b))

hcentral.SetMarkerColor(1)
hcentral.SetMarkerStyle(20)
hcentral.SetLineWidth(2)
hcentral.SetLineColor(1)
hcentral.SetTitle("")
hcentral.GetYaxis().SetTitleSize(0.032)
hcentral.GetYaxis().SetTitleOffset(0.98)
hcentral.GetXaxis().SetTitleSize(0.06)
hcentral.GetXaxis().SetLabelSize(0)
#hcentral.GetYaxis().SetTitle(ytitle)
hcentral.SetMinimum(float(ymin))
hcentral.SetMaximum(float(ymax))
#hcentral.SetMinimum(0.5)
#hcentral.SetMaximum(1.5)
hcentral.GetXaxis().SetNdivisions(010)

leg = ROOT.TLegend(0.76,0.11,0.99,0.92)
leg.SetBorderSize(0)
leg.SetTextFont(42)
leg.AddEntry(hcentral,"Nominal #pm MC. stat","PEL")

# Now the variations 
allpars = tf.list_of_parameters()
allh=[]
icol=1
istyle=0
iter = allpars.createIterator()
allstat = []
allewk = []
while 1:
  tpar = iter.Next() # allpars.at(n)
  if tpar == None : break
  print" found parameter ", tpar.GetName()
  if "ewkqcdratio_stat" in tpar.GetName(): continue 
  if "QCDZ_SR_bin" in tpar.GetName() : continue
  if "NLOSF_" in tpar.GetName() : continue
  #if "QCDwzratio_stat_bin" in tpar.GetName(): continue
  
  #if not ("EWKwzratio" in tpar.GetName() or "QCDwzratio" in tpar.GetName()): continue 
  #print " continue " 
  if "stat_" in tpar.GetName(): 
   print "Add to stat ", tpar.GetName()
   allstat.append(tpar)
   continue
  
  if "EWK_corr_" in tpar.GetName(): 
   print "Add to corr ", tpar.GetName()
   allewk.append(tpar)
   continue

  if tpar.isConstant(): continue 
  print " Adding parameter --> ", tpar.GetName()
  up = tf.gimmeHist(tpar,hcentral,1)
  down = tf.gimmeHist(tpar,hcentral,-1)
  colorthis = icol%9+1
  if colorthis == 5 : colorthis = 800
  if colorthis == 3 : colorthis = ROOT.kGreen+2
  up.SetLineColor(colorthis)
  down.SetLineColor(colorthis)
  up.SetLineStyle(icol//9+1)
  down.SetLineStyle(icol//9+1)
  up.SetLineWidth(2)
  down.SetLineWidth(2)
  up.SetName(tpar.GetName()+"_Up")
  down.SetName(tpar.GetName()+"_Down")
  allh.append(up)
  allh.append(down)
  
  leg.AddEntry(allh[-1],tpar.GetName(),"L")
  istyle+=1
  icol+=1

tgStat = ROOT.TGraphAsymmErrors()
tgStat.SetMarkerStyle(20)
tgStat.SetMarkerColor(1)
tgStat.SetMarkerSize(1)

tgEWK = ROOT.TGraphAsymmErrors()
tgEWK.SetMarkerStyle(0)
tgEWK.SetMarkerColor(ROOT.kOrange)
tgEWK.SetLineColor(ROOT.kOrange)
tgEWK.SetMarkerColor(0)
tgEWK.SetMarkerSize(0)
tgEWK.SetFillColor(ROOT.kOrange)

# now we add any stat uncertainties 
for b in range(1,(tf.nbins)+1):
 erru = 0 
 errd = 0 
 for i,spar in enumerate(allstat): 
   up = tf.gimmeHist(spar,hcentral,1)
   dn = tf.gimmeHist(spar,hcentral,-1)
   print "bin", b, up.GetName(),  abs(up.GetBinContent(b)-hcentral.GetBinContent(b))
   erru+=(abs(up.GetBinContent(b)-hcentral.GetBinContent(b)))**2
   errd+=(abs(dn.GetBinContent(b)-hcentral.GetBinContent(b)))**2
 hcv = hcentral.GetBinContent(b)
 tgStat.SetPoint(b-1,hcentral.GetBinCenter(b),1)#hcentral.GetBinContent(b))
 tgStat.SetPointError(b-1,0,0,(errd**0.5)/hcv,(erru**0.5)/hcv)

for b in range(1,(tf.nbins)+1):
 erru = 0 
 errd = 0 
 for i,spar in enumerate(allewk): 
   up = tf.gimmeHist(spar,hcentral,1)
   dn = tf.gimmeHist(spar,hcentral,-1)
   erru+=(abs(up.GetBinContent(b)-hcentral.GetBinContent(b)))**2
   errd+=(abs(dn.GetBinContent(b)-hcentral.GetBinContent(b)))**2
 hcv = hcentral.GetBinContent(b)
 bw = hcentral.GetBinWidth(b)/2
 tgEWK.SetPoint(b-1,hcentral.GetBinCenter(b),1)#hcentral.GetBinContent(b))
 tgEWK.SetPointError(b-1,bw,bw,(errd**0.5)/hcv,(erru**0.5)/hcv)
 print "bin", b, erru

  
leg.AddEntry(tgEWK,"#pm EWK NLO syst.","F")

c = ROOT.TCanvas("c","c",960,640)
#c.SetBottomMargin(0.15)
#c.SetRightMargin(0.25)
pad2 = ROOT.TPad("p1","p1",0.0,0.0,1,0.25)
pad1 = ROOT.TPad("p2","p2",0.0,0.25,1,0.95)
pad1.SetBottomMargin(0.014)
pad1.SetTopMargin(0.05)
pad2.SetTopMargin(0.035)
pad2.SetBottomMargin(0.4)
pad1.SetLeftMargin(0.1)
pad2.SetLeftMargin(0.1)
pad1.SetRightMargin(0.25)
pad2.SetRightMargin(0.25)
pad1.Draw()
pad2.Draw()

c.cd()
for h in allh: h.Divide(hcentral)
#tgStat.Divide(hcentral)
hcentral.Divide(hcentral)


leg.Draw()

tlat = ROOT.TLatex()
tlat.SetTextFont(42)
tlat.SetNDC()
tlat.DrawLatex(0.11,0.94,"#bf{CMS} #it{Preliminary}")
tlat.DrawLatex(0.44,0.94,lstr)
tlat.SetTextSize(0.04)
tlat.DrawLatex(0.14,0.86,clab)

c.SetTicky()
c.SetTickx()
c.SetGridy()
#c.SetGridx()
lines = []
tlat.SetTextSize(0.02)
tlat.SetNDC(False)

pad1.cd()
hcentral.Draw("histP")
tgEWK.Draw("e2")
for h in allh: h.Draw("histsame")
for i in range(2,(tf.nbins)+1): 
  le = hcentral.GetBinLowEdge(i)
  lc = hcentral.GetBinCenter(i-1)
  l = ROOT.TLine(le,hcentral.GetMinimum(),le,hcentral.GetMaximum())
  l.SetLineColor(1)
  l.SetLineStyle(2)
  lines.append(l)
  errl = tgStat.GetErrorYlow(i-2)
  errh = tgStat.GetErrorYhigh(i-2)
  #tlat.DrawLatex(lc,hcentral.GetMaximum()*0.8,"+%.2f -%.2f"%(errl,errh))
for l in lines: l.Draw()

pad1.SetGridy()
c.cd()
pad2.cd()
pad2.SetGridy()
pad2.SetTicky()
pad2.SetTickx()
haxis = ROOT.TH1F("haxis","",int(tf.nbins),tf.getBins())
haxis.SetMaximum(tgStat.GetYaxis().GetXmax())
haxis.SetMinimum(tgStat.GetYaxis().GetXmin())
haxis.GetXaxis().SetRangeUser(hcentral.GetXaxis().GetXmin(),hcentral.GetXaxis().GetXmax())
haxis.GetYaxis().SetLabelSize(0.03)
haxis.GetYaxis().SetNdivisions(010)
haxis.GetXaxis().SetLabelSize(0.15)
haxis.GetXaxis().SetTitle(hcentral.GetXaxis().GetTitle())
haxis.GetYaxis().SetLabelSize(0.1)
haxis.GetXaxis().SetTitleOffset(0.98)
haxis.GetXaxis().SetTitleSize(0.18)
haxis.Draw("axis")
tgStat.Draw("pe")
pad2.SetGridy()
pad2.RedrawAxis()

c.cd()
c.RedrawAxis()
c.SaveAs("single_tf_uncert_VBF_%s_%s_%s.pdf"%(tf.cat,tf.Numerator,tf.Denominator))
c.SaveAs("single_tf_uncert_VBF_%s_%s_%s.png"%(tf.cat,tf.Numerator,tf.Denominator))

fout = ROOT.TFile("single_tf_uncert_VBF_%s_%s_%s.root"%(tf.cat,tf.Numerator,tf.Denominator),"RECREATE")
hcentral.SetName("nominal")
hcentral.Write()
tgStat.SetName("MC_stat")
tgStat.Write()
tgEWK.SetName("EWK_uncert")
tgEWK.Write()
for h in allh: 
 h.Write()
fout.Close()
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
