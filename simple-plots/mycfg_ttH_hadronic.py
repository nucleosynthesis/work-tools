# Configuration file for plotting
# L is the Luminosity in fb, signalScale is a factor for the signal to be scaled to - thats it 
import ROOT 
import math 
import csv
import array

treeName    = "trilinearTree"

L           = 3000 # = 100/fb
signalScale = 10
minWeight   = -9.e100
#odir 	    = "plots_extendtracker_preselection_cutBDT_gt_0p45"
odir 	    = "plots_ttH_hadronic_preapp"
runBDT      = False

#cutBDTMinimum = 0.45
cutBDTMinimum = -1

directory = "/afs/cern.ch/user/j/jolangfo/public/ForNick/trilinear_Ntuples/btag_correction/ttHHad/"

pre_backs = directory+"bkg/ttHHad_background_"
pre_sigas = directory+"sig/ttHHad_signal_"

samples = { 
	"#gamma-#gamma"	:[ [pre_backs+"DiPhotonJetsBox_MGG-80toInf.root"], [1], ROOT.kAzure-9 ]
	,"#gamma-jet"	:[ [pre_backs+"GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf.root"], [1], ROOT.kAzure+2 ]
	,"tt+#gamma#gamma":[ [pre_backs+"ttgammagamma.root"], [1], ROOT.kGray ]
	,"tt+#gamma"	:[ [pre_backs+"ttgamma_dilepton.root",pre_backs+"ttgamma_hadronic.root",pre_backs+"ttgamma_singlelepfromt.root", pre_backs+"ttgamma_singlelepfromtbar.root"], [1,1,1,1], ROOT.kGray+1 ]
	,"tt"		:[ [pre_backs+"ttbar.root"], [1], ROOT.kGray+3 ]
	,"t+#gamma+jets":[ [pre_backs+"TGJet_inclusive.root"], [1], ROOT.kGray+2 ]
#	,"Z+b/Z(bb)":[ ["zj_b.root"], [6522.7694364], ROOT.kAzure-2 ]
	  }

order = ["tt+#gamma#gamma","tt+#gamma","t+#gamma+jets","tt","#gamma-jet","#gamma-#gamma"]

signals = {
	"ttH" :[ [pre_sigas+"ttH_M125.root"],[1],ROOT.kRed+1]
	,"ggH":[ [pre_sigas+"ggH_M125.root"],[1],ROOT.kGreen+2]
	,"VH" :[ [pre_sigas+"VH_M125.root"],[1],ROOT.kGreen+4]
	,"tH" :[ [pre_sigas+"THQ_M125.root",pre_sigas+"THW_M125.root"],[1,1],ROOT.kPink+7]
	}

