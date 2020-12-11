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

def Ratio(a,b):
  ret = a.Clone(); ret.SetName(a.GetName()+"_"+b.GetName())
  ret.Divide(b)
  return ret

def runValidator(tf,ytitle,ymin,ymax,out,lstr,clab): 
	fdummy = ROOT.TFile.Open("%s/fitDiagnostics%s.root"%(BASE_DIRECTORY,sys.argv[1]))
	hdummy = fdummy.Get("shapes_prefit/%s_SR/qqH_hinv"%sys.argv[1])

	data = hdummy.Clone(); data.SetName("data")
	rata  = hdummy.Clone(); rata.SetName("ratio")
	ratae = hdummy.Clone(); ratae.SetName("ratio")
	ratae_nostat = hdummy.Clone(); ratae_nostat.SetName("ratio_nostat")
	ratae_noexp = hdummy.Clone(); ratae_noexp.SetName("ratio_noexp")

	nbins = hdummy.GetNbinsX() 

	lists_of_uncertainties = [] 
	for b in range(1,nbins+1):
	  de = tf.calcRdata(b)
	  data.SetBinContent(b,de[0])
	  data.SetBinError(b,de[1])

	  rth = tf.calcR(b)
	  print "bin %d"%b,"ratio_th=", rth, "data-bkg rat=", de[0],"+/-",de[1],
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

	c = ROOT.TCanvas("c","c",960,640)

	
	lat = ROOT.TLegend(0.76,0.62,0.99,0.89)
	lat.SetBorderSize(0)
	lat.SetTextFont(42)
	lat.AddEntry(data,"Data - bkg","PEL")
	lat.AddEntry(rata,"Prediction","L")
	lat.AddEntry(ratae_nostat, "#pm Th. uncert.","F")
	lat.AddEntry(ratae_noexp,"#pm MC stat. uncert.","F")
	lat.AddEntry(ratae, "#pm expt.","F")
	
	pad1 = ROOT.TPad("pad1","pad1",0,0.32,1,0.9)
	pad2 = ROOT.TPad("pad2","pad2",0,0,1,0.31)
	pad1.Draw()
	pad1.SetBottomMargin(0.05)
	pad1.SetTicky()
	pad1.SetTickx()
	
	pad1.SetRightMargin(0.25)
	pad1.SetLeftMargin(0.11)
	pad1.SetTopMargin(0.02)
	pad1.SetBottomMargin(0.02)

	pad2.SetRightMargin(0.25)
	pad2.SetLeftMargin(0.11)
	pad2.SetTopMargin(0.02)
	pad2.SetBottomMargin(0.32)

	pad1.cd()

	ratae.SetTitle("")
	ratae.GetXaxis().SetNdivisions(510)
	ratae.GetYaxis().SetTitleSize(0.06)
	ratae.GetYaxis().SetTitleOffset(0.7)
	ratae.GetXaxis().SetTitleSize(0.0)
	ratae.GetXaxis().SetLabelSize(0.0)

	ratae.SetFillColor(ROOT.kGray+2)
	ratae_noexp.SetFillColor(ROOT.kGray+1)
	ratae_nostat.SetFillColor(ROOT.kGray)
	#ratae.GetYaxis().SetTitle("Z#rightarrow #mu#mu / W#rightarrow #mu#nu")
	ratae.GetYaxis().SetTitle(ytitle)
	ratae.SetMinimum(float(ymin))
	ratae.SetMaximum(float(ymax))
	ratae.GetXaxis().SetNdivisions(010)
	ratae.GetXaxis().SetTitle("M_{jj} (GeV)")

	ratae.Draw("E2")
	ratae_noexp.Draw("E2same")
	ratae_nostat.Draw("E2same")
	rata.Draw("histsame")
	data.Draw("PELsame")

	pad1.RedrawAxis()

	c.cd()
	pad2.Draw()
        pad2.cd()

	ratae_r = Ratio(ratae,rata)
	ratae_noexp_r  = Ratio(ratae_noexp,rata)
	ratae_nostat_r = Ratio(ratae_nostat,rata)
	data_r  = Ratio(data,rata)
	rata_r  = Ratio(rata,rata)

	data_r.SetTitle("")
	data_r.GetXaxis().SetNdivisions(510)
	data_r.GetXaxis().SetTitleSize(0.12)
	data_r.GetXaxis().SetTitleOffset(1.1)
	data_r.GetYaxis().SetTitleOffset(0.5)
	data_r.GetXaxis().SetLabelSize(0.08)
	data_r.GetYaxis().SetTitleSize(0.08)
	data_r.GetYaxis().SetLabelSize(0.08)
	data_r.GetYaxis().SetTitle("Data/Prediction")

	data_r.Draw("PEL")
	ratae_r.Draw("E2same")
	ratae_noexp_r.Draw("E2same")
	ratae_nostat_r.Draw("E2same")
	rata_r.Draw("histsame")
	data_r.Draw("PELsame")

	pad2.SetTicky()
	pad2.RedrawAxis()

	c.cd()
	lat.Draw()
	tlat = ROOT.TLatex()
	tlat.SetTextFont(42)
	tlat.SetNDC()
	#tlat.DrawLatex(0.11,0.92,"#bf{CMS} #it{Preliminary}")
	tlat.DrawLatex(0.11,0.92,"#bf{CMS}")
	tlat.DrawLatex(0.44,0.92,lstr)
	tlat.SetTextSize(0.04)
	tlat.DrawLatex(0.14,0.83,clab)

	c.RedrawAxis()


	c.SaveAs("%s.pdf"%out)
	c.SaveAs("%s.png"%out)

	  
	lists_of_uncertainties = list(set(lists_of_uncertainties))
	writeout = open("bands_%s.txt"%out,"w")
	writeout.write("All uncertainties included in RMS...")
	for uncert in lists_of_uncertainties: writeout.write(uncert+"\n")


