import sys
import array
import simplified_likelihood as SL

from optparse import OptionParser
parser=OptionParser()
parser.add_option("-o","--outname",default="SL",help="Output name extension")
parser.add_option("-v","--verbose",default=False,action='store_true',help="Turn on verbosity")
parser.add_option("","--model",default="mymodel",help="Choose python model (which defines SL inputs) to run over for SL")
#parser.add_option("","--limit",default=False,action='store_true',help="Calculate Limit instead of the scan")
#parser.add_option("","--doMultiplicative",default=False,action='store_true',help="Multiplicative rather than additive parameterisation")
#parser.add_option("","--ignoreCorrelation",default=False,action='store_true',help="Ignore the off-diagonal covariance terms")
#parser.add_option("","--includeQuadratic",default=False,action='store_true',help="run quadratic version of SL") <-- not yet working
parser.add_option("","--rMin",default=-0.5,type='float')
parser.add_option("","--rMax",default=2.0,type='float')
parser.add_option("","--npoints",default=30,type='int',help="Number of points for likelihood scanning")
(options,args)=parser.parse_args()

# HERE we build up the elements for the SL from a python file
model = __import__(options.model)

print "Simplified Likelihood for model file --> ",  
try : print model.name
except : print " no named model file"

SL.simplified_likelihood_linear(model,options)