variables = { 
	   "mgg":["m_{#gamma#gamma} (GeV)",20,100,180,False,0,[],[]] 
	   ,"mgg_pt_0_50"	:["m_{#gamma#gamma} (GeV) (p_{T}^{#gamma#gamma} < 50 GeV)",20,100,180,False,0,[],[]] 
	   ,"mgg_pt_50_100"	:["m_{#gamma#gamma} (GeV) (50 < p_{T}^{#gamma#gamma} < 50 GeV)",20,100,180,False,0,[],[]] 
	   ,"mgg_pt_100_150"	:["m_{#gamma#gamma} (GeV) (100 < p_{T}^{#gamma#gamma} < 150 GeV)",20,100,180,False,0,[],[]] 
	   ,"mgg_pt_150_250"	:["m_{#gamma#gamma} (GeV) (150 < p_{T}^{#gamma#gamma} < 250 GeV)",20,100,180,False,0,[],[]] 
	   ,"mgg_pt_250"	:["m_{#gamma#gamma} (GeV) (p_{T}^{#gamma#gamma} > 250 GeV)",20,100,180,False,0,[],[]] 
	   ,"scalarHT":["H_{T} (GeV)",40,0,4000,True,0,[],[]] 
	   ,"Njets":["N jets",15,0,15,True,0,[],[]] 
	   ,"Nbjets":["N b-jets",8,0,8,True,0,[],[]] 
	   ,"MET":["p_{T}^{miss} (GeV)",40,0,400,True,0,[],[]] 
	   ,"pTH_reco":["p_{T}^{#gamma#gamma} (GeV)",40,0,400,True,0,[],[]] 
	   ,"pho1_pT":["p_{T}^{#gamma 1} (GeV)",40,0,400,True,0,[],[]] 
	   ,"pho2_pT":["p_{T}^{#gamma 2} (GeV)",30,0,300,True,0,[],[]] 
	   ,"pho1_pTom":["p_{T}^{#gamma 1}/m_{#gamma#gamma}",20,0,2,True,0,[],[]] 
	   ,"pho2_pTom":["p_{T}^{#gamma 2}/m_{#gamma#gamma}",20,0,2,True,0,[],[]] 
	   ,"pho1_eta":["|#eta|^{#gamma 1} (GeV)",10,0,3,True,0,[],[]] 
	   ,"pho2_eta":["|#eta|^{#gamma 2} (GeV)",10,0,3,True,0,[],[]] 
	   ,"pho1_ch_isolation":["Isolation - Sum charged p_{T} / p_{T}^{#gamma 1} ",40,0,.4,True,0,[],[]] 
	   ,"pho2_ch_isolation":["Isolation - Sum charged p_{T} / p_{T}^{#gamma 2} ",40,0,.4,True,0,[],[]] 
	   ,"jet1_pT":["p_{T}^{jet 1} (GeV)",40,0,400,True,0,[],[]] 
	   ,"jet1_eta":["|#eta|^{jet 1} (GeV)",15,0,5,True,0,[],[]] 
	   ,"jet2_pT":["p_{T}^{jet 2} (GeV)",40,0,400,True,0,[],[]] 
	   ,"jet2_eta":["|#eta|^{jet 2} (GeV)",15,0,5,True,0,[],[]] 
	   ,"jet3_pT":["p_{T}^{jet 3} (GeV)",30,0,300,True,0,[],[]] 
	   ,"jet3_eta":["|#eta|^{jet 3} (GeV)",15,0,5,True,0,[],[]] 
	   ,"jet4_pT":["p_{T}^{jet 4} (GeV)",30,0,300,True,0,[],[]] 
	   ,"jet4_eta":["|#eta|^{jet 4} (GeV)",15,0,5,True,0,[],[]] 
	   ,"bdt_class":["Hadronic BDT output",12,-0.8,1,True,0,[],[]] 
	   ,"mindphi_gg_jets":["min #Delta#phi(#gamma#gamma,j)",50,0,5,True,0,[],[]] 

	  }


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
writer =  open("events.csv","w")
#  writer = csv.writer(csvfile,delimiter=' ')
writer.write(",".join(["file","process","entry_id","label","weight","Njets","Nbjets","scalarHT","MET","pho1_ptom","pho2_ptom","pho1_eta","pho2_eta", \
"j1_pt","j1_eta","j2_pt","j2_eta","j3_pt","j3_eta","j4_pt","j4_eta"])+"\n")
# also make a TTree with all of the info :)
fout    = ROOT.TFile("bdt_trees_hadronic.root","RECREATE")
fout.cd()
oTree_s = ROOT.TTree("tree_s","tree_s")
oTree_b = ROOT.TTree("tree_b","tree_b")


b_weight  = array.array('f',[0]) 
b_Njets   = array.array('f',[0]) 
b_Nbjets  = array.array('f',[0]) 
b_scalarHT= array.array('f',[0]) 
b_pTgg    = array.array('f',[0]) 
b_MET     = array.array('f',[0]) 
b_pho1_ptom     = array.array('f',[0]) 
b_pho2_ptom     = array.array('f',[0]) 
b_pho1_eta      = array.array('f',[0]) 
b_pho2_eta      = array.array('f',[0]) 
b_pho1_ch_isolation      = array.array('f',[0]) 
b_pho2_ch_isolation      = array.array('f',[0]) 
b_j1_pt		= array.array('f',[0]) 
b_j1_eta	= array.array('f',[0]) 
b_j2_pt		= array.array('f',[0]) 
b_j2_eta	= array.array('f',[0]) 
b_j3_pt		= array.array('f',[0]) 
b_j3_eta	= array.array('f',[0]) 
b_j4_pt		= array.array('f',[0]) 
b_j4_eta	= array.array('f',[0]) 
b_BDT		= array.array('f',[0]) 
b_mgg		= array.array('f',[0]) 
b_mindphi_gg_jets = array.array('f',[0]) 

