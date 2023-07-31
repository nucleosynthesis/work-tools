#!/usr/bin/env python 

import matplotlib.pyplot as plt

import sys

from optparse import OptionParser
parser=OptionParser()
parser.add_option("-p","--points",action="store_true",help="add markers to curve")
parser.add_option("-x","--xvar",default="r",type='str',help="x variable in tree")
(options,args)=parser.parse_args()

import ROOT

files = args[:]

def getpoints(fn):
  fi = ROOT.TFile.Open(fn)
  tr = fi.Get("limit")
  ret = []
  for i in range(tr.GetEntries()):
    tr.GetEntry(i)
    x = getattr(tr,options.xvar)
    y = 2*tr.deltaNLL
    ret.append([x,y])
  ret.sort()
  return ret

for fi in files:
  print("Adding scan for file - %s"%fi)
  points = getpoints(fi)
  np = len(points)
  if options.points: plt.plot([points[i][0] for i in range(np)],[points[i][1] for i in range(np)],label=fi,marker='o')
  else: plt.plot([points[i][0] for i in range(np)],[points[i][1] for i in range(np)],label=fi)
  
plt.legend()
plt.xlabel(options.xvar)
plt.ylabel("$-2\Delta\ln L($%s$)$"%options.xvar)
plt.savefig("scans.pdf")
#plt.show()
