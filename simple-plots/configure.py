# Configuration file for plotting
# L is the Luminosity in fb, signalScale is a factor for the signal to be scaled to - thats it 
import ROOT 
import math 

treeName    = "events"

L           = 10 # = 100/fb
signalScale = 200

samples = { 
	"VV":[ ["vv.root"], [98.5356], ROOT.kGreen+1 ]
	,"tt":[ ["tt.root"], [504.338], ROOT.kPink+2 ]
	,"W+jets":[ ["wj_lv.root"], [24.50967], ROOT.kOrange+2 ]
	,"Z+jets":[ ["zj_vv.root"], [28.2833], ROOT.kAzure+6 ]
#	,"Z+b/Z(bb)":[ ["zj_b.root"], [6522.7694364], ROOT.kAzure-2 ]
	  }

order = ["VV","tt","W+jets","Z+jets"]

signals = {
	"V(jj)H#rightarrow inv.":[ ["vhinv.root"],[0.0274167],ROOT.kRed]
	,"Z(bb)H#rightarrow inv.":[ ["zhinv.root"],[0.020429],ROOT.kCyan]
	}

variables = { 
	   "met":["p_{T}^{miss} (GeV)",30,200,1000,True,0,[],[]] 
	  ,"mjj":["m_{jj} (GeV)",30,0,800,False,0,[],[]] 
	  ,"ptjj":["p_{T}^{jj} (GeV)",30,0,1000,False,0,[],[]] 
	  ,"drjj":["#Delta R(jj) ",20,0,4.5,False,0,[],[]] 
	  ,"jet_bT":["b-tag (all jets)",20,-1,1,False,0,[],[]] 
	  ,"njets":["njets",8,0,8,False,0,[],[]] 
	  ,"nbtag":["nbtag",6,0,6,True,0,[],[]] 
	  ,"njetsall":["njets",10,0,10,False,0,[],[]] 
	  ,"dphijm":["#Delta#phi(jj,p_{T}^{miss})",15,0,5,True,0,[],[]] 
	  }

# here define a simple analysis (selection of cuts or whatever)

def doAnalysis(tr,entry,i,w):
     
     variables["njets"][entry][i].Fill(tr.njets,w)
     variables["njetsall"][entry][i].Fill(tr.njetsall,w)
     nbt = 0 
     variables["jet_bT"][entry][i].Fill(tr.jet1_bT,w)
     variables["jet_bT"][entry][i].Fill(tr.jet2_bT,w)
     variables["jet_bT"][entry][i].Fill(tr.jet3_bT,w)
     variables["jet_bT"][entry][i].Fill(tr.jet4_bT,w)
     
     nbtags = 0.001+max([tr.jet1_bT,0]) +max([tr.jet2_bT,0]) +max([tr.jet3_bT,0]) +max([tr.jet4_bT,0])
     variables["nbtag"][entry][i].Fill(nbtags,w)

     variables["met"][entry][i].Fill(float(tr.missing_momentum),w)

     # turn the first two jets into lorentz vectors 
     j1 = ROOT.TLorentzVector(tr.jet1_px,tr.jet1_py,tr.jet1_pz,tr.jet1_E)
     j2 = ROOT.TLorentzVector(tr.jet2_px,tr.jet2_py,tr.jet2_pz,tr.jet2_E)

     jj = j1+j2
     
     dR = j1.DeltaR(j2)
     
     jjt  = ROOT.TVector3(jj.Px(),jj.Py(),0)
     mett = ROOT.TVector3(tr.missing_momentum*math.cos(tr.missing_momentum_phi),tr.missing_momentum*math.sin(tr.missing_momentum_phi),0)
     
     dphi = abs(jjt.DeltaPhi(mett))
     variables["dphijm"][entry][i].Fill(dphi,w)
   
     variables["mjj"][entry][i].Fill(jj.M(),w)
     variables["drjj"][entry][i].Fill(dR,w)
     variables["ptjj"][entry][i].Fill(jj.Pt(),w)