oTree_s.Branch("weight",	b_weight,"weight/F")
oTree_s.Branch("Njets",		b_Njets,"Njets/F")
oTree_s.Branch("Nbjets",	b_Nbjets,"Nbjets/F")
oTree_s.Branch("scalarHT",	b_scalarHT,"scalarHT/F")
oTree_s.Branch("pTgg",		b_pTgg,"pTgg/F")
oTree_s.Branch("MET",		b_MET,"MET/F")
oTree_s.Branch("pho1_ptom",	b_pho1_ptom,"pho1_ptom/F")
oTree_s.Branch("pho2_ptom",	b_pho2_ptom,"pho2_ptom/F")
oTree_s.Branch("pho1_eta",	b_pho1_eta,"pho1_eta/F")
oTree_s.Branch("pho2_eta",	b_pho2_eta,"pho2_eta/F")
oTree_s.Branch("pho1_ch_isolation",	b_pho1_ch_isolation,"pho1_ch_isolation/F")
oTree_s.Branch("pho2_ch_isolation",	b_pho2_ch_isolation,"pho2_ch_isolation/F")
oTree_s.Branch("j1_pt",		b_j1_pt,"j1_pt/F")
oTree_s.Branch("j1_eta",	b_j1_eta,"j1_eta/F")
oTree_s.Branch("j2_pt",		b_j2_pt,"j2_pt/F")
oTree_s.Branch("j2_eta",	b_j2_eta,"j2_eta/F")
oTree_s.Branch("j3_pt",		b_j3_pt,"j3_pt/F")
oTree_s.Branch("j3_eta",	b_j3_eta,"j3_eta/F")
oTree_s.Branch("j4_pt",		b_j4_pt,"j4_pt/F")
oTree_s.Branch("j4_eta",	b_j4_eta,"j4_eta/F")
oTree_s.Branch("out_BDTG",		b_BDT,"out_BDTG/F")
oTree_s.Branch("mgg",		b_mgg,"mgg/F")
oTree_s.Branch("mindphi_gg_jets",		b_mindphi_gg_jets,"mindphi_gg_jets/F")


oTree_b.Branch("weight",b_weight,"weight/F")
oTree_b.Branch("Njets",b_Njets,"Njets/F")
oTree_b.Branch("Nbjets",b_Nbjets,"Nbjets/F")
oTree_b.Branch("scalarHT",b_scalarHT,"scalarHT/F")
oTree_b.Branch("pTgg",b_pTgg,"pTgg/F")
oTree_b.Branch("MET",b_MET,"MET/F")
oTree_b.Branch("pho1_ptom",b_pho1_ptom,"pho1_ptom/F")
oTree_b.Branch("pho2_ptom",b_pho2_ptom,"pho2_ptom/F")
oTree_b.Branch("pho1_eta",b_pho1_eta,"pho1_eta/F")
oTree_b.Branch("pho2_eta",b_pho2_eta,"pho2_eta/F")
oTree_b.Branch("pho1_ch_isolation",	b_pho1_ch_isolation,"pho1_ch_isolation/F")
oTree_b.Branch("pho2_ch_isolation",	b_pho2_ch_isolation,"pho2_ch_isolation/F")
oTree_b.Branch("j1_pt",b_j1_pt,"j1_pt/F")
oTree_b.Branch("j1_eta",b_j1_eta,"j1_eta/F")
oTree_b.Branch("j2_pt",b_j2_pt,"j2_pt/F")
oTree_b.Branch("j2_eta",b_j2_eta,"j2_eta/F")
oTree_b.Branch("j3_pt",b_j3_pt,"j3_pt/F")
oTree_b.Branch("j3_eta",b_j3_eta,"j3_eta/F")
oTree_b.Branch("j4_pt",b_j4_pt,"j4_pt/F")
oTree_b.Branch("j4_eta",b_j4_eta,"j4_eta/F")
oTree_b.Branch("out_BDTG",b_BDT,"out_BDTG/F")
oTree_b.Branch("mgg",b_mgg,"mgg/F")
oTree_b.Branch("mindphi_gg_jets",		b_mindphi_gg_jets,"mindphi_gg_jets/F")


