# run with ...
# python makeCombinedPlot.py contourfiles


import sys
import ROOT as r
r.gROOT.SetBatch(1)
r.gROOT.ProcessLine(".L /afs/cern.ch/work/n/nckw/private/stats-tools/tdrstyle.cc")
from ROOT import tdrstyle

tdrstyle()
r.gStyle.SetOptStat(0)
r.gStyle.SetTextFont(42);

contours = [0.68]#]0.95]

# Main Routine
args=sys.argv[1:]

xaxis = ["#mu_{ggH+ttH}"	,0,3]
yaxis = ["#mu_{VH+qqH}"		,0,6]

channels = {
	     0:["H #rightarrow #tau#tau",	r.kMagenta+2,	[],3]
	    ,1:["H #rightarrow WW",		r.kBlue,	[],3]
	    ,2:["H #rightarrow ZZ",		r.kRed,		[],3]
	    ,3:["H #rightarrow bb",		r.kCyan,	[],3]
	    ,4:["H #rightarrow #gamma#gamma",	r.kGreen+2,	[],4]
	   }

print "Plotting rVrF FC plots. "
print "Assuming input order is ",
for ch in range(len(channels.keys())):
	print channels[ch][0]+", ",
print "\n"

# Make the SM point
smgraph = r.TGraph()
smgraph.SetPoint(0,1,1)
smgraph.SetMarkerStyle(33)
smgraph.SetMarkerColor(5)
smgraph.SetLineColor(2)
smgraph.SetMarkerSize(2.5)
smgraph2 = smgraph.Clone()
smgraph2.SetMarkerStyle(27)
smgraph2.SetMarkerColor(2)
smgraph2.SetLineWidth(3)


tleg = r.TLegend(0.60,0.65,0.92,0.92)
tleg.SetTextSize(0.04)
tleg.SetFillColor(10)

for ch,obj in enumerate(channels):

	# Get the file 
	fChannel = r.TFile.Open(args[ch])
	fHisto   = fChannel.Get("h2_cl")
	nHisto   = fChannel.Get("n_toys")
	for bx in range(fHisto.GetNbinsX()):
	  for by in range(fHisto.GetNbinsY()):
		if nHisto.GetBinContent(bx+1,by+1)<=1: fHisto.SetBinContent(bx+1,by+1,0.99999)
	for ns in range(channels[ch][3]):	fHisto.Smooth()

	# Copy for the contours
	for cl_i,cl in enumerate(contours):
		cHisto = fHisto.Clone();
		cHisto.SetLineWidth(3)
		cHisto.SetLineColor(channels[ch][1])
		cHisto.SetLineStyle(cl_i+1)
		cHisto.SetContour(2)
		cHisto.SetContourLevel(1,cl)
		channels[ch][2].append(cHisto.Clone())
	
	tleg.AddEntry(channels[ch][2][0],channels[ch][0],"L")

	#fChannel.Close()

# Now plot all of the lines 
#canvas = r.TCanvas("c","",800,800);
canvas = r.TCanvas();
# dummy histogram for axis
dummy = r.TH2F("dum","",10,xaxis[1],xaxis[2],10,yaxis[1],yaxis[2])
dummy.GetXaxis().SetTitle(xaxis[0])
dummy.GetYaxis().SetTitle(yaxis[0])
dummy.Draw()

for ch,obj in enumerate(channels):
	for cl_i,obj in enumerate(contours): 
		print "Plotting channel " ,ch, ", contour ", obj 
		channels[ch][2][cl_i].Draw("sameCONT3");
# SM point
smgraph.Draw("P")
smgraph2.Draw("P")
	
tleg.Draw()

tLatex = r.TLatex()
tLatex.SetNDC()
tLatex.SetTextSize(0.03)
tLatex.SetTextFont(42)
tLatex.DrawLatex(0.17,0.96,"CMS Preliminary  #sqrt{s} = 7TeV L #leq 5.1 fb^{-1}, #sqrt{s} = 8TeV  L #leq 19.6 fb^{-1}")
canvas.SaveAs("rVrF-fc.pdf")
canvas.SaveAs("rVrF-fc.png")
canvas.SaveAs("rVrF-fc.eps")

