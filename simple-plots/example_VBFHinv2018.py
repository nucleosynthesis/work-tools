# Configuration file for plotting
# L is the Luminosity in fb, signalScale is a factor for the signal to be scaled to - thats it 
import ROOT 
import math 
import csv
import array
import sys 
import copy 

treeName    = "Events"

L           = 59740.56520/5      # = 1/fb?
signalScale = 0.19
minWeight   = -9999999
odir 	    = "plots_2018"


directory = "Data/"
pre_mc    = "Nominal/" 

samples = { 
	"Z(#nu#nu)+jets (Strong)":[ [pre_mc+"zjets.root"], [1], ROOT.kAzure-9 ]
	,"Z(#nu#nu)+jets (VBF)"	:[ [pre_mc+"ewkznunu.root"], [1], ROOT.kRed+7 ]
	,"W(l#nu)+jets (Strong)":[ [pre_mc+"wjets.root"], [1], ROOT.kAzure ]
	,"W(l#nu)+jets (VBF)"	:[ [pre_mc+"ewkw.root"], [1], ROOT.kAzure+10 ]
	,"Dibosons"		:[ [pre_mc+"vv.root"], [1], ROOT.kGray+1 ]
	,"Top"			:[ [pre_mc+"topincl.root"], [1], ROOT.kOrange ]
	,"Z(ll)+jets"		:[ [pre_mc+"dy.root",pre_mc+"ewkzll.root"], [1,1], ROOT.kGreen+2 ]
	,"QCD"			:[ [pre_mc+"qcd.root"], [1], ROOT.kOrange+6 ]
	  }

#order = ["Top"]
order = ["Z(#nu#nu)+jets (Strong)","W(l#nu)+jets (Strong)","Z(#nu#nu)+jets (VBF)","W(l#nu)+jets (VBF)","Dibosons","Top","Z(ll)+jets","QCD"]
order.reverse()

signals = {
	"qqH, H#rightarrow inv" :[ [pre_mc+"/VBF125/Skim_VBF125.root"],[1],ROOT.kRed+1]
	,"ggH, H#rightarrow inv":[ [pre_mc+"/ggF125/Skim_ggF125.root"],[1],ROOT.kMagenta]
	}

data = { "data" : [ [directory+"/MET.root"],[1],ROOT.kBlack ] }
       

