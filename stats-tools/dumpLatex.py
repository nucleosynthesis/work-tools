#!/usr/bin/env python
import re
import os.path
from math import *
from optparse import OptionParser

parser = OptionParser()
(options, args) = parser.parse_args()
options.stat = False
options.bin = True # fake that is a binary output, so that we parse shape lines
options.out = "tmp.root"
options.fileName = args[0]
options.cexpr = False
options.fixpars = False
options.libs = []
options.verbose = 0
options.poisson = 0
options.nuisancesToExclude = []
options.noJMax = True
options.allowNoSignal = True
# import ROOT with a fix to get batch mode (http://root.cern.ch/phpBB3/viewtopic.php?t=3198)
import sys
sys.argv = [ '-b-']
import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gSystem.Load("libHiggsAnalysisCombinedLimit")

from HiggsAnalysis.CombinedLimit.DatacardParser import *
from HiggsAnalysis.CombinedLimit.ShapeTools     import *

if options.fileName.endswith(".gz"):
    import gzip
    file = gzip.open(options.fileName, "rb")
    options.fileName = options.fileName[:-3]
else:
    file = open(options.fileName, "r")

DC = parseCard(file, options)
if not DC.hasShapes: DC.hasShapes = True

errlines = {}
allProcMap = {}
for (lsyst,nofloat,pdf,pdfargs,errline) in DC.systs:
    if pdf != "lnN": continue
    if not len(errline) : continue
    types = []
    processes = {}
    channels  = []
    errlines[lsyst] = errline
    for b in DC.bins:
    	types.append(pdf)
        channels.append(b)
        for p in DC.exp[b].iterkeys():
	    processes[p] = False
            if errline[b][p] == 0: continue
            processes[p] = True
            vals = errline[b][p] if type(errline[b][p]) == list else [ errline[b][p] ]
        allProcMap[b]=DC.exp[b].keys()

print "\\documentclass{article}"
print "\\usepackage{rotating}"
print "\\begin{document}"

for b in DC.bins:
 print  
 print "\\begin{table}[hbt]"
 print "\\begin{center}"
 print "\\caption{Systematic effects - \\texttt{%s}}"%b.replace("_","\\_")
 print "\\tiny"
 print "\\begin{tabular}{l",
 for p in allProcMap[b]: print "|c", 
 print "}"
 for p in allProcMap[b]: 
   #if allProcMap[b][p]: 
     print " & %s"%p,
 print "\\\\"
 print "\\hline"

 for e in errlines.keys():
  print "\\texttt{%s}"%e.replace("_","\\_"),
  for p in allProcMap[b]:
   val = errlines[e][b][p]
   if type(val)== list : 
   	print " & %g/%g "%(val[0],val[1]),
   else: 
      if val!=0:
   	print " & %g "%(val),
      else :print " & - ",
  print "\\\\"
 print "\\hline"
 print "\\end{tabular}"
 print "\\end{center}"
 print "\\end{table}"
print "\\end{document}"