tmvaReader_ = ROOT.TMVA.Reader()
tmvaReader_.AddVariable("Njets"  ,b_Njets)
tmvaReader_.AddVariable("Nbjets" ,b_Nbjets)
tmvaReader_.AddVariable("scalarHT",	b_scalarHT)
tmvaReader_.AddVariable("MET",		b_MET	  )
tmvaReader_.AddVariable("mindphi_gg_jets",		b_mindphi_gg_jets	 )
tmvaReader_.AddVariable("pho1_ptom",	b_pho1_ptom)
tmvaReader_.AddVariable("pho2_ptom",	b_pho2_ptom)
tmvaReader_.AddVariable("pho1_eta",	b_pho1_eta)
tmvaReader_.AddVariable("pho2_eta",	b_pho2_eta)
tmvaReader_.AddVariable("pho1_ch_isolation",	b_pho1_ch_isolation)
tmvaReader_.AddVariable("pho2_ch_isolation",	b_pho2_ch_isolation)
tmvaReader_.AddVariable("j1_pt",	b_j1_pt )
tmvaReader_.AddVariable("j1_eta",	b_j1_eta)
tmvaReader_.AddVariable("j2_pt",	b_j2_pt )
tmvaReader_.AddVariable("j2_eta",	b_j2_eta)
tmvaReader_.AddVariable("j3_pt",	b_j3_pt )
tmvaReader_.AddVariable("j3_eta",	b_j3_eta)
tmvaReader_.AddVariable("j4_pt",	b_j4_pt )
tmvaReader_.AddVariable("j4_eta",	b_j4_eta)


if runBDT : tmvaReader_.BookMVA("BDTG","weights_hadronic/TMVAClassification_BDTG.weights.xml")

def preselection(tr):

     #if tr.scalarHT < 350 : return False
     if tr.mgg < 180 and tr.mgg > 100 : return True
     return False
# here define a simple analysis (selection of cuts or whatever)

def thingsToStrings(l):
    rlist = []
    for ll in l : rlist.append(str(ll))
    return rlist
 
