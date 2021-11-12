import ROOT 
import sys
import os

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)


BASE_DIRECTORY="../../../"

"""
tf.ZProc = "mumu"
tf.WProc = "munu"
tf.ZR = "MUMU"
tf.WR = "MUNU"
"""

isPublished = True

def RatioD(a,b):
  ret = a.Clone(); ret.SetName(a.GetName()+"_"+b.GetName())
  for i in range(b.GetNbinsX()): 
    v = a.GetY()[i]
    vel = a.GetErrorYlow(i)
    veu = a.GetErrorYhigh(i)
    u = b.GetBinContent(i+1)

    ret.SetPoint(i,a.GetX()[i],v/u)
    ret.SetPointError(i,0,0,vel/u,veu/u)
  return ret

def Ratio(a,b):
  ret = a.Clone(); ret.SetName(a.GetName()+"_"+b.GetName())
  ret.Divide(b)
  return ret

def average(x,y):
 return (abs(x)+abs(y))/2

def getAveragePull(gr):
  	Npoints = gr.GetN()-1
	rms  = 0 
	mean = 0
	for p in range(Npoints): 
	  mean += (average(gr.GetErrorYhigh(p),gr.GetErrorYlow(p)))
	return mean/Npoints

def runValidator(tf,ytitle,ymin,ymax,out,lstr,clab,pos=0): 
	fdummy = ROOT.TFile.Open("%s/fitDiagnostics%s.root"%(BASE_DIRECTORY,sys.argv[1]))
	hdummy = fdummy.Get("shapes_prefit/%s_SR/qqH_hinv"%sys.argv[1])
	ddummy = fdummy.Get("shapes_prefit/%s_SR/data"%sys.argv[1])

	data  = ddummy.Clone(); data.SetName("data")
	rata  = hdummy.Clone(); rata.SetName("ratio")
	ratae = hdummy.Clone(); ratae.SetName("ratio")
	ratae_nostat = hdummy.Clone(); ratae_nostat.SetName("ratio_nostat")
	ratae_noexp = hdummy.Clone(); ratae_noexp.SetName("ratio_noexp")

	nbins = hdummy.GetNbinsX() 

	lists_of_uncertainties = [] 
	for b in range(1,nbins+1):
	  de = tf.calcRdata(b)
	  data.SetPoint(b-1,ddummy.GetX()[b-1],de[0])
	  data.SetPointError(b-1,0,0,de[1],de[2])

	  rth = tf.calcR(b)
	  print "bin %d"%b,"ratio_th=", rth, "data-bkg rat=", de[0],"-",de[1], "+", de[2]
	  print "check ", data.GetErrorYlow(b-1),data.GetErrorYhigh(b-1) 
	  rata.SetBinContent(b,rth)
	  rata.SetBinError(b,0)
	  ratae.SetBinContent(b,rth)
	  etot = tf.returnRMS(b,True,True)
	  for uncert in etot[1]: 
	    lists_of_uncertainties.append(uncert)
	  #etot=1.
	  ratae.SetBinError(b,etot[0])

	  ratae_noexp.SetBinContent(b,rth)
	  e_noexp = tf.returnRMS(b,True,False)[0]
	  #e_noexp=1.
	  ratae_noexp.SetBinError(b,e_noexp)

	  ratae_nostat.SetBinContent(b,rth)
	  e_nostat = tf.returnRMS(b,False,False)[0]
	  ratae_nostat.SetBinError(b,e_nostat)
	  print " ... relative uncert = ", e_nostat/rth 


        rata_pf = hdummy.Clone(); rata_pf.SetName("ratio_postfit")
	rata_pf.SetLineColor(2)

	for b in range(1,nbins+1):
	  tf.setPostFit(b)
	  rat_postfit = tf.calcR(b)
	  rata_pf.SetBinContent(b,rat_postfit)

	rata_pf.SetLineColor(2)
	rata_pf.SetLineWidth(3)
	rata_pf_rat = rata_pf.Clone()
	rata_pf_rat.SetName("ratio_postfit_ratio")
	rata_pf_rat.Divide(rata)

	data.SetMarkerStyle(20)
	data.SetMarkerSize(1.2)
	data.SetLineWidth(2)
	data.SetLineColor(1)

	ratae_nostat.SetLineColor(0)
	ratae_nostat.SetLineWidth(3)
	ratae_noexp.SetLineColor(0)
	ratae_noexp.SetLineWidth(3)
	ratae.SetLineColor(0)
	ratae.SetLineWidth(3)
	rata.SetLineColor(4)
	rata.SetLineWidth(3)

	c = ROOT.TCanvas("c","c",820,820)

	
	if pos==0: 
	 lat = ROOT.TLegend(0.16,0.05,0.68,0.28)
	 leg.SetNColumns(2)

	lab = tf.cat.replace("_"," ")
	
	lat.SetTextSize(0.044)
	lat.SetBorderSize(0)
	lat.SetTextFont(42)
	lat.AddEntry(data,"Data - bkg.","PE")
	lat.AddEntry(ratae_nostat, "#pm Th. uncert.","F")
	lat.AddEntry(rata_pf,"Prediction (CR-postfit)","L")
	lat.AddEntry(ratae_noexp,"#pm MC stat. uncert.","F")
	lat.AddEntry(rata,"Prediction (prefit)","L")
	lat.AddEntry(ratae, "#pm expt.","F")
	
	pad1 = ROOT.TPad("pad1","pad1",0,0.305,1,0.95)
	pad2 = ROOT.TPad("pad2","pad2",0,0.0,1,0.30)
	pad1.Draw()
	pad1.SetTicky()
	pad1.SetTickx()
	
	pad1.SetBottomMargin(0.0175)
	pad1.SetTopMargin(0.05)
	pad2.SetTopMargin(0.044)
	pad2.SetBottomMargin(0.36)
	pad1.SetLeftMargin(0.13)
	pad2.SetLeftMargin(0.13)
	pad1.SetRightMargin(0.06)
	pad2.SetRightMargin(0.06)

	pad1.cd()

	ratae.SetTitle("")
	ratae.GetYaxis().SetNdivisions(510)
	ratae.GetYaxis().SetTitleSize(0.08)
	ratae.GetYaxis().SetLabelSize(0.05)
	ratae.GetYaxis().SetTitleOffset(0.66)
	ratae.GetXaxis().SetTitleSize(0.0)
	ratae.GetXaxis().SetLabelSize(0.0)

	ratae.SetFillColor(ROOT.kGray+2)
	ratae_noexp.SetFillColor(ROOT.kGray+1)
	ratae_nostat.SetFillColor(ROOT.kGray)
	#ratae.GetYaxis().SetTitle("Z#rightarrow #mu#mu / W#rightarrow #mu#nu")
	ratae.GetYaxis().SetTitle(ytitle)
	ratae.SetMinimum(float(ymin))
	ratae.SetMaximum(float(ymax))
	#ratae.GetXaxis().SetNdivisions(010)
	ratae.GetXaxis().SetTitle("M_{jj} (GeV)")

	ratae.Draw("E2")
	ratae_noexp.Draw("E2same")
	ratae_nostat.Draw("E2same")
	rata.Draw("histsame")
	rata_pf.Draw("histsame")
	data.Draw("PE0same")

	pad1.RedrawAxis()

	c.cd()
	pad2.Draw()
        pad2.cd()

	ratae_r = Ratio(ratae,rata)
	ratae_noexp_r  = Ratio(ratae_noexp,rata)
	ratae_nostat_r = Ratio(ratae_nostat,rata)
	data_r  = RatioD(data,rata)
	rata_r  = Ratio(rata,rata)

	# check if the last bin error is significantly different to the others 
	error_rms = getAveragePull(data_r)
	pm1 = data_r.GetN()-1
	data_r_skipLastBin = data_r.Clone(); data_r_skipLastBin.SetName("not_important")
	textpoints =[]
	if average(data_r.GetErrorYlow(pm1),data_r.GetErrorYhigh(pm1)) > 3*error_rms:
		data_r_skipLastBin.SetPoint(data_r.GetN()-1,data_r.GetX()[data_r.GetN()-1],data_r.GetY()[data_r.GetN()-1])
		#data_r_skipLastBin.SetPoint(data_r.GetN()-1,data_r.GetX()[data_r.GetN()-1],1)
		data_r_skipLastBin.SetPointError(data_r.GetN()-1,0,0,0,0)
		data_r_skipLastBin.Draw()
		if data_r.GetY()[pm1-1] < 1 : ytext = data_r_skipLastBin.GetYaxis().GetXmin()*1.4
		else: ytext = data_r_skipLastBin.GetYaxis().GetXmax()*0.6
		#textpoints.append([rata_r.GetBinLowEdge(pm1+1),ytext,data_r.GetY()[pm1],data_r.GetErrorYlow(pm1),data_r.GetErrorYhigh(pm1)])

	
	rata_r.SetTitle("")
	rata_r.GetYaxis().SetNdivisions(010)
	rata_r.GetXaxis().SetRangeUser(rata_r.GetXaxis().GetXmin(),rata_r.GetXaxis().GetXmax())
	rata_r.GetXaxis().SetTitleSize(0.125)
	rata_r.GetXaxis().SetTitleOffset(1.1)
	rata_r.GetYaxis().SetTitleOffset(0.5)
	rata_r.GetXaxis().SetLabelSize(0.09)
	rata_r.GetYaxis().SetTitleSize(0.095)
	rata_r.GetYaxis().SetLabelSize(0.09)
	rata_r.GetYaxis().SetTitle("(Data - bkg.) / prediction")
	rata_r.SetMaximum(data_r_skipLastBin.GetYaxis().GetXmax())
	rata_r.SetMinimum(max([data_r_skipLastBin.GetYaxis().GetXmin(),0]))
	
	rata_r.GetXaxis().SetTitle("M_{jj} (GeV)")
	rata_r.Draw("AXIS")
	data_r.Draw("PE")
	ratae_r.Draw("E2same")
	ratae_noexp_r.Draw("E2same")
	ratae_nostat_r.Draw("E2same")
	rata_r.Draw("histsame")
	rata_pf_rat.Draw("histsame")
	data_r.Draw("PE0same")

	latex_small = ROOT.TLatex()
	latex_small.SetTextFont(42)
	latex_small.SetTextSize(0.12)
	for lt in textpoints: 
	  latex_small.DrawLatex(lt[0],lt[1],"%.2f^{+%.2f}_{-%.2f}"%(lt[2],lt[3],lt[4]))
	pad2.SetTicky()
	pad2.SetTickx()
	pad2.RedrawAxis()

	pad1.cd()
	lat.Draw()
	c.cd()
	tlat = ROOT.TLatex()
	tlat.SetTextFont(42)
	tlat.SetNDC()
	#tlat.DrawLatex(0.11,0.92,"#bf{CMS} #it{Preliminary}")
	tlat.SetTextSize(0.042)
	if isPublished : tlat.DrawLatex(0.128,0.93,"#bf{CMS}")
	else : tlat.DrawLatex(0.128,0.93,"#bf{CMS} #it{Supplementary}")
	tlat.SetTextSize(0.042)
	tlat.DrawLatex(0.18,0.83,clab)
	tlat.SetTextSize(0.032)
	#tlat.SetTextAlign(32)
	tlat.DrawLatex(0.71,0.93,lstr)

	c.RedrawAxis()


	c.SaveAs("%s.pdf"%out)
	c.SaveAs("%s.png"%out)

	  
	lists_of_uncertainties = list(set(lists_of_uncertainties))
	writeout = open("bands_%s.txt"%out,"w")
	writeout.write("All uncertainties included in RMS...")
	for uncert in lists_of_uncertainties: writeout.write(uncert+"\n")