variables = { 
	   "MET_phi"      :["#phi(E_{T}^{miss})",50,-4,4,True,0,[],[],[]] 
,	   "dijet_pT"      :["p_{T}^{jj}",60,0,3000,True,0,[],[],[]] 
,	   "dijet_phi"      :["#phi(p_{T}^{jj} vec)",50,-4,4,True,0,[],[],[]] 
,	   "dijet_pT_reldiff_MET"      :["(p_{T}^{jj}-E_{T}^{miss})/E_{T}^{miss}",50,-3,3,True,0,[],[],[]] 
,	   "dijet_pT_reldiff_MET_METWindow"      :["(p_{T}^{jj}-E_{T}^{miss})/E_{T}^{miss}, -1.6 < #phi(MET)",50,-3,3,True,0,[],[],[]] 
,	   "MET_phi_VetoRelDiff0p4"      :["#phi(E_{T}^{miss}), (p_{T}^{jj}-E_{T}^{miss})/E_{T}^{miss}) < 0.4)  ",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoRelDiff0p4"          :["E_{T}^{miss} (GeV), (p_{T}^{jj}-E_{T}^{miss})/E_{T}^{miss}) < 0.4) ",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoRelDiff0p4_METWindow"      :["#phi(E_{T}^{miss}), (p_{T}^{jj}-E_{T}^{miss})/E_{T}^{miss}) < 0.4)  if -1.6 < #phi(MET) < -0.8",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoRelDiff0p4_METWindow"          :["E_{T}^{miss} (GeV), (p_{T}^{jj}-E_{T}^{miss})/E_{T}^{miss}) < 0.4)  if -1.6 < #phi(MET) < -0.8",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoSoftJetOrIsoTrackInHEM"      :["#phi(E_{T}^{miss}), ! #geq 1 soft JET or Iso Track in HEM ",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoSoftJetOrIsoTrackInHEM"          :["E_{T}^{miss} (GeV), ! #geq 1 soft JET or Iso Track in HEM",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoSoftJetOrIsoTrackInHEM_METWindow"      :["#phi(E_{T}^{miss}), 0, #geq 1 soft JET or Iso Track in HEM if -1.6 < #phi(MET) < -0.8",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoSoftJetOrIsoTrackInHEM_METWindow"          :["E_{T}^{miss} (GeV), 0, #geq 1 soft JET or Iso Track in HEM if -1.6 < #phi(MET) < -0.8",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoSoftJetInHEM"      :["#phi(E_{T}^{miss}), ! #geq 1 soft JET in HEM ",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoSoftJetInHEM"          :["E_{T}^{miss} (GeV), ! #geq 1 soft JET in HEM",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoSoftJetInHEM_METWindow"      :["#phi(E_{T}^{miss}), 0, #geq 1 soft JET in HEM if -1.6 < #phi(MET) < -0.8",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoSoftJetInHEM_METWindow"          :["E_{T}^{miss} (GeV), 0, #geq 1 soft JET in HEM if -1.6 < #phi(MET) < -0.8",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoSoftJetInHEM_noIso_METWindow"      :["#phi(E_{T}^{miss}), 0, #geq 1 soft JET in HEM, no IsoTrack overlap, if -1.6 < #phi(MET) < -0.8",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoSoftJetInHEM_noIso_METWindow"          :["E_{T}^{miss} (GeV), 0, #geq 1 soft JET in HEM, no IsoTrack overlap,  if -1.6 < #phi(MET) < -0.8",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoIsoTrackInHEM"      :["#phi(E_{T}^{miss}), ! #geq 1 Iso Track in HEM ",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoIsoTrackInHEM"          :["E_{T}^{miss} (GeV), ! #geq 1 Iso Track in HEM",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoIsoTrackInHEM_METWindow"      :["#phi(E_{T}^{miss}), 0, #geq 1 Iso Track in HEM if -1.6 < #phi(MET) < -0.8",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoIsoTrackInHEM_METWindow"          :["E_{T}^{miss} (GeV), 0, #geq 1 Iso Track in HEM if -1.6 < #phi(MET) < -0.8",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoFailedJetInHEM"      :["#phi(E_{T}^{miss}), ! #geq 1 Failed PU JET in HEM ",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoFailedJetInHEM"          :["E_{T}^{miss} (GeV), ! #geq 1 Failed PU JET in HEM",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoFailedJetInHEM_METWindow"      :["#phi(E_{T}^{miss}), 0, #geq 1 Failed PU JET in HEM if -1.6 < #phi(MET) < -0.8",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoFailedJetInHEM_METWindow"          :["E_{T}^{miss} (GeV), 0, #geq 1 Failed PU JET in HEM if -1.6 < #phi(MET) < -0.8",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_SoftJETHEM30"      :["#phi(E_{T}^{miss}), soft JET in HEM sum pT>30",50,-4,4,True,0,[],[],[]] 
,	   "Met_SoftJETHEM30"          :["E_{T}^{miss} (GeV), soft JET in HEM sum pT>30",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoSoftJETHEM30"      :["#phi(E_{T}^{miss}), veto soft JET in HEM sum pT>30",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoSoftJETHEM30"          :["E_{T}^{miss} (GeV), veto soft JET in HEM sum pT>30",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_SoftJETHEM5"      :["#phi(E_{T}^{miss}), soft JET in HEM sum pT>5",50,-4,4,True,0,[],[],[]] 
,	   "Met_SoftJETHEM5"          :["E_{T}^{miss} (GeV), soft JET in HEM sum pT>5",50,0,500,True,0,[],[],[]] 
,	   "MET_phi_VetoSoftJETHEM5"      :["#phi(E_{T}^{miss}), veto soft JET in HEM sum pT>5",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoSoftJETHEM5"          :["E_{T}^{miss} (GeV), veto soft JET in HEM sum pT>5",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_HEMJET30"  :["#phi(E_{T}^{miss}) - \geq 1 jet in HEM with pT>30 GeV",50,-4,4,True,0,[],[],[]] 
,	   "Met_VetoSoftActivity40"          :["E_{T}^{miss} (GeV), veto events with activity < 40GeV",50,0,3000,True,0,[],[],[]] 
,	   "MET_phi_VetoSoftActivity40"      :["#phi(E_{T}^{miss}),  veto events with activity < 40GeV",50,-4,4,True,0,[],[],[]] 
,	   "Met"          :["E_{T}^{miss} (GeV)",50,0,3000,True,0,[],[],[]] 
,	   "CaloMET_phi"  :["Calo #phi(E_{T}^{miss})",50,-4,4,True,0,[],[],[]] 
,	   "Calo_Met"     :["Calo E_{T}^{miss} (GeV)",50,0,3000,True,0,[],[],[]] 
,	   "TkMET_over_MET"  :["Tk MET / MET",30,0,3,True,0,[],[],[]] 
,	   "TkMET_reldiff_MET"  :["PF MET - Tk MET / PF MET",80,-2,2,True,0,[],[],[]] 
,	   "TkMET_phi"  :["Tk #phi(E_{T}^{miss})",50,-4,4,True,0,[],[],[]] 
,	   "TkMET"      :["Tk E_{T}^{miss} (GeV)",50,0,3000,True,0,[],[],[]] 
,	   "CHSMET_phi"  :["CHS #phi(E_{T}^{miss})",50,-4,4,True,0,[],[],[]] 
,	   "CHS_Met"     :["CHS E_{T}^{miss} (GeV)",50,0,3000,True,0,[],[],[]] 
,	   "METCLEAN"     :["(MET-CALOMET)/MET",60,-1.5,1.5,True,0,[],[],[]] 
,	   "dijet_dPhi"   :["#delta#phi(jj)",40,-0,4,True,0,[],[],[]] 
,	   "JetMetmindPhi":["min #Delta#phi(j,E_{T}^{miss})",40,0,4,True,0,[],[],[]] 
,	   "dijet_M"	  :["m_{jj} (GeV)",60,0,6000,True,0,[],[],[]] 
,	   "dijet_dEta"	  :["#Delta#eta_{jj}",50,0,10,True,0,[],[],[]] 
,	   "Leading_jet_eta":["#eta_{j^{1}}",50,-5,5,True,0,[],[],[]] 
,	   "Subleading_jet_eta":["#eta_{j^{2}}",50,-5,5,True,0,[],[],[]] 
,	   "Leading_jet_phi":["#phi_{j^{1}}",50,-4,4,True,0,[],[],[]] 
,	   "Subleading_jet_phi":["#phi_{j^{2}}",50,-4,4,True,0,[],[],[]] 
,	   "Leading_jet_pt":["pT_{j^{1}} (GeV)",60,0,500,True,0,[],[],[]] 
,	   "Subleading_jet_pt":["pT_{j^{2}} (GeV)",60,0,500,True,0,[],[],[]] 
,	   "jet3_eta":["#eta_{j^{3}}",50,-5,5,True,0,[],[],[]] 
,	   "jet4_eta":["#eta_{j^{4}}",50,-5,5,True,0,[],[],[]] 
,	   "jet3_phi":["#phi_{j^{3}}",50,-4,4,True,0,[],[],[]] 
,	   "jet4_phi":["#phi_{j^{4}}",50,-4,4,True,0,[],[],[]] 
,	   "jet3_pt":["pT_{j^{3}} (GeV)",60,0,500,True,0,[],[],[]] 
,	   "jet4_pt":["pT_{j^{4}} (GeV)",60,0,500,True,0,[],[],[]] 
,	   "jetInHEM1_pt":["pT_{j^{HEM,1}} (GeV)",60,0,500,True,0,[],[],[]] 
,	   "jetInHEM1_eta":["#eta_{j^{HEM,1}}",50,-5,5,True,0,[],[],[]] 
,	   "jetInHEM1_phi":["#phi_{j^{HEM,1}}",50,-4,4,True,0,[],[],[]] 
,	   "nJetsInHEM":["#Jets in HEM",10,0,10,True,0,[],[],[]] 
,	   "nMediumBJet":["#b-Jets (medium) ",6,0,6,True,0,[],[],[]] 
,	   "jetInHEM1_closestJet":["Closest p_{T}-ordered jet to HEM (9 = > 8th jet) to HEM jet",9,1,10,False,0,[],[],[]] 
,	   "jetInHEM1_dPhiMET":["#Delta#phi(j^{HEM,1},E_{T}^{miss})",40,0,4,True,0,[],[],[]] 
,	   "jetInHEM1_dPhiLeadJet":["#Delta#phi(j^{HEM,1},j^{1})",40,0,4,True,0,[],[],[]] 
,	   "jetInHEM1_dPhiSubLeadJet":["#Delta#phi(j^{HEM,1},j^{2})",40,0,4,True,0,[],[],[]] 
,	   "jetInHEM1_dRLeadJet":["#Delta#R(j^{HEM,1},j^{1})",40,0,8,True,0,[],[],[]] 
,	   "jetInHEM1_dRSubLeadJet":["#Delta#R(j^{HEM,1},j^{2})",40,0,8,True,0,[],[],[]] 
,	   "MHT_phi"      :["#phi(H_{T}^{miss})",50,-4,4,True,0,[],[],[]] 
,	   "MHT"          :["H_{T}^{miss} (GeV)",50,0,3000,True,0,[],[],[]] 
,	   "MHT_MET_dPhi" :["#Delta#phi(H_{T}^{miss},E_{T}^{miss})",50,-4,4,True,0,[],[],[]] 
, 	   "jet1_neHEF": ["j^{1} neutral Frac.",50,0,1,True,0,[],[],[]]
, 	   "jet2_neHEF": ["j^{2} neutral Frac.",50,0,1,True,0,[],[],[]]
, 	   "jet3_neHEF": ["j^{3} neutral Frac.",50,0,1,True,0,[],[],[]]
, 	   "jet4_neHEF": ["j^{4} neutral Frac.",50,0,1,True,0,[],[],[]]
, 	   "jetInHEM1_neHEF": ["j^{HEM,1} neutral Frac.",50,0,1,True,0,[],[],[]]
, 	   "jet1_chHEF": ["j^{1} charged Frac.",50,0,1,True,0,[],[],[]]
, 	   "jet2_chHEF": ["j^{2} charged Frac.",50,0,1,True,0,[],[],[]]
, 	   "jet3_chHEF": ["j^{3} charged Frac.",50,0,1,True,0,[],[],[]]
, 	   "jet4_chHEF": ["j^{4} charged Frac.",50,0,1,True,0,[],[],[]]
, 	   "jetInHEM1_chHEF": ["j^{HEM,1} charged Frac.",50,0,1,True,0,[],[],[]]
, 	   "CaloToPFMET": ["Calo MET / pF MET",60,0,3,True,0,[],[],[]]
, 	   "CaloToPFMET_InHEM": ["Calo MET / pF MET - with -1.6 < MET PHI < -0.8 ",60,0,3,True,0,[],[],[]]
, 	   "MHTToPFMET": ["MHT / pF MET",60,0,3,True,0,[],[],[]]
, 	   "MHTToPFMET_InHEM": ["MHT / pF MET - with -1.6 < MET PHI < -0.8 ",60,0,3,True,0,[],[],[]]
,	   "PuppiMET_phi"  :["Puppi #phi(E_{T}^{miss})",50,-4,4,True,0,[],[],[]] 
,	   "Puppi_Met"     :["Puppi E_{T}^{miss} (GeV)",50,0,3000,True,0,[],[],[]] 
,	   "softActivityInHEM" :["soft HT in HEM (soft jets pt>2GeV, in HEM) (GeV)",50,-0,500,True,0,[],[],[]]
,	   "softActivityHT2Vec2" :["soft HT (soft jets pt>2GeV) (GeV)",50,-0,500,True,0,[],[],[]]
,	   "softActivityHT2Vec2_phi" :["#phi (soft HT)",50,-4,4,True,0,[],[],[]]
,	   "softActivityHT2Vec2_dPhi_MET" :["#Delta#phi(soft jets HT,MET)",50,-4,4,False,0,[],[],[]]
,	   "LeadingSoftJetInHEM1_pt": ["Leading soft-jet in HEM, p_{T} GeV",60,0,500,True,0,[],[],[]]
,	   "LeadingSoftJetInHEM1_eta":["Leading soft-jet in HEM, #eta_{j^{HEM,1}}",50,-5,5,True,0,[],[],[]] 
,	   "LeadingSoftJetInHEM1_phi":["Leading soft-jet in HEM, #phi_{j^{HEM,1}}",50,-4,4,True,0,[],[],[]] 
,	   "SubleadingSoftJetInHEM1_pt": ["Subleading soft-jet in HEM, p_{T} GeV",60,0,500,True,0,[],[],[]]
,	   "SubleadingSoftJetInHEM1_eta":["Subleading soft-jet in HEM, #eta_{j^{HEM,1}}",50,-5,5,True,0,[],[],[]] 
,	   "SubleadingSoftJetInHEM1_phi":["Subleading soft-jet in HEM, #phi_{j^{HEM,1}}",50,-4,4,True,0,[],[],[]] 
	  }

for i in range(1,6+1): 
  variables["softActivityJet%d_pt"%i]  = ["soft jet %d p_{T} (GeV)"%i,50,0,250,True,0,[],[],[]]
  variables["softActivityJet%d_eta"%i] = ["soft jet %d #eta"%i,50,-5,5,False,0,[],[],[]]
  variables["softActivityJet%d_phi"%i] = ["soft jet %d #phi"%i,50,-4,4,False,0,[],[],[]]
for i in range(1,4+1): 
  variables["isoTrack%d_pt"%i]  = ["iso track %d p_{T} (GeV)"%i,50,0,250,True,0,[],[],[]]
  variables["isoTrack%d_eta"%i] = ["iso track %d #eta"%i,50,-5,5,False,0,[],[],[]]
  variables["isoTrack%d_phi"%i] = ["iso track %d #phi"%i,50,-4,4,False,0,[],[],[]]

# recreate for the VBF category - need to do a deepcopy to really create new objects in the map, not just references to the other ones! 
for var in variables.keys(): variables["VTR"+var]=copy.deepcopy(variables[var])
#print variables 
#sys.exit()
# These get set by the plotter ------------
fName   = ""
fSample = ""
fLabel  = ""

def setInfo(fnam,pnam,label):
  fName   = fnam
  fSample = pnam
  fLabel  = label
#------------------------------------------

# book an output .csv file with two trees, signal and background ? - For training!
#writer =  open("events.csv","w")
#  writer = csv.writer(csvfile,delimiter=' ')
#writer.write(",".join(["file","process","entry_id","label","met_phi","run","event","lumi"])+"\n")
# also make a TTree with all of the info :)

def preselection(tr):
     if tr.MetNoLep < 160 : return False
     if tr.nJets < 2: return False
     if (tr.MET_pt - tr.CaloMET_pt)/tr.MetNoLep > 0.5 : return False
     if tr.isData==1 and (not (tr.met_filters_2018_data>0.1)): return False
     if (not tr.isData==1) and (not (tr.met_filters_2018_mc>0.1)): return False
     if abs(tr.JetMetmindPhi) < 0.5 : return False
     if tr.nMediumBJet > 0.5 : return False
     if tr.nLoosePhoton > 0.5 : return False
     if tr.isData : 
       if tr.nVetoElectron > 0.5 : return False 
       if tr.nLooseMuon    > 0.5 : return False 
       if tr.nVLooseTau    > 0.5 : return False 
     
     return True
     # here define a simple analysis (selection of cuts or whatever)

def selectVTR(tr):
     
     if tr.MetNoLep >= 250 : return False 
     if tr.lMjj     < 900 : return False
     if abs(tr.JetMetmindPhi) < 1.8 : return False
     if tr.lMjj_jet1_pt    < 140 : return False
     if tr.lMjj_jet2_pt    < 70 : return False
     if abs(tr.lMjj_dijet_dphi) > 1.5 : return False
     if abs(tr.lMjj_dijet_deta) < 1   : return False
     if not (tr.lMjj_jet1_eta*tr.lMjj_jet2_eta < 0): return False
     if abs(tr.lMjj_jet1_eta)    > 4.7 : return False
     if abs(tr.lMjj_jet2_eta)    > 4.7 : return False
     if tr.isData==1 and (not (tr.HLT_DiJet110_35_Mjj650_PFMET110 > 0.1 or tr.HLT_TripleJet110_35_35_Mjj650_PFMET110 > 0.1) ): return False 
     return True

def selectMTR(tr): 
     
     if tr.MetNoLep < 250 : return False
     if tr.dijet_M  < 200 : return False
     if tr.Leading_jet_pt     < 80 : return False
     if tr.Subleading_jet_pt  < 40 : return False
     if abs(tr.dijet_dPhi)    > 1.5 : return False
     if abs(tr.dijet_dEta)    < 1   : return False
     if not (tr.Leading_jet_eta*tr.Subleading_jet_eta < 0): return False
     if abs(tr.Leading_jet_eta)    > 4.7 : return False
     if abs(tr.Subleading_jet_eta) > 4.7 : return False
     if tr.isData==1 and (not (tr.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight>0.1 or tr.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60>0.1) ): return False 
     return True

def ObjectIsInHEM(vec): 
  if (vec.Eta() > -3 and vec.Eta() < -1.2 and vec.Phi() < -0.5 and vec.Phi() > -1.9 ) : return True
  return False

gEntry=[0]
gI=[0]

def Fill(var,v,w):
    #print gEntry[0], gI[0]
    if var in variables.keys(): variables[var][gEntry[0]][gI[0]].Fill(v,w)
    else: sys.exit("No Variable booked called %s"%(var))

def thingsToStrings(l):
    rlist = []
    for ll in l : rlist.append(str(ll))
    return rlist

def noOverlap(j,object_list,maxdR):
     for obj in object_list:
       if j[1].DeltaR(obj[1]) < maxdR: return False
     return True

def doAnalysis(tr,entry,i,w):
     #print fName, fSample, fLabel 
     # override weight variable : 
     gI[0]=i
     gEntry[0]=entry

     # depending on the selection, dijet is the leading pair or highest mJJ pair  
     jet1    = ROOT.TVector3();
     jet2    = ROOT.TVector3();
     dijet4vec = ROOT.TLorentzVector(); 

     passSel = ""
     if selectVTR(tr): 
       passSel = "VTR"
       jet1.SetPtEtaPhi(tr.lMjj_jet1_pt,tr.lMjj_jet1_eta,tr.lMjj_jet1_phi)
       jet2.SetPtEtaPhi(tr.lMjj_jet2_pt,tr.lMjj_jet2_eta,tr.lMjj_jet2_phi)

       dijet = jet1+jet2
       dijet4vec.SetPtEtaPhiM(dijet.Pt(),dijet.Eta(),dijet.Phi(),tr.lMjj)

     elif selectMTR(tr): 
       jet1.SetPtEtaPhi(tr.Leading_jet_pt,tr.Leading_jet_eta,tr.Leading_jet_phi)
       jet2.SetPtEtaPhi(tr.Subleading_jet_pt,tr.Subleading_jet_eta,tr.Subleading_jet_phi)
       
       dijet = jet1+jet2
       dijet4vec.SetPtEtaPhiM(dijet.Pt(),dijet.Eta(),dijet.Phi(),tr.dijet_M)

     else : return 0; 
     

     # now setup the weights
     if tr.isData==1 : 
       w=1
     else :
        if passSel == "VTR": 
            w = tr.trigger_weight_VBF2018*tr.puWeight*tr.xs_weight*tr.VLooseSITTau_eventVetoW*tr.VetoElectron_eventVetoW*tr.LooseMuon_eventVetoW*L
            w *= tr.fnlo_SF_EWK_corr*tr.fnlo_SF_QCD_corr_QCD_proc_VTR*tr.fnlo_SF_QCD_corr_EWK_proc
        else: 
            w = tr.trigger_weight_METMHT2018*tr.puWeight*tr.xs_weight*tr.VLooseSITTau_eventVetoW*tr.VetoElectron_eventVetoW*tr.LooseMuon_eventVetoW*L
            w *= tr.fnlo_SF_EWK_corr*tr.fnlo_SF_QCD_corr_QCD_proc_MTR*tr.fnlo_SF_QCD_corr_EWK_proc
    
     
     jetHEM  = ROOT.TVector3();
     jet3 = ROOT.TVector3();
     jet4 = ROOT.TVector3();
     jet5 = ROOT.TVector3();
     jet6 = ROOT.TVector3();
     jet7 = ROOT.TVector3();
     jet8 = ROOT.TVector3();
     METVEC = ROOT.TVector3();
     MHT = ROOT.TVector3();

     METVEC.SetPtEtaPhi(tr.MetNoLep,0,tr.MetPhiNoLep)
     MHT.SetPtEtaPhi(tr.MHT_pt,0,tr.MHT_phi)
     jetHEM.SetPtEtaPhi(tr.jetInHEM1_pt,tr.jetInHEM1_eta,tr.jetInHEM1_phi)
     
     jet3.SetPtEtaPhi(tr.jet3_pt,tr.jet3_eta,tr.jet3_phi)
     jet4.SetPtEtaPhi(tr.jet4_pt,tr.jet4_eta,tr.jet4_phi)
     jet5.SetPtEtaPhi(tr.jet5_pt,tr.jet5_eta,tr.jet5_phi)
     jet6.SetPtEtaPhi(tr.jet6_pt,tr.jet6_eta,tr.jet6_phi)
     jet7.SetPtEtaPhi(tr.jet7_pt,tr.jet7_eta,tr.jet7_phi)
     jet8.SetPtEtaPhi(tr.jet8_pt,tr.jet8_eta,tr.jet8_phi)

     deltaPhiHEMJetMET          = abs(METVEC.DeltaPhi(jetHEM))
     deltaPhiHEMJetLeadJet      = abs(jetHEM.DeltaPhi(jet1))
     deltaPhiHEMJetSubLeadJet   = abs(jetHEM.DeltaPhi(jet2))

     deltaRHEMJetLeadJet    = abs(jetHEM.DeltaR(jet1)) 
     deltaRHEMJetSubLeadJet = abs(jetHEM.DeltaR(jet2))
     if jet3.Pt()>1: deltaRHEMJetJet3       = abs(jetHEM.DeltaR(jet3))  
     else : deltaRHEMJetJet3=1000
     if jet4.Pt()>1: deltaRHEMJetJet4       = abs(jetHEM.DeltaR(jet4))  
     else : deltaRHEMJetJet4=1000
     if jet5.Pt()>1: deltaRHEMJetJet5       = abs(jetHEM.DeltaR(jet5))  
     else : deltaRHEMJetJet5=1000
     if jet6.Pt()>1: deltaRHEMJetJet6       = abs(jetHEM.DeltaR(jet6))  
     else : deltaRHEMJetJet6=1000
     if jet7.Pt()>1: deltaRHEMJetJet7       = abs(jetHEM.DeltaR(jet7))  
     else : deltaRHEMJetJet7=1000
     if jet8.Pt()>1: deltaRHEMJetJet8       = abs(jetHEM.DeltaR(jet8))  
     else : deltaRHEMJetJet8=1000


     closetJet=0
     if deltaRHEMJetLeadJet<0.1 : closetJet=1.1
     elif deltaRHEMJetSubLeadJet<0.1 : closetJet=2.1
     elif deltaRHEMJetJet3<0.1 : closetJet=3.1
     elif deltaRHEMJetJet4<0.1 : closetJet=4.1
     elif deltaRHEMJetJet5<0.1 : closetJet=5.1
     elif deltaRHEMJetJet6<0.1 : closetJet=6.1
     elif deltaRHEMJetJet7<0.1 : closetJet=7.1
     elif deltaRHEMJetJet8<0.1 : closetJet=8.1
     else : closetJet = 9.1
     
     deltaPhiHTMET = MHT.DeltaPhi(METVEC)
     
     # soft jets --> additional to our leading VBF Jets
     soft_jets = []
     for sj in range(1,7): 
       if getattr(tr,"softActivityJet%d_pt"%sj) <2 : continue 
       this_sj = ROOT.TVector3()
       this_sj.SetPtEtaPhi(getattr(tr,"softActivityJet%d_pt"%sj),getattr(tr,"softActivityJet%d_eta"%sj),getattr(tr,"softActivityJet%d_phi"%sj))

       soft_jets.append([this_sj.Pt(),this_sj])
     
     # isolated tracks 
     iso_tracks = []
     for sj in range(1,5): 
       if getattr(tr,"isoTrack%d_pt"%sj) <2 : continue 
       this_sj = ROOT.TVector3()
       this_sj.SetPtEtaPhi(getattr(tr,"isoTrack%d_pt"%sj),getattr(tr,"isoTrack%d_eta"%sj),getattr(tr,"isoTrack%d_phi"%sj))

       iso_tracks.append([this_sj.Pt(),this_sj])
     iso_tracks = sorted(iso_tracks, key=lambda x: x[0])
     isoTrackHT2Vec = ROOT.TVector3()
     isoTrackActivityInHEM=0
     iso_tracks_in_hem=[]


     for sj in iso_tracks: 
       if sj[0]>2 : 
       	isoTrackHT2Vec+=sj[1]
	if ObjectIsInHEM(sj[1]):
	 isoTrackActivityInHEM += sj[1].Pt()
	 iso_tracks_in_hem.append(sj)

     #print soft_jets
     soft_jets = sorted(soft_jets, key=lambda x: x[0])
     softJetHT2Vec = ROOT.TVector3()
     softJetActivityInHEM=0
     soft_jets_in_hem=[]
     soft_jets_in_hem_noIso=[]
     for sj in soft_jets: 
       if sj[0]>2 : 
       	softJetHT2Vec+=sj[1]
	if ObjectIsInHEM(sj[1]):
	 softJetActivityInHEM += sj[1].Pt()
	 soft_jets_in_hem.append(sj)
	 if noOverlap(sj,iso_tracks,0.4): soft_jets_in_hem_noIso.append(sj)

     #print soft_jets_in_hem
     soft_jets_in_hem = sorted(soft_jets_in_hem, key=lambda x: x[0])
     soft_jets_in_hem_noIso = sorted(soft_jets_in_hem_noIso, key=lambda x: x[0])
     
     deltaPhiSJMET = softJetHT2Vec.DeltaPhi(METVEC) if softJetHT2Vec.Pt()>1 else 10000

     Fill(passSel+"MHT_phi",MHT.Phi(),w)

     Fill(passSel+"MHT_phi",MHT.Phi(),w)
     Fill(passSel+"MHT",MHT.Pt(),w)
     Fill(passSel+"MHT_MET_dPhi",deltaPhiHTMET,w)
     Fill(passSel+"MET_phi",tr.MetPhiNoLep,w)
     Fill(passSel+"Met",tr.MetNoLep,w)
     Fill(passSel+"CaloMET_phi",tr.CaloMET_phi,w)
     Fill(passSel+"Calo_Met",tr.CaloMET_pt,w)
     Fill(passSel+"CHSMET_phi",tr.ChsMET_phi,w)
     Fill(passSel+"CHS_Met",tr.ChsMET_pt,w)
     Fill(passSel+"JetMetmindPhi",tr.JetMetmindPhi,w)
     Fill(passSel+"dijet_dPhi",abs(dijet.DeltaPhi(METVEC)),w)
     Fill(passSel+"dijet_M",dijet4vec.M(),w)
     Fill(passSel+"dijet_dEta",abs(jet1.Eta()-jet2.Eta()),w)
     Fill(passSel+"jetInHEM1_pt",tr.jetInHEM1_pt,w)
     Fill(passSel+"jetInHEM1_phi",tr.jetInHEM1_phi,w)
     Fill(passSel+"jetInHEM1_eta",tr.jetInHEM1_eta,w)
     if len(soft_jets_in_hem):
       Fill(passSel+"LeadingSoftJetInHEM1_pt",soft_jets_in_hem[0][1].Pt(),w)
       Fill(passSel+"LeadingSoftJetInHEM1_phi",soft_jets_in_hem[0][1].Phi(),w)
       Fill(passSel+"LeadingSoftJetInHEM1_eta",soft_jets_in_hem[0][1].Eta(),w)
     if len(soft_jets_in_hem)>1:
       Fill(passSel+"SubleadingSoftJetInHEM1_pt",soft_jets_in_hem[1][1].Pt(),w)
       Fill(passSel+"SubleadingSoftJetInHEM1_phi",soft_jets_in_hem[1][1].Phi(),w)
       Fill(passSel+"SubleadingSoftJetInHEM1_eta",soft_jets_in_hem[1][1].Eta(),w)
     if tr.nJetsInHEM > 0 and tr.jetInHEM1_pt>30 :
       Fill(passSel+"jetInHEM1_dPhiMET",deltaPhiHEMJetMET,w)
       Fill(passSel+"jetInHEM1_dPhiLeadJet",deltaPhiHEMJetLeadJet,w)
       Fill(passSel+"jetInHEM1_dPhiSubLeadJet",deltaPhiHEMJetSubLeadJet,w)
       Fill(passSel+"jetInHEM1_dRLeadJet",deltaRHEMJetLeadJet,w)
       Fill(passSel+"jetInHEM1_dRSubLeadJet",deltaRHEMJetSubLeadJet,w)
       Fill(passSel+"jetInHEM1_closestJet",closetJet,w)
       Fill(passSel+"jetInHEM1_chHEF",tr.jetInHEM1_chHEF,w)
       Fill(passSel+"jetInHEM1_neHEF",tr.jetInHEM1_neHEF,w)

     Fill(passSel+"Leading_jet_eta"   ,jet1.Eta(),w)
     Fill(passSel+"Subleading_jet_eta",jet2.Eta(),w)
     Fill(passSel+"Leading_jet_phi"   ,jet1.Phi(),w)
     Fill(passSel+"Subleading_jet_phi",jet2.Phi(),w)
     Fill(passSel+"Leading_jet_pt"    ,jet1.Pt(),w)
     Fill(passSel+"Subleading_jet_pt" ,jet2.Pt(),w)
     Fill(passSel+"jet3_eta",tr.jet3_eta,w)
     Fill(passSel+"jet4_eta",tr.jet4_eta,w)
     Fill(passSel+"jet3_phi",tr.jet3_phi,w)
     Fill(passSel+"jet4_phi",tr.jet4_phi,w)
     Fill(passSel+"jet3_pt",tr.jet3_pt,w)
     Fill(passSel+"jet4_pt",tr.jet4_pt,w)
     Fill(passSel+"nJetsInHEM",tr.nJetsInHEM,w)
     Fill(passSel+"jet1_neHEF",tr.Leading_jet_neHEF,w)
     Fill(passSel+"jet2_neHEF",tr.Subleading_jet_neHEF,w)
     Fill(passSel+"jet3_neHEF",tr.jet3_neHEF,w)
     Fill(passSel+"jet4_neHEF",tr.jet4_neHEF,w)
     Fill(passSel+"jet1_chHEF",tr.Leading_jet_chHEF,w)
     Fill(passSel+"jet2_chHEF",tr.Subleading_jet_chHEF,w)
     Fill(passSel+"jet3_chHEF",tr.jet3_chHEF,w)
     Fill(passSel+"jet4_chHEF",tr.jet4_chHEF,w)

     Fill(passSel+"TkMET",tr.TkMET_pt,w)
     Fill(passSel+"TkMET_phi",tr.TkMET_phi,w)
     Fill(passSel+"TkMET_over_MET",tr.TkMET_pt/tr.MetNoLep,w)
     Fill(passSel+"TkMET_reldiff_MET",(tr.MetNoLep-tr.TkMET_pt)/tr.MetNoLep,w)

     if (tr.nJetsInHEM > 0 and tr.jetInHEM1_pt>30) : Fill(passSel+"MET_phi_HEMJET30",tr.MetPhiNoLep,w)
     Fill(passSel+"nMediumBJet",tr.nMediumBJet,w)

     Fill(passSel+"CaloToPFMET",tr.CaloMET_pt/tr.MetNoLep,w)
     if  (tr.MetPhiNoLep < -0.8 and tr.MetPhiNoLep > -1.6):  Fill(passSel+"CaloToPFMET_InHEM",tr.CaloMET_pt/tr.MetNoLep,w)
     
     Fill(passSel+"MHTToPFMET",tr.MHT_pt/tr.MetNoLep,w)
     if  (tr.MetPhiNoLep < -0.8 and tr.MetPhiNoLep > -1.6):  Fill(passSel+"MHTToPFMET_InHEM",tr.MHT_pt/tr.MetNoLep,w)

     Fill(passSel+"PuppiMET_phi",tr.PuppiMET_phi,w)
     Fill(passSel+"Puppi_Met",tr.PuppiMET_pt,w)

     Fill(passSel+"softActivityInHEM",softJetActivityInHEM,w)
     Fill(passSel+"softActivityHT2Vec2",softJetHT2Vec.Pt(),w)
     Fill(passSel+"softActivityHT2Vec2_phi",softJetHT2Vec.Phi(),w)
     Fill(passSel+"softActivityHT2Vec2_dPhi_MET",deltaPhiSJMET,w)

     Fill(passSel+"dijet_pT",dijet.Pt(),w)
     Fill(passSel+"dijet_phi",dijet.Phi(),w)
     Fill(passSel+"dijet_pT_reldiff_MET",(dijet.Pt()-tr.MetNoLep)/tr.MetNoLep,w)
     if ( tr.MetPhiNoLep > -1.6 and tr.MetPhiNoLep < -0.8) :Fill(passSel+"dijet_pT_reldiff_MET_METWindow",(dijet.Pt()-tr.MetNoLep)/tr.MetNoLep,w)

     if not( ((dijet.Pt()-tr.MetNoLep)/tr.MetNoLep) > 0.4 ) : 
     	Fill(passSel+"MET_phi_VetoRelDiff0p4",tr.MetPhiNoLep,w)
     	Fill(passSel+"Met_VetoRelDiff0p4",tr.MetNoLep,w)

     if not( ((dijet.Pt()-tr.MetNoLep)/tr.MetNoLep) > 0.4  and (tr.MetPhiNoLep > -1.6 and tr.MetPhiNoLep < -0.8) ) : 
        Fill(passSel+"MET_phi_VetoRelDiff0p4_METWindow",tr.MetPhiNoLep,w)
        Fill(passSel+"Met_VetoRelDiff0p4_METWindow",tr.MetNoLep,w)
     
     if softJetActivityInHEM > 30 : 
     	Fill(passSel+"MET_phi_SoftJETHEM30",tr.MetPhiNoLep,w)
     	Fill(passSel+"Met_SoftJETHEM30",tr.MetNoLep,w)
     else: 
     	Fill(passSel+"MET_phi_VetoSoftJETHEM30",tr.MetPhiNoLep,w)
     	Fill(passSel+"Met_VetoSoftJETHEM30",tr.MetNoLep,w)
     if softJetActivityInHEM > 5 : 
     	Fill(passSel+"MET_phi_SoftJETHEM5",tr.MetPhiNoLep,w)
     	Fill(passSel+"Met_SoftJETHEM5",tr.MetNoLep,w)

     if not(len(soft_jets_in_hem) and soft_jets_in_hem[0][1].Pt() > 0) : 
     	Fill(passSel+"MET_phi_VetoSoftJetInHEM",tr.MetPhiNoLep,w)
     	Fill(passSel+"Met_VetoSoftJetInHEM",tr.MetNoLep,w)

     if not(len(soft_jets_in_hem) and soft_jets_in_hem[0][1].Pt() > 0 and tr.MetPhiNoLep > -1.6 and tr.MetPhiNoLep < -0.8): 
        Fill(passSel+"MET_phi_VetoSoftJetInHEM_METWindow",tr.MetPhiNoLep,w)
        Fill(passSel+"Met_VetoSoftJetInHEM_METWindow",tr.MetNoLep,w)
     
     if not( (len(soft_jets_in_hem) and soft_jets_in_hem[0][1].Pt() > 0) or (len(iso_tracks_in_hem) and iso_tracks_in_hem[0][1].Pt() > 0) ) : 
     	Fill(passSel+"MET_phi_VetoSoftJetOrIsoTrackInHEM",tr.MetPhiNoLep,w)
     	Fill(passSel+"Met_VetoSoftJetOrIsoTrackInHEM",tr.MetNoLep,w)

     if not( ((len(soft_jets_in_hem) and soft_jets_in_hem[0][1].Pt() > 0) or (len(iso_tracks_in_hem) and iso_tracks_in_hem[0][1].Pt() > 0)) and (tr.MetPhiNoLep > -1.6 and tr.MetPhiNoLep < -0.8) ) : 
        Fill(passSel+"MET_phi_VetoSoftJetOrIsoTrackInHEM_METWindow",tr.MetPhiNoLep,w)
        Fill(passSel+"Met_VetoSoftJetOrIsoTrackInHEM_METWindow",tr.MetNoLep,w)
     
     if not(len(soft_jets_in_hem_noIso) and soft_jets_in_hem_noIso[0][1].Pt() > 0 and tr.MetPhiNoLep > -1.6 and tr.MetPhiNoLep < -0.8): 
        Fill(passSel+"MET_phi_VetoSoftJetInHEM_noIso_METWindow",tr.MetPhiNoLep,w)
        Fill(passSel+"Met_VetoSoftJetInHEM_noIso_METWindow",tr.MetNoLep,w)
     
     if not(len(iso_tracks_in_hem) and iso_tracks_in_hem[0][1].Pt() > 0) : 
     	Fill(passSel+"MET_phi_VetoIsoTrackInHEM",tr.MetPhiNoLep,w)
     	Fill(passSel+"Met_VetoIsoTrackInHEM",tr.MetNoLep,w)

     if not(len(iso_tracks_in_hem) and iso_tracks_in_hem[0][1].Pt() > 0 and tr.MetPhiNoLep > -1.6 and tr.MetPhiNoLep < -0.8): 
        Fill(passSel+"MET_phi_VetoIsoTrackInHEM_METWindow",tr.MetPhiNoLep,w)
        Fill(passSel+"Met_VetoIsoTrackInHEM_METWindow",tr.MetNoLep,w)
     
     if softJetHT2Vec.Pt() > 40 : 
     	Fill(passSel+"MET_phi_VetoSoftActivity40",tr.MetPhiNoLep,w)
     	Fill(passSel+"Met_VetoSoftActivity40",tr.MetNoLep,w)
     else: 
     	Fill(passSel+"MET_phi_VetoSoftJETHEM5",tr.MetPhiNoLep,w)
     	Fill(passSel+"Met_VetoSoftJETHEM5",tr.MetNoLep,w)

     for j,sj in enumerate(soft_jets): #range(1,7): 
       Fill(passSel+"softActivityJet%d_pt"%(j+1), sj[1].Pt(),w)#getattr(tr,"softActivityJet%d_pt"%sj),w)
       Fill(passSel+"softActivityJet%d_eta"%(j+1),sj[1].Eta(),w)#getattr(tr,"softActivityJet%d_eta"%sj),w)
       Fill(passSel+"softActivityJet%d_phi"%(j+1),sj[1].Phi(),w)#getattr(tr,"softActivityJet%d_phi"%sj),w)
     
     for j,sj in enumerate(iso_tracks): #range(1,7): 
       Fill(passSel+"isoTrack%d_pt"%(j+1), sj[1].Pt(),w)#getattr(tr,"isoTrack%d_pt"%sj),w)
       Fill(passSel+"isoTrack%d_eta"%(j+1),sj[1].Eta(),w)#getattr(tr,"isoTrack%d_eta"%sj),w)
       Fill(passSel+"isoTrack%d_phi"%(j+1),sj[1].Phi(),w)#getattr(tr,"isoTrack%d_phi"%sj),w)

     

     Fill(passSel+"METCLEAN",(tr.MET_pt - tr.CaloMET_pt)/tr.MetNoLep,w) 
     return w 
     # can also do the delta phi between the photons and the two lead jets?

