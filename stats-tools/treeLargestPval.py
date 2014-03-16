# Quick script which turns the p-values from all the toys into the largest p-value per toy
import ROOT
import sys

files = sys.argv[1:]

pval_data_125 = 0.000921931

# Assume all pvalues are in 1 file, each entry contains a pvalue for each mass 
# Handy function
ROOT.gROOT.ProcessLine( \
   "struct Entry{ \
    double r;   \
    double mh;    \
    int iToy;    \
   };"
)
from ROOT import Entry

def getENTRY(tree,entry=0):
  br = tree.GetBranch("limit")
  m = tree.GetBranch("mh")
  t = tree.GetBranch("iToy")
  c = Entry()
  br.SetAddress(ROOT.AddressOf(c,'r'))
  m.SetAddress(ROOT.AddressOf(c,'mh'))
  t.SetAddress(ROOT.AddressOf(c,'iToy'))
  tree.GetEntry(entry)  
  return c.r,c.mh,c.iToy

def fillSmallestP(f,collection):

 file = ROOT.TFile(f)
 tree = file.Get("limit")
 nevt=0
 try : nevt = tree.GetEntries()
 except AttributeError: "no tree!"

 toy_map = {}

 for i in range(nevt):
  
  # For each entry in the tree, need to get the toy, mass and pval
  p,mh,it = getENTRY(tree,i)
  try: 
      toy_map[it]
      toy_map[it].append(p)
  except KeyError : toy_map[it] = [p]

 for j,k in enumerate(toy_map.keys()):
  # Find the largest pvalue
  print len(toy_map[k]) 
  pv = min(toy_map[k])
  collection.append(pv)


alltoys = []
for f in files:
  fillSmallestP(f,alltoys)

print "done collecting pvals, making plot"

def countExcess(thresh):
  count = 0
  for t in alltoys:
    if t<thresh: count+=1
  tot = len(alltoys)
  count=float(count)
  eff = float(count)/tot
  return eff,(1./tot)*((count*(1.-count/tot))**0.5)

print "Ntoys -> ",  len(alltoys)
gra = ROOT.TGraphErrors()
gra1 = ROOT.TGraphErrors()
graD = ROOT.TGraph()
# dump into a Graph 
for l,pval in enumerate(range(1000)):
  x = 10**(-1*float(pval)/100)
  gpv = countExcess(x)
  gra.SetPoint(l,x,gpv[0])
  gra1.SetPoint(l,x,gpv[0])
  #print x,gpv[0],gpv[1]
  gra.SetPointError(l,0,gpv[1])
  gra1.SetPointError(l,0,0)

graD.SetPoint(0,0,pval_data_125)

outfile = ROOT.TFile("smallesttoys.root","RECREATE")
outfile.cd()
gra.SetName("pval")
gra.Write()
gra1.SetName("pval_cent")
gra1.Write()
graD.SetName("pval_data")
graD.Write()
outfile.Close()
