#!/usr/bin/env python 
import ROOT
from optparse import OptionParser
parser=OptionParser()
parser.add_option("-x","--xv",default=0,type='float')
parser.add_option("-y","--yv",default=0,type='float')
parser.add_option("","--dxstat",default=0,type='float')
parser.add_option("","--dystat",default=0,type='float')
parser.add_option("","--dxsyscorr",default=0,type='float')
parser.add_option("","--dysyscorr",default=0,type='float')
parser.add_option("","--dxsysuncorr",default=0,type='float')
parser.add_option("","--dysysuncorr",default=0,type='float')
(options,args)=parser.parse_args()

ROOT.gROOT.ProcessLine(".L ~/work-tools/stats-tools/AverageMeasurements.C")
from ROOT import AverageMeasurements
AverageMeasurements(options.xv,options.dxstat,options.dxsysuncorr,options.dxsyscorr,options.yv,options.dystat,options.dysysuncorr,options.dysyscorr)
