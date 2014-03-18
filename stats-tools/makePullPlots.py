import ROOT
import sys
ROOT.gROOT.SetBatch(1)

nb = 21
st = 10./nb

fi = ROOT.TFile(sys.argv[1])
limit = fi.Get("limit")
limit.Draw("-1*TMath::Sqrt(2*deltaNLL)>>hleft(%d,-5.+%f,5.+%f)"%(nb,st/2,st/2),"quantileExpected<0 && r<1") #&& deltaNLL>=0 ")
hleft = ROOT.gROOT.FindObject("hleft")
limit.Draw("TMath::Sqrt(2*deltaNLL)>>hright(%d,-5.+%f,5.+%f)"%(nb,st/2,st/2),"quantileExpected<0   && r>=1") #&& deltaNLL>=0 " )
hright = ROOT.gROOT.FindObject("hright")

print hleft.GetBinLowEdge(hleft.FindBin(0))
print hleft.GetBinLowEdge(hleft.FindBin(0)+1)
#limit.Draw("-1*TMath::Sqrt(2*deltaNLL)>>hleft(25,-5+-.2,5+0.2)","quantileExpected<0 && r<1 && TMath::Abs(r-1)>0.01 && deltaNLL>=0 ")
#hleft = ROOT.gROOT.FindObject("hleft")
#limit.Draw("TMath::Sqrt(2*deltaNLL)>>hright(25,-5+0.2,5+0.2)","quantileExpected<0   && r>=1 && TMath::Abs(r-1)>0.01 && deltaNLL>=0 " )
#hright = ROOT.gROOT.FindObject("hright")

#limit.Draw("0*deltaNLL>>h0(%d,-5+%f,5+%f)"%(nb,st/2,st/2),"quantileExpected<0 && deltaNLL<0")
#h0 = ROOT.gROOT.FindObject("h0")

hleft.Add(hright)
#hleft.Add(h0)
hleft.GetXaxis().SetTitle("(#hat{#mu}-1)/#sigma_{#mu}")

hleft.SetTitle("h_pull")
hleft.SetName("h_pull")

fout = ROOT.TFile("%s"%sys.argv[2],"RECREATE")
fout.cd()
hleft.Write()
