import ROOT as r 
import csv 
import sys 
import array 

r.gROOT.ProcessLine(".L Delphes/libDelphes.so")
from ROOT import MissingET
from ROOT import Jet

fi_in  = r.TFile.Open(sys.argv[1])
fi_out = r.TFile(sys.argv[2],"RECREATE")
tree_out = r.TTree("events","events")

#fi_out_csv = open("%s.csv"%sys.argv[2],"w")

treename = "Delphes"


def leptonCleaning(lepton, jets):

   for jet in jets:
     dr = abs(lepton.DeltaR(jet))
     if dr < 0.4 : return False

   return True 
  

output_variables = {
	 "missing_momentum":array.array("d",[-999.])
	,"missing_momentum_phi":array.array("d",[-999.])
	,"jet1_px":array.array("d",[-999.])
	,"jet1_py":array.array("d",[-999.])
	,"jet1_pz":array.array("d",[-999.])
	,"jet1_E":array.array("d",[-999.])
	,"jet1_bT":array.array("d",[-999.])
	,"jet2_px":array.array("d",[-999.])
	,"jet2_py":array.array("d",[-999.])
	,"jet2_pz":array.array("d",[-999.])
	,"jet2_E":array.array("d",[-999.])
	,"jet2_bT":array.array("d",[-999.])
	,"jet3_px":array.array("d",[-999.])
	,"jet3_py":array.array("d",[-999.])
	,"jet3_pz":array.array("d",[-999.])
	,"jet3_E":array.array("d",[-999.])
	,"jet3_bT":array.array("d",[-999.])
	,"jet4_px":array.array("d",[-999.])
	,"jet4_py":array.array("d",[-999.])
	,"jet4_pz":array.array("d",[-999.])
	,"jet4_E":array.array("d",[-999.])
	,"jet4_bT":array.array("d",[-999.])
	,"muon1_px":array.array("d",[-999.])
	,"muon1_py":array.array("d",[-999.])
	,"muon1_pz":array.array("d",[-999.])
	,"muon1_E":array.array("d",[-999.])
	,"muon2_px":array.array("d",[-999.])
	,"muon2_py":array.array("d",[-999.])
	,"muon2_pz":array.array("d",[-999.])
	,"muon2_E":array.array("d",[-999.])
	,"electron1_px":array.array("d",[-999.])
	,"electron1_py":array.array("d",[-999.])
	,"electron1_pz":array.array("d",[-999.])
	,"electron1_E":array.array("d",[-999.])
	,"electron2_px":array.array("d",[-999.])
	,"electron2_py":array.array("d",[-999.])
	,"electron2_pz":array.array("d",[-999.])
	,"electron2_E":array.array("d",[-999.])
	,"njets":array.array("d",[-999.])
	,"njetsall":array.array("d",[-999.])
	,"nmuons":array.array("d",[-999.])
	,"nelectrons":array.array("d",[-999.])
}

for k in output_variables.keys() : tree_out.Branch(k,output_variables[k],"%s/D"%k) 

#writer = csv.writer(fi_out_csv,delimiter = ",")
#writer.writerow(output_variables.keys())

tree = fi_in.Get(treename)
evnts = tree.GetEntries()

for i in range(evnts):

 # Best to reset our variables :
 for k in output_variables.keys() : output_variables[k][0]=-999.

 tree.GetEntry(i)

 output_variables["missing_momentum"][0] = getattr(tree.MissingET[0],"MET")
 output_variables["missing_momentum_phi"][0] = tree.MissingET[0].Phi

 local_nj = 0
 local_nm = 0
 local_ne = 0

 alljets = []

 for j in range(tree.Jet_size):

   if j>3 : break 
   local_nj+=1

   vjetid = "jet%d_"%(j+1)

   tlvec = r.TLorentzVector()
   tlvec.SetPtEtaPhiM(tree.Jet[j].PT,tree.Jet[j].Eta,tree.Jet[j].Phi,tree.Jet[j].Mass)

   alljets.append(tlvec)

   output_variables[vjetid+"px"][0]  = tlvec.Px()
   output_variables[vjetid+"py"][0]  = tlvec.Py()
   output_variables[vjetid+"pz"][0]  = tlvec.Pz()
   output_variables[vjetid+"E"][0]   = tlvec.E()
   output_variables[vjetid+"bT"][0]  = tree.Jet[j].BTag

 output_variables["njets"][0]  =  local_nj
 output_variables["njetsall"][0]  =  tree.Jet_size
 
 for j in range(tree.Muon_size):

   if j>1 : break 
   vjetid = "muon%d_"%(j+1)

   tlvec = r.TLorentzVector()
   tlvec.SetPtEtaPhiM(tree.Muon[j].PT,tree.Muon[j].Eta,tree.Muon[j].Phi,0)

   if not leptonCleaning(tlvec,alljets): continue
   local_nm+=1

   output_variables[vjetid+"px"][0] = tlvec.Px()
   output_variables[vjetid+"py"][0]  = tlvec.Py()
   output_variables[vjetid+"pz"][0]  = tlvec.Pz()
   output_variables[vjetid+"E"][0]  = tlvec.E()

 output_variables["nmuons"][0] = local_nm
 
 for j in range(tree.Electron_size):

   if j>1 : break 
   vjetid = "electron%d_"%(j+1)

   tlvec = r.TLorentzVector()
   tlvec.SetPtEtaPhiM(tree.Electron[j].PT,tree.Electron[j].Eta,tree.Electron[j].Phi,0)

   if not leptonCleaning(tlvec,alljets): continue
   local_ne+=1

   output_variables[vjetid+"px"][0] = tlvec.Px()
   output_variables[vjetid+"py"][0]  = tlvec.Py()
   output_variables[vjetid+"pz"][0]  = tlvec.Pz()
   output_variables[vjetid+"E"][0]  = tlvec.E()

 output_variables["nelectrons"][0] = local_ne

 tree_out.Fill()
 #writer.writerow([ str(output_variables[k][0]) for k in output_variables.keys()] ) 

fi_out.WriteTObject(tree_out)
fi_out.Close()
