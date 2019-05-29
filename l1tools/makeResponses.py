#Generic tool which makes "response" plots vs variables
#! /usr/env/python
import ROOT
import sys
import array 

fitDistribs = False
doDiff      = True 

ROOT.gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptFit(1111)
rand = ROOT.TRandom3()

treename = "entries"
cstr = ""  # add a cutr string applied to each entry
inputfilename = sys.argv[1]
outputfilename = sys.argv[2]

# Bunch of reasonable colors fill,line 
colors = [ 
	[ROOT.kBlue-8,ROOT.kBlue+3] 
,	[ROOT.kRed-8,ROOT.kRed+2]
,	[ROOT.kGreen-2,ROOT.kGreen+4] 
,	[ROOT.kOrange-2,ROOT.kBlack] 
,	[ROOT.kViolet-4,ROOT.kViolet] 
]



def getMeanAndRMS(hist):
 
 mean  = hist.GetMean()
 meanE = hist.GetMeanError()
 rms   = hist.GetRMS()
 rmsE  = hist.GetRMSError()
 if not  hist.GetEntries()>0 : return mean, meanE, rms, rmsE

 if fitDistribs: 
   tries = 0
   while tries < 3:
    hist.Fit("gaus","","",mean-rms,mean+rms)
    hist.Print()
    mean = hist.GetFunction("gaus").GetParameter(1)
    rms  = hist.GetFunction("gaus").GetParameter(2)
    meanE = hist.GetFunction("gaus").GetParError(1)
    rmsE  = hist.GetFunction("gaus").GetParError(2)

    tries+=1
 return mean, meanE, rms, rmsE,

