# Configuration file for plotting
# L is the Luminosity in fb, signalScale is a factor for the signal to be scaled to - thats it 
import ROOT 
import math 

# These will get set by the plotting script to highlight what is being currently processed
fName   = ""
fSample = ""
fLabel  = ""
###########################################################################################
treeName    = ""
L           = 10     # Luminosity in same units as XSec of samples
signalScale = 200    # Signal histograms (not sum of weights) will be scaled
minWeight   = -9999. # Any event with weight less than this is not filled 

#samples (and signals) should be 
#	"Label":[ ["file1.root","file2.root",...], [XSec1,XSec2,..],color]

samples = { 
	  "Diboson":[ ["vv.root"], [98.5356], ROOT.kGreen+1 ]
	  }

signals = {
	"V(jj)H#rightarrow inv.":[ ["vhinv.root"],[0.0274167],ROOT.kRed]
	}

# preferred order, if empty, will use keys in samples dict (random order)
order = ["VV","tt","W+jets","Z+jets"]

# Variables are defined 
#	"name":["x-label",nbins,xmin,xmax,log_scale,0,[],[]]  - leave 0, and lists blank
variables = { 
	   "met":["p_{T}^{miss} (GeV)",30,200,1000,True,0,[],[]] 
	  }

# Here define a simple analysis (selection of cuts or whatever)
# Needs only to return an event weight, 
# if weight < minWeight , won't be counted in sum of weights at summary 

def doAnalysis(tr,entry,i,w):

     variables["met"][entry][i].Fill(float(tr.missing_momentum),w)
     return w