# inputs are cat ZProc, WProc, ZR, WR, ytitle, ymin, ymax, outname
def checkLoadAndRun(year): 
	if "photon" in sys.argv[3]:
	  # better check if it makes sense in this case 
	  if "VTR" in sys.argv[1]: 
	    print "No photon CR in VTR, skipping"
	    return 0 
	    #sys.exit("No photon CR in VTR, skipping")
	  import plotRatiosPhotons
	  tf = plotRatiosPhotons.TFValidator("%s/%s.root"%(BASE_DIRECTORY,sys.argv[1]),"%s/fitDiagnostics%s.root"%(BASE_DIRECTORY,sys.argv[1]))
	  tf.PProc = sys.argv[3]
	  tf.PR = sys.argv[5]
	else : 
	  import plotRatios 
	  tf = plotRatios.TFValidator("%s/%s.root"%(BASE_DIRECTORY,sys.argv[1]),"%s/fitDiagnostics%s.root"%(BASE_DIRECTORY,sys.argv[1]))
	  tf.WProc = sys.argv[3]
	  tf.WR = sys.argv[5]

	tf.cat   = sys.argv[1]
	tf.ZProc = sys.argv[2]
	tf.ZR = sys.argv[4]

  	
	tf.year = year

	return tf

ytitle = sys.argv[6]
ymin = sys.argv[7]
ymax = sys.argv[8]
out  = sys.argv[9]
clab = sys.argv[10]#

year = "2018"
lstr = "59.7 fb^{-1} (13 TeV, 2018)" 
if "2017" in sys.argv[1] : 
 year = "2017"
 if "VTR" in sys.argv[1] : lstr = "36.7 fb^{-1} (13 TeV, 2017)"
 else : lstr = "41.5 fb^{-1} (13 TeV, 2017)"
tf = checkLoadAndRun(year)
if tf!=0 : runValidator(tf,ytitle,ymin,ymax,out,lstr,clab)
