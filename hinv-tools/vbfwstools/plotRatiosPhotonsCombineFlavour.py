import array
import ROOT 

class TFValidator: 
 def __init__(self,input_ws_file,fit_file):

  self.fiws = ROOT.TFile.Open(input_ws_file)
  self.workspace = self.fiws.Get("w")
  
  self.fit_file = ROOT.TFile.Open(fit_file)

  self.r = ROOT.TRandom3()
  self.nbins=9 

  self.ntoys = 1000

  self.cat = "MTR_2017"
  self.PProc = "photon"
  self.PR = "photon"
  self.year = "2017"

 def AddTGraphs(self,g1,g2):
  
  print "Trying to add graph", g1.GetName(), " to ", g2.GetName()
  up = array.array('d',[0])
  dn = array.array('d',[0])

  for p in range(g1.GetN()):
    y2 = g2.GetY()[p]
    
    x  = g1.GetX()[p]
    y1 = g1.GetY()[p]

    xeu = g1.GetErrorXhigh(p)
    xel = g1.GetErrorXlow(p)

    bw      = xel+xeu
    central = (y1+y2)*bw
    
    g1.SetPoint(p,x,central/bw)
    
    ROOT.RooHistError.instance().getPoissonInterval(int(central),dn,up,1)
    uE = up[0]-central
    dE = central-dn[0]

    g1.SetPointError(p,xel,xeu,dE/bw,uE/bw)

 def calcR(self,b):
  zq_ee = self.workspace.function("%s_QCDV_Zee_bin%d"%(self.cat,b)).getVal()
  ze_ee = self.workspace.function("%s_EWKV_Zee_bin%d"%(self.cat,b)).getVal()
  zq_mm = self.workspace.function("%s_QCDV_Zmumu_bin%d"%(self.cat,b)).getVal()
  ze_mm = self.workspace.function("%s_EWKV_Zmumu_bin%d"%(self.cat,b)).getVal()

  pq = self.workspace.function("pmu_cat_vbf_%s_qcd_zjets_ch_qcd_%s_bin%d"%(self.year,self.PProc,b)).getVal()
  pe = self.workspace.function("pmu_cat_vbf_%s_ewk_zjets_ch_ewk_%s_bin%d"%(self.year,self.PProc,b)).getVal()

  #print "%sQCDV_Z%s_bin%d"%(self.cat,self.ZProc,b), "%sQCDV_W%s_bin%d"%(self.cat,self.WProc,b)
  return (pe+pq)/(ze_ee+zq_ee+zq_mm+ze_mm)


 def returnRMS(self,b,includeStat=False, includeAll=False): 

  r2=0
  mean=0 
  
  allpars   = self.workspace.function("%s_QCDV_Zee_bin%d"%(self.cat,b)).getParameters(ROOT.RooArgSet())
  allpars2  = self.workspace.function("%s_EWKV_Zee_bin%d"%(self.cat,b)).getParameters(ROOT.RooArgSet())
  allpars2a = self.workspace.function("%s_QCDV_Zmumu_bin%d"%(self.cat,b)).getParameters(ROOT.RooArgSet())
  allpars2b = self.workspace.function("%s_EWKV_Zmumu_bin%d"%(self.cat,b)).getParameters(ROOT.RooArgSet())
  allpars3 = self.workspace.function("pmu_cat_vbf_%s_qcd_zjets_ch_qcd_%s_bin%d"%(self.year,self.PProc,b)).getParameters(ROOT.RooArgSet())
  allpars4 = self.workspace.function("pmu_cat_vbf_%s_ewk_zjets_ch_ewk_%s_bin%d"%(self.year,self.PProc,b)).getParameters(ROOT.RooArgSet())
  
  allpars.add(allpars2)
  allpars.add(allpars2a)
  allpars.add(allpars2b)
  allpars.add(allpars3)
  allpars.add(allpars4)
  
  c = ROOT.TCanvas()
  rwzcental = self.calcR(b)
  hist = ROOT.TH1F("histo","",50,0.75*rwzcental,1.25*rwzcental)
  
  SRCAT = "" 
  if   "MTRC" in self.cat :SRCAT = "MTRC_" 
  elif "VTRC" in self.cat :SRCAT = "VTRC_" 
  elif "MTRF" in self.cat :SRCAT = "MTRF_" 
  elif "VTRF" in self.cat :SRCAT = "VTRF_" 
  elif "MTR" in self.cat  :SRCAT  = "MTR_"
  elif "VTR" in self.cat  :SRCAT  = "VTR_" 

  list_of_parameters = []
  vetonames = ["wzCR","singleelectron","dielectron","singlemuon","ewkqcdzCR","dimuon","TR_fnlo_SF","pmu_","sfactor_","W_SR_freebin"]
  for t in range(self.ntoys): 

    if includeAll: 
      iter = allpars.createIterator()
      while 1:
       tpar = iter.Next() # allpars.at(n)
       if tpar == None : break
       if "QCDZ_SR_bin" in tpar.GetName() : continue
       # not even sure of these 2 but they are constant at least 
       if "TF_syst_fnlo_SF" in tpar.GetName(): continue 
       if "ewkqcdratio_stat" in tpar.GetName(): continue 
       veto = False
       for v in vetonames: 
         if v in tpar.GetName(): 
	 	veto=True 
		break
       if veto: continue 
       self.workspace.var(tpar.GetName()).setVal(self.r.Gaus(0,1))
       list_of_parameters.append(tpar.GetName())

  
    else:
      self.workspace.var("Photon_QCD_facscale_vbf").setVal(self.r.Gaus(0,1))
      self.workspace.var("Photon_QCD_renscale_vbf").setVal(self.r.Gaus(0,1))
      self.workspace.var("Photon_QCD_pdf_vbf").setVal(self.r.Gaus(0,1))
      self.workspace.var("qcd_photon_ewk_vbf_bin%d"%(b-1)).setVal(self.r.Gaus(0,1))
      self.workspace.var("Photon_EWK_facscale_vbf").setVal(self.r.Gaus(0,1))
      self.workspace.var("Photon_EWK_renscale_vbf").setVal(self.r.Gaus(0,1))
      self.workspace.var("Photon_EWK_pdf_vbf").setVal(self.r.Gaus(0,1))
      self.workspace.var("ewkphoton_ewk_vbf_bin%d"%(b-1)).setVal(self.r.Gaus(0,1))
      list_of_parameters.append("Photon_QCD_facscale_vbf")   
      list_of_parameters.append("Photon_QCD_renscale_vbf")   
      list_of_parameters.append("Photon_QCD_pdf_vbf")   
      list_of_parameters.append("Photon_EWK_facscale_vbf")   
      list_of_parameters.append("Photon_EWK_renscale_vbf")   
      list_of_parameters.append("Photon_EWK_pdf_vbf")   
      list_of_parameters.append("qcd_photon_ewk_vbf_bin%d"%(b-1))   
      list_of_parameters.append("ewkphoton_ewk_vbf_bin%d"%(b-1))   

      if (includeStat):
	self.workspace.var("vbf_%s_stat_error_ewk_photonCR_bin%d"%(self.year,b-1)).setVal(self.r.Gaus(0,1))
	self.workspace.var("vbf_%s_stat_error_qcd_photonCR_bin%d"%(self.year,b-1)).setVal(self.r.Gaus(0,1))
	list_of_parameters.append("vbf_%s_stat_error_ewk_photonCR_bin%d"%(self.year,b-1))	
	list_of_parameters.append("vbf_%s_stat_error_qcd_photonCR_bin%d"%(self.year,b-1))	

    
    rwz = self.calcR(b)
    hist.Fill(rwz)
    r2   += rwz*rwz
    mean += rwz

  mean /=self.ntoys 
  rms = (r2/self.ntoys - mean*mean)**0.5
    
  if includeAll: 
      iter = allpars.createIterator()
      while 1:
       tpar = iter.Next() # allpars.at(n)
       if tpar == None : break
       if "QCDZ_SR_bin" in tpar.GetName() : continue
       # not even sure of these 2 but they are constant at least 
       if "TF_syst_fnlo_SF" in tpar.GetName(): continue 
       if "ewkqcdratio_stat" in tpar.GetName(): continue 
       veto = False
       for v in vetonames: 
         if v in tpar.GetName(): 
	 	veto=True 
		break
       if veto: continue 
       self.workspace.var(tpar.GetName()).setVal(0)
  else:
      self.workspace.var("Photon_QCD_facscale_vbf").setVal(0)
      self.workspace.var("Photon_QCD_renscale_vbf").setVal(0)
      self.workspace.var("Photon_QCD_pdf_vbf").setVal(0)
      self.workspace.var("qcd_photon_ewk_vbf_bin%d"%(b-1)).setVal(0)
      self.workspace.var("Photon_EWK_facscale_vbf").setVal(0)
      self.workspace.var("Photon_EWK_renscale_vbf").setVal(0)
      self.workspace.var("Photon_EWK_pdf_vbf").setVal(0)
      self.workspace.var("ewkphoton_ewk_vbf_bin%d"%(b-1)).setVal(0)
    
      if (includeStat):
	self.workspace.var("vbf_%s_stat_error_ewk_photonCR_bin%d"%(self.year,b-1)).setVal(0)
	self.workspace.var("vbf_%s_stat_error_qcd_photonCR_bin%d"%(self.year,b-1)).setVal(0)

  hist.Draw()
  hist.Fit("gaus")
  #c.SaveAs("bin%d.pdf"%b)
  return rms,  list_of_parameters


 def calcRdata(self,b):

  data_Z = self.fit_file.Get("shapes_prefit/%s_ZEE/data"%(self.cat))
  self.AddTGraphs(data_Z,self.fit_file.Get("shapes_prefit/%s_ZMUMU/data"%(self.cat)))
  Zd     = data_Z.GetY()[b-1]
  Zeu     = data_Z.GetErrorYhigh(b-1)
  Zed     = data_Z.GetErrorYlow(b-1)
  
  data_P = self.fit_file.Get("shapes_prefit/photon_cr_%s/data"%(self.year))
  Pd     = data_P.GetY()[b-1]
  Peu     = data_P.GetErrorYhigh(b-1)
  Ped     = data_P.GetErrorYlow(b-1)

  # Remove the backgrounds!
  TT_Z  = self.fit_file.Get("shapes_prefit/%s_ZEE/TOP"%(self.cat))
  TT_Z.Add(self.fit_file.Get("shapes_prefit/%s_ZMUMU/TOP"%(self.cat)))
  ttZ_d = TT_Z.GetBinContent(b)
  VV_Z  = self.fit_file.Get("shapes_prefit/%s_ZEE/VV"%(self.cat))
  VV_Z.Add(self.fit_file.Get("shapes_prefit/%s_ZMUMU/VV"%(self.cat)))
  VVZ_d = VV_Z.GetBinContent(b)

  
  # Remove the backgrounds!
  QCD_P  = self.fit_file.Get("shapes_prefit/photon_cr_%s/qcd"%(self.year))
  QCD_d = QCD_P.GetBinContent(b)

  Pd -= (QCD_d)
  Zd -= (ttZ_d+VVZ_d)
  
  rpz = Pd/Zd
  rpz_eu = abs(rpz) * ( ( (Zeu/Zd)**2 + (Peu/Pd)**2)**0.5 )
  rpz_ed = abs(rpz) * ( ( (Zed/Zd)**2 + (Ped/Pd)**2)**0.5 )

  return rpz, rpz_ed, rpz_eu

 
 


