import sys
import array 

from optparse import OptionParser
parser=OptionParser()
parser.add_option("-g","--group",default=3,type='int')
(options,args)=parser.parse_args()
import ROOT
f = ROOT.TFile("%s.root"%args[0],"RECREATE")

#assume input is v,ru,rd
tr = ROOT.TTree("restree","restree")
cv = array.array('d',[0])
cu = array.array('d',[0])
cl = array.array('d',[0])
cnu = array.array('d',[0])
cnl = array.array('d',[0])
F = array.array('i',[0])

tr.Branch("r",cv,"r/D")
tr.Branch("r_u",cu,"r_u/D")
tr.Branch("r_d",cl,"r_d/D")
tr.Branch("r_nl",cnu,"r_nl/D")
tr.Branch("r_nu",cnl,"r_nu/D")
tr.Branch("flag",F,"flag/I")

allargs = [args[1:][i:i+options.group] for i in range(0, len(args[1:]), options.group)]

for i in allargs:
  F[0]=0

  if "," in i[0]:
    G = i[0].split(",")
    cv[0] = float(G[1])
    if int(G[0])==1: F[0] =1 
  else:
    cv[0] = float(i[0])

  if "," in i[1]:
    G = i[1].split(",")
    cu[0] = float(G[1])
    if int(G[0])==1: F[0] =1 
  else:
    cu[0] = float(i[1])

  if "," in i[2]:
    G = i[2].split(",")
    cl[0] = float(G[1])
    if int(G[0])==1: F[0] =1 
  else:
    cl[0] = float(i[2])

  if options.group == 5:
   if "," in i[3]:
    G = i[3].split(",")
    cnl[0] = float(G[1])
    if int(G[0])==1: F[0] =1 
   if "," in i[4]:
    G = i[4].split(",")
    cnu[0] = float(G[1])
    if int(G[0])==1: F[0] =1
 
  if options.group != 5: 
    cnu[0]=-999	
    cnl[0]=-999	

  tr.Fill()

tr.Write()
print "made file", f.GetName()
f.Close()
