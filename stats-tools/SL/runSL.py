import sys
import array

from optparse import OptionParser
parser=OptionParser()
parser.add_option("-o","--outname",default="SL",help="Output name extension")
parser.add_option("-v","--verbose",default=False,action='store_true',help="Turn on verbosity")
parser.add_option("","--model",default="mymodel",help="Choose python model (which defines SL inputs) to run over for SL")
parser.add_option("","--limit",default=False,action='store_true',help="Calculate Limit instead of the scan")
parser.add_option("","--doMultiplicative",default=False,action='store_true',help="Multiplicative rather than additive parameterisation")
parser.add_option("","--ignoreCorrelation",default=False,action='store_true',help="Ignore the off-diagonal covariance terms")
parser.add_option("","--includeQuadratic",default=False,action='store_true',help="run quadratic version of SL")
parser.add_option("","--rMin",default=-0.5,type='float')
parser.add_option("","--rMax",default=2.0,type='float')
parser.add_option("","--npoints",default=30,type='int',help="Number of points for likelihood scanning")
(options,args)=parser.parse_args()

import ROOT
"""
if options.includeQuadratic:
  ROOT.gROOT.ProcessLine(".L simplifiedLikelihoodQuadratic.C")
  from ROOT import simplifiedLikelihoodQuadratic

else:
  ROOT.gROOT.ProcessLine(".L simplifiedLikelihoodLinear.C")
  from ROOT import simplifiedLikelihoodLinear
"""
ROOT.gROOT.ProcessLine(".L simplifiedLikelihoodLinear.C")
from ROOT import simplifiedLikelihoodLinear

if not options.verbose:
  ROOT.RooMsgService.instance().setSilentMode(True)
  ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.ERROR)

# Default ROOT minimizer options
#ROOT.Math.MinimizerOptions.SetDefaultStrategy(2);

ROOT.RMIN=options.rMin
ROOT.RMAX=options.rMax

ROOT.gMultiplicative=options.doMultiplicative
ROOT.ignoreCorrelation=options.ignoreCorrelation
ROOT.justCalcLimit=options.limit
ROOT.verb=options.verbose
ROOT.globalNpoints=options.npoints
ROOT.includeQuadratic=options.includeQuadratic
ROOT.outname=options.outname

# HERE we build up the elements for the SL from a python file
model = __import__(options.model)

# CHECK we don't go over the max 
if model.nbins > ROOT.MAXBINS: sys.exit("Too many bins (nbins > %d), you should modify MAXBINS in .C code"%ROOT.MAXBINS)

print "Simplified Likelihood for model file --> ",  
try : print model.name
except : print " no named model file"

ROOT.globalNbins      = model.nbins

for i in range(model.nbins):
  ROOT.globalData[i]       = model.data[i]
  ROOT.globalBackground[i] = model.background[i]
  ROOT.globalSignal[i]     = model.signal[i]
  if options.includeQuadratic : ROOT.globalThirdMoments[i]     = model.third_moment[i]

for j in range(model.nbins*model.nbins):
  ROOT.globalCovariance[j] = model.covariance[j]

#if options.includeQuadratic: simplifiedLikelihoodQuadratic()
#else: simplifiedLikelihoodLinear()
simplifiedLikelihoodLinear()