# inputs are cat ZProc, WProc, ZR, WR, ytitle, ymin, ymax, outname
def checkLoadAndRun(year,combineleptons=False):
  file_name = "%s/fitDiagnosticsCRonlyFit.root"%(BASE_DIRECTORY)
  if combineleptons:
	if "photon" in sys.argv[2]:
	  # better check if it makes sense in this case 
	  if "VTR" in sys.argv[1]: 
	    print "No photon CR in VTR, skipping"
	    return 0 
	    #sys.exit("No photon CR in VTR, skipping")
	  import plotRatiosPhotonsCombineFlavour
	  tf = plotRatiosPhotonsCombineFlavour.TFValidator("%s/%s.root"%(BASE_DIRECTORY,sys.argv[1]),file_name)

	else : 
	  print "New thing"
	  import plotRatiosCombineFlavour
	  tf = plotRatiosCombineFlavour.TFValidator("%s/%s.root"%(BASE_DIRECTORY,sys.argv[1]),file_name)

	tf.cat   = sys.argv[1]
	tf.year = year
	tf.setup()
	
  else: 
  	isPublished=False
	if "photon" in sys.argv[3]:
	  # better check if it makes sense in this case 
	  if "VTR" in sys.argv[1]: 
	    print "No photon CR in VTR, skipping"
	    return 0 
	    #sys.exit("No photon CR in VTR, skipping")
	  import plotRatiosPhotons
	  tf = plotRatiosPhotons.TFValidator("%s/%s.root"%(BASE_DIRECTORY,sys.argv[1]),file_name)
	  tf.PProc = sys.argv[3]
	  tf.PR = sys.argv[5]
	  tf.ZProc = "Z"+sys.argv[2]
	  tf.ZR = "Z"+sys.argv[4]
	else : 
	  import plotRatios 
	  tf = plotRatios.TFValidator("%s/%s.root"%(BASE_DIRECTORY,sys.argv[1]),file_name)
	  tf.WProc = sys.argv[3]
	  tf.WR = sys.argv[5]
	  tf.ZProc = sys.argv[2]
	  tf.ZR = sys.argv[4]

	tf.cat   = sys.argv[1]
	tf.year = year

  return tf

combinedleptons = False
if (sys.argv[2]=="lepton") or (sys.argv[2]=="photon"):
 combinedleptons = True
 ytitle = sys.argv[3]
 ymin = sys.argv[4]
 ymax = sys.argv[5]
 out  = sys.argv[6]
 clab = sys.argv[7]#
else:
 ytitle = sys.argv[6]
 ymin = sys.argv[7]
 ymax = sys.argv[8]
 out  = sys.argv[9]
 clab = sys.argv[10]#

pos=0
year = "2018"
lstr = "59.7 fb^{-1} (13 TeV)" 
if "2017" in sys.argv[1] : 
 year = "2017"
 if "VTR" in sys.argv[1] : lstr = "36.7 fb^{-1} (13 TeV)"
 else : lstr = "41.5 fb^{-1} (13 TeV)"
tf = checkLoadAndRun(year,combineleptons=(combinedleptons))
if tf!=0 : runValidator(tf,ytitle,ymin,ymax,out,lstr,clab,pos)
