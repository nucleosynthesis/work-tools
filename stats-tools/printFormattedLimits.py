import ROOT 
import sys 
filesin=sys.argv[1:]

ay=[]
aeyl=[]
aeyh=[]
aeyl_y=[]
aeyh_y=[]

for f in filesin: 
 fo= ROOT.TFile.Open(f)
 tr = fo.Get("limit")
 tr.GetEntry(0)
 aeyl_y.append(tr.limit)
 tr.GetEntry(1)
 aeyl.append(tr.limit)
 tr.GetEntry(2)
 ay.append(tr.limit)
 tr.GetEntry(3)
 aeyh.append(tr.limit)
 tr.GetEntry(4)
 aeyh_y.append(tr.limit)


def printme(l):
 l = [ "%.4f"%ll for ll in l] 
 return " = [ %s ]"%(",".join(l))
 
names_normal = [(f.strip("higgsCombine")).strip("AsymptoticLimits.mH120.root") for f in filesin]
print "---------------|", " ".join(names_normal)
print "Expected 2.5%  |", printme(aeyl_y)
print "Expected 16%   |", printme(aeyl)
print "Expected 50%   |", printme(ay)
print "Expected 84%   |", printme(aeyh)
print "Expected 97.5% |", printme(aeyh_y)

for i in range(len(ay)):
 print "%30s"%names_normal[i], "%.4f"%ay[i]," & [%.4f -- %.4f]"%(aeyl[i],aeyh[i]), " & [%.4f -- %.4f] \\\\ "%(aeyl_y[i],aeyh_y[i])


print "ay",printme(ay)
print "aeyl",printme(aeyl)
print "aeyh",printme(aeyh)
print "aeyl_y",printme(aeyl_y)
print "aeyh_y",printme(aeyh_y)