def doAnalysis(tr,entry,i,w):
     #print fName, fSample, fLabel 
     # override weight variable : 
     w = tr.weight_LO*L

     pt1om = tr.pho1_pT/tr.mgg
     pt2om = tr.pho2_pT/tr.mgg

     #writer.write(",".join(thingsToStrings([fName,fSample,i,fLabel,w,tr.Njets,tr.Nbjets,tr.scalarHT,tr.MET,pt1om,pt2om,abs(tr.pho1_eta),abs(tr.pho2_eta),\
     #tr.jet1_pT,abs(tr.jet1_eta),tr.jet2_pT,abs(tr.jet2_eta),tr.jet3_pT,abs(tr.jet3_eta),tr.jet4_pT,abs(tr.jet4_eta)]))+"\n")

     b_weight[0] = w
     b_Njets[0]  = tr.Njets
     b_Nbjets[0]  = tr.Nbjets
     b_scalarHT[0]	= tr.scalarHT 
     b_MET[0]      	= tr.MET
     b_pTgg[0]      	= tr.pTH_reco
     b_pho1_ptom[0]     = pt1om
     b_pho2_ptom[0]     = pt2om
     b_pho1_eta[0]      = abs(tr.pho1_eta)
     b_pho2_eta[0]      = abs(tr.pho2_eta) 
     b_j1_pt[0]		= tr.jet1_pT
     b_j1_eta[0] 	= abs(tr.jet1_eta)	
     b_j2_pt[0]		= tr.jet2_pT
     b_j2_eta[0]	= abs(tr.jet2_eta)
     b_j3_pt[0]		= tr.jet3_pT
     b_j3_eta[0]	= abs(tr.jet3_eta)
     b_mgg[0]		= tr.mgg
     b_pho1_ch_isolation[0]	= tr.pho1_IsolationVar
     b_pho2_ch_isolation[0]	= tr.pho2_IsolationVar

     if tr.jet4_pT < 0:
       b_j4_pt[0]	= -999
       b_j4_eta[0]	= -999
       
     else:
       b_j4_pt[0]	= tr.jet4_pT
       b_j4_eta[0]	= abs(tr.jet4_eta)


     # look for difference between higgs and closest jet ?
     photon_1 = ROOT.TLorentzVector(); photon_1.SetPtEtaPhiE(tr.pho1_pT,tr.pho1_eta,tr.pho1_phi,tr.pho1_E)
     photon_2 = ROOT.TLorentzVector(); photon_2.SetPtEtaPhiE(tr.pho2_pT,tr.pho2_eta,tr.pho2_phi,tr.pho2_E)

     diphoton = photon_1+photon_2;
     mindelphi = 999.
     for ji in range(1,5): 
       if getattr(tr,"jet%d_pT"%ji) < 0: continue 
       jet_p4 = ROOT.TLorentzVector()
       jet_p4.SetPtEtaPhiM(getattr(tr,"jet%d_pT"%ji),getattr(tr,"jet%d_eta"%ji),getattr(tr,"jet%d_phi"%ji),getattr(tr,"jet%d_mass"%ji))
       
       dphi = diphoton.DeltaPhi(jet_p4)
       if abs(dphi)<mindelphi: mindelphi = abs(dphi)


     b_mindphi_gg_jets[0] = mindelphi

     if runBDT: bdtg = tmvaReader_.EvaluateMVA("BDTG") 
     else:  bdtg = -999.
     b_BDT[0]		= bdtg


     # And fill the tree, only use ttH and TH in the signal, the rest are backgrounds! 
     if fSample in ["ttH","tH"]: oTree_s.Fill()
     else:  oTree_b.Fill()

     variables["mgg"][entry][i].Fill(tr.mgg,w)

     # bins 
     ptHiggs = tr.pTH_reco
     ev_mgg  = tr.mgg
     if   (ptHiggs < 50): variables["mgg_pt_0_50"][entry][i].Fill(ev_mgg,w)
     elif (ptHiggs < 100): variables["mgg_pt_50_100"][entry][i].Fill(ev_mgg,w)
     elif (ptHiggs < 150): variables["mgg_pt_100_150"][entry][i].Fill(ev_mgg,w)
     elif (ptHiggs < 250): variables["mgg_pt_150_250"][entry][i].Fill(ev_mgg,w)
     else: variables["mgg_pt_250"][entry][i].Fill(ev_mgg,w)

     variables["Njets"][entry][i].Fill(tr.Njets,w)
     variables["Nbjets"][entry][i].Fill(tr.Nbjets,w)
     variables["MET"][entry][i].Fill(tr.MET,w)
     variables["scalarHT"][entry][i].Fill(tr.scalarHT,w)
     variables["pTH_reco"][entry][i].Fill(tr.pTH_reco,w)

     variables["pho1_pT"][entry][i].Fill(tr.pho1_pT,w)
     variables["pho2_pT"][entry][i].Fill(tr.pho2_pT,w)
     variables["pho1_pTom"][entry][i].Fill(pt1om,w)
     variables["pho2_pTom"][entry][i].Fill(pt2om,w)
     variables["pho1_ch_isolation"][entry][i].Fill(tr.pho1_IsolationVar,w)
     variables["pho2_ch_isolation"][entry][i].Fill(tr.pho2_IsolationVar,w)
     variables["jet1_pT"][entry][i].Fill(tr.jet1_pT,w)
     variables["jet2_pT"][entry][i].Fill(tr.jet2_pT,w)
     variables["jet3_pT"][entry][i].Fill(tr.jet3_pT,w)
     variables["jet4_pT"][entry][i].Fill(tr.jet4_pT,w)
     
     variables["pho1_eta"][entry][i].Fill(abs(tr.pho1_eta),w)
     variables["pho2_eta"][entry][i].Fill(abs(tr.pho2_eta),w)
     variables["jet1_eta"][entry][i].Fill(abs(tr.jet1_eta),w)
     variables["jet2_eta"][entry][i].Fill(abs(tr.jet2_eta),w)
     variables["jet3_eta"][entry][i].Fill(abs(tr.jet3_eta),w)
     if tr.jet4_pT < 0:  variables["jet4_eta"][entry][i].Fill(-999,w)
     else: variables["jet4_eta"][entry][i].Fill(abs(tr.jet4_eta),w)

     variables["bdt_class"][entry][i].Fill(bdtg,w)
     variables["mindphi_gg_jets"][entry][i].Fill(mindelphi,w)

     return w 
     # can also do the delta phi between the photons and the two lead jets?

