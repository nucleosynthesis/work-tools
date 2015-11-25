#!/usr/bin/env python 
# wrapper for fit checker
from optparse import OptionParser
parser=OptionParser()
parser.add_option("-i","--infile",type='str',default="nada")
parser.add_option("-o","--output",type='str',default="min")
parser.add_option("-e","--expected",default=False,action='store_true')
(options,args)=parser.parse_args()

import ROOT as r

r.gROOT.ProcessLine(".L ~/scratch0/tools/stats-tools/checkBestFitPoint.C")
#r.gROOT.ProcessLine(".L ~/scratch0/tools/stats-tools/load.C+")
from ROOT import checkBestFitPoint
checkBestFitPoint(options.infile,options.output,0)