# response plots are done in terms of bins along x-axis (in xbins) for different y bins 
def makeResponsePlots(inputfile,outputfile,quant,target,Xbins,xaxis,Ybins,yaxis):
 
 output_f	 = outputfile.mkdir("%s_%s_X_%s_Y_%s"%(quant,target,xaxis,yaxis))
 output_f.cd()
 output_f_hists  = output_f.mkdir("Histograms") 
 
 lat = ROOT.TLatex()
 lat.SetNDC()
 lat.SetTextFont(42); lat.SetTextSize(0.04)

 leg = ROOT.TLegend(0.55,0.7,0.94,0.94)
 leg.SetFillColor(0); leg.SetTextFont(42); leg.SetTextSize(0.04)

 leg2 = ROOT.TLegend(0.6,0.75,0.94,0.94)
 leg2.SetFillColor(0); leg.SetTextFont(42); leg.SetTextSize(0.04)

 tree_raw    = inputfile.Get(treename)

 all_grs    = []
 all_grsRMS = []
 
 for iY in range(len(Ybins)-1): 

  g_Y  = ROOT.TGraphAsymmErrors()
  g_YR = ROOT.TGraphAsymmErrors()

  cutY = "%s>=%g && %s<%g"%( yaxis,Ybins[iY],yaxis,Ybins[iY+1] )

  for iX in range(len(Xbins)-1): 

   cutX = "%s>=%g && %s<%g"%( xaxis,Xbins[iX],xaxis,Xbins[iX+1] )

   cut = cutX+" && "+cutY
   if cstr : cut+=" && %s "%cstr

   dstring = ""

   if doDiff : dstring = "%s-%s"%(quant,target)
   else : dstring = "%s/%s"%(quant,target)

   rnd = rand.Uniform()

   tree_raw.Draw(dstring+">>h_%g"%rnd,cut) 
   h = ROOT.gROOT.FindObject("h_%g"%rnd)
   h.SetName("hist_RSP_%s_%g_%g_%s_%g_%g"%(yaxis,Ybins[iY],Ybins[iY+1],xaxis,Xbins[iX],Xbins[iX+1]))
   h.GetXaxis().SetTitle(dstring)
   mean,meanE,rms,rmsE = getMeanAndRMS(h)  
   output_f_hists.WriteTObject(h)


   tree_raw.Draw(xaxis+">>h_X_%g"%rnd,cut) 
   hX = ROOT.gROOT.FindObject("h_X_%g"%rnd)
   hX.SetName("hist_X_%s_%g_%g_%s_%g_%g"%(yaxis,Ybins[iY],Ybins[iY+1],xaxis,Xbins[iX],Xbins[iX+1]))
   hX.GetXaxis().SetTitle(xaxis)
   xave =  hX.GetMean()
   output_f_hists.WriteTObject(hX)

   g_Y.SetPoint(iX,xave,mean)
   g_Y.SetPointError(iX,xave-Xbins[iX],Xbins[iX+1]-xave,meanE,meanE)


   g_YR.SetPoint(iX,xave,rms)
   g_YR.SetPointError(iX,xave-Xbins[iX],Xbins[iX+1]-xave,rmsE,rmsE)

  g_Y.SetName("%s_%g_%g"%(yaxis,Ybins[iY],Ybins[iY+1]))
  g_Y.GetXaxis().SetTitle(xaxis)
  g_Y.GetYaxis().SetTitle("<%s>"%dstring)

  g_YR.SetName("rms_%s_%g_%g"%(yaxis,Ybins[iY],Ybins[iY+1]))
  g_YR.GetXaxis().SetTitle(xaxis)
  g_YR.GetYaxis().SetTitle("RMS %s"%dstring)

  all_grs.append(g_Y)
  all_grsRMS.append(g_YR)
 
 cv = ROOT.TCanvas()
 leg = ROOT.TLegend(0.6,0.7,0.9,0.9)
 leg.SetFillColor(0)
 

 for i,gr in enumerate(all_grs):

   gr.SetMarkerStyle(20) 
   gr.SetMarkerSize(0.8)
   gr.SetLineColor(colors[i][1])
   gr.SetMarkerColor(colors[i][1])
   gr.SetFillColor(colors[i][0])

   if i==0: 
   	gr.Draw("AP")
   	gr.Draw("E2")
   	gr.Draw("P")
   else : 
   	gr.Draw("E2")
	gr.Draw("P")

   output_f.WriteTObject(gr)
   leg.AddEntry(gr,"%g <= %s < %g"%(Ybins[i],yaxis,Ybins[i+1]),"PF")

 leg.Draw()
 cv.SetName("c_%s"%output_f.GetName())
 output_f.WriteTObject(cv)


 cv = ROOT.TCanvas()
 leg = ROOT.TLegend(0.6,0.7,0.9,0.9)
 leg.SetFillColor(0)

 for i,gr in enumerate(all_grsRMS):

   gr.SetMarkerStyle(20) 
   gr.SetMarkerSize(0.8)
   gr.SetLineColor(colors[i][1])
   gr.SetMarkerColor(colors[i][1])
   gr.SetFillColor(colors[i][0])

   if i==0: 
   	gr.Draw("AP")
   	gr.Draw("E2")
   	gr.Draw("P")
   else : 
   	gr.Draw("E2")
	gr.Draw("P")

   output_f.WriteTObject(gr)
   leg.AddEntry(gr,"%g <= %s < %g"%(Ybins[i],yaxis,Ybins[i+1]),"PF")

 leg.Draw()
 cv.SetName("c_RMS_%s"%output_f.GetName())
 output_f.WriteTObject(cv)

inputf  = ROOT.TFile.Open(inputfilename)
outputf = ROOT.TFile(outputfilename,"RECREATE")

ptBins  = [0,20,40,60,10000]
vtxbins = [0,10,20,25,30,35,40,45,100]

#makeResponsePlots(inputf,outputf,"recalculated_met_T1C_hf","recomet",ptBins,"recomet",vtxbins,"nvtx") # 0 = pt, 1 = eta
makeResponsePlots(inputf,outputf,"recalculated_met_T1C_hf","recomet",vtxbins,"nvtx",ptBins,"recomet") # 0 = pt, 1 = eta

#makeResponsePlots(inputf,outputf,"recalculated_met","recomet",ptBins,"recomet",vtxbins,"nvtx") # 0 = pt, 1 = eta
makeResponsePlots(inputf,outputf,"recalculated_met","recomet",vtxbins,"nvtx",ptBins,"recomet") # 0 = pt, 1 = eta
