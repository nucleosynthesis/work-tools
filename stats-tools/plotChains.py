import ROOT

rmin = 0 
rmax = 30 
nbins = 100
CL = 0.95
chains = "higgsCombineTest.MarkovChainMC.blahblahblah.root"


def findSmallestInterval(hist,CL): 

 bins = hist.GetNbinsX()

 best_i = 1
 best_j = 1
 bd = bins+1
 val = 0;

 for i in range(1,bins+1): 
   integral = hist.GetBinContent(i)
   for j in range(i+1,bins+2):
    integral += hist.GetBinContent(j)
    if integral > CL :
      val = integral
      break  
 
   if integral > CL and  j-i < bd : 
     bd = j-i 
     best_j = j+1 
     best_i = i
     val = integral


 return hist.GetBinLowEdge(best_i), hist.GetBinLowEdge(best_j), val


fi_MCMC = ROOT.TFile.Open(chains)

# Sum up all of the chains / or could take the average limit
mychain=0
for k in fi_MCMC.Get("toys").GetListOfKeys():
    obj = k.ReadObj
    if mychain ==0: 
        mychain = k.ReadObj().GetAsDataSet()
    else :
        mychain.append(k.ReadObj().GetAsDataSet())

# Easier to fill a histogram why not ?
hist = ROOT.TH1F("h_post",";r;posterior probability",nbins,rmin,rmax)
for i in range(mychain.numEntries()): 
  mychain.get(i)
  hist.Fill(mychain.get(i).getRealValue("r"), mychain.weight())

hist.Scale(1./hist.Integral())

c6a = ROOT.TCanvas()
hist.Draw()
vl,vu,trueCL = findSmallestInterval(hist,CL)

ll = ROOT.TLine(vl,0,vl,0.15); ll.SetLineColor(2)
lu = ROOT.TLine(vu,0,vu,0.15); lu.SetLineColor(2)
ll.Draw()
lu.Draw()

print " %g %% (%g %%) interval (target)  = %g < r < %g "%(trueCL,CL,vl,vu)
raw_input()
