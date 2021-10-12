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
  self.year = "2017"

 def setPostFit(self,b):

  fit_res = self.fit_file.Get("fit_b")
  floatingpars = fit_res.floatParsFinal()

  vetonames = ["QCDZ_SR_bin","TF_syst_fnlo_SF","ewkqcdratio_stat","TR_fnlo_SF","NLOSF_","W_SR_freebin"]
  allpars = self.workspace.allVars()
  iter = allpars.createIterator()
  while 1: 
   tpar = iter.Next() # allpars.at(n)
   if tpar == None : break
   pn = tpar.GetName()
       
   veto = False
   for v in vetonames: 
     if v in tpar.GetName(): 
     	veto=True 
    	break
   if veto: continue 
   
   fitval = floatingpars.find(pn)
   if fitval == None: continue 
   bf = fitval.getVal()
   self.workspace.var(pn).setVal(bf)
   print "Setting default Parameter value ", pn,bf
  

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
    print "Values are -> ", y1,  y2, central/bw,dE/bw,uE/bw

 def calcR(self,b):

  zq_ee = self.workspace.function("%s_QCDV_Zee_bin%d"%(self.cat,b)).getVal()
  ze_ee = self.workspace.function("%s_EWKV_Zee_bin%d"%(self.cat,b)).getVal()
  zq_mm = self.workspace.function("%s_QCDV_Zmumu_bin%d"%(self.cat,b)).getVal()
  ze_mm = self.workspace.function("%s_EWKV_Zmumu_bin%d"%(self.cat,b)).getVal()
  wq_e  = self.workspace.function("%s_QCDV_Wenu_bin%d"%(self.cat,b)).getVal()
  we_e  = self.workspace.function("%s_EWKV_Wenu_bin%d"%(self.cat,b)).getVal()
  wq_m  = self.workspace.function("%s_QCDV_Wmunu_bin%d"%(self.cat,b)).getVal()
  we_m  = self.workspace.function("%s_EWKV_Wmunu_bin%d"%(self.cat,b)).getVal()

  #print "%sQCDV_Z%s_bin%d"%(self.cat,self.ZProc,b), "%sQCDV_W%s_bin%d"%(self.cat,self.WProc,b)
  return (ze_ee+zq_ee+ze_mm+zq_mm)/(we_e+wq_e+we_m+wq_m)
 
 """
 def calcRPostFit(self,b):

  zq_ee = self.workspace.function("%s_QCDV_Zee_bin%d"%(self.cat,b)).getVal()
  ze_ee = self.workspace.function("%s_EWKV_Zee_bin%d"%(self.cat,b)).getVal()
  zq_mm = self.workspace.function("%s_QCDV_Zmumu_bin%d"%(self.cat,b)).getVal()
  ze_mm = self.workspace.function("%s_EWKV_Zmumu_bin%d"%(self.cat,b)).getVal()
  wq_e  = self.workspace.function("%s_QCDV_Wenu_bin%d"%(self.cat,b)).getVal()
  we_e  = self.workspace.function("%s_EWKV_Wenu_bin%d"%(self.cat,b)).getVal()
  wq_m  = self.workspace.function("%s_QCDV_Wmunu_bin%d"%(self.cat,b)).getVal()
  we_m  = self.workspace.function("%s_EWKV_Wmunu_bin%d"%(self.cat,b)).getVal()

  #print "%sQCDV_Z%s_bin%d"%(self.cat,self.ZProc,b), "%sQCDV_W%s_bin%d"%(self.cat,self.WProc,b)
  return (ze_ee+zq_ee+ze_mm+zq_mm)/(we_e+wq_e+we_m+wq_m)

 """

 def returnRMS(self,b,includeStat=False, includeAll=False): 

  r2=0
  mean=0 
  
  allpars  = self.workspace.function("%s_QCDV_Wenu_bin%d"%(self.cat,b)).getParameters(ROOT.RooArgSet())
  allpars2 = self.workspace.function("%s_EWKV_Wenu_bin%d"%(self.cat,b)).getParameters(ROOT.RooArgSet())
  allpars3 = self.workspace.function("%s_QCDV_Wmunu_bin%d"%(self.cat,b)).getParameters(ROOT.RooArgSet())
  allpars4 = self.workspace.function("%s_EWKV_Wmunu_bin%d"%(self.cat,b)).getParameters(ROOT.RooArgSet())
  allpars.add(allpars2)
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
  
  vetonames = ["QCDZ_SR_bin","TF_syst_fnlo_SF","ewkqcdratio_stat","TR_fnlo_SF","NLOSF_","W_SR_freebin"]

  print " here are the things ", 
  print SRCAT
  print self.cat 
  for t in range(self.ntoys): 

    if includeAll: 
      iter = allpars.createIterator()
      while 1:
       tpar = iter.Next() # allpars.at(n)
       if tpar == None : break
       
       veto = False
       for v in vetonames: 
         if v in tpar.GetName(): 
	 	veto=True 
		break
       if veto: continue 
       
       self.workspace.var(tpar.GetName()).setVal(self.r.Gaus(0,1))
       list_of_parameters.append(tpar.GetName())

  
    else:
      self.workspace.var("%sQCDwzratioQCDcorrSyst_pdf"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sQCDwzratioQCDcorrSyst_muF"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sQCDwzratioQCDcorrSyst_muR"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sQCDwzratio_EWK_corr_on_Strong_bin%d"%(SRCAT,b)).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sEWKwzratioQCDcorrSyst_pdf"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sEWKwzratioQCDcorrSyst_muF"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sEWKwzratioQCDcorrSyst_muR"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sEWKwzratio_EWK_corr_on_Strong_bin%d"%(SRCAT,b)).setVal(self.r.Gaus(0,1))
      list_of_parameters.append("%sQCDwzratioQCDcorrSyst_pdf"%SRCAT)
      list_of_parameters.append("%sQCDwzratioQCDcorrSyst_muF"%SRCAT)
      list_of_parameters.append("%sQCDwzratioQCDcorrSyst_muR"%SRCAT)
      list_of_parameters.append("%sQCDwzratio_EWK_corr_on_Strong_biin%d"%(SRCAT,b))
      list_of_parameters.append("%sEWKwzratioQCDcorrSyst_pdf"%SRCAT)
      list_of_parameters.append("%sEWKwzratioQCDcorrSyst_muF"%SRCAT)
      list_of_parameters.append("%sEWKwzratioQCDcorrSyst_muR"%SRCAT)
      list_of_parameters.append("%sEWKwzratio_EWK_corr_on_Strong_bin%d"%(SRCAT,b))
   

      if (includeStat):
        self.workspace.var("%s_QCDwzratio_stat_bin%d"%(self.cat,b)).setVal(self.r.Gaus(0,1))
        self.workspace.var("%s_EWKwzratio_stat_bin%d"%(self.cat,b)).setVal(self.r.Gaus(0,1))
        list_of_parameters.append("%s_QCDwzratio_stat_bin%d"%(self.cat,b))
        list_of_parameters.append("%s_EWKwzratio_stat_bin%d"%(self.cat,b))

    
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
       veto = False
       for v in vetonames: 
         if v in tpar.GetName(): 
           veto=True 
           break
       if veto: continue 
       self.workspace.var(tpar.GetName()).setVal(0)
  else:
    self.workspace.var("%sQCDwzratioQCDcorrSyst_pdf"%SRCAT).setVal(0)
    self.workspace.var("%sQCDwzratioQCDcorrSyst_muF"%SRCAT).setVal(0)
    self.workspace.var("%sQCDwzratioQCDcorrSyst_muR"%SRCAT).setVal(0)
    self.workspace.var("%sQCDwzratio_EWK_corr_on_Strong_bin%d"%(SRCAT,b)).setVal(0)

    self.workspace.var("%sEWKwzratioQCDcorrSyst_pdf"%SRCAT).setVal(0)
    self.workspace.var("%sEWKwzratioQCDcorrSyst_muF"%SRCAT).setVal(0)
    self.workspace.var("%sEWKwzratioQCDcorrSyst_muR"%SRCAT).setVal(0)
    self.workspace.var("%sEWKwzratio_EWK_corr_on_Strong_bin%d"%(SRCAT,b)).setVal(0)
    
    if (includeStat):
      self.workspace.var("%s_QCDwzratio_stat_bin%d"%(self.cat,b)).setVal(0)
      self.workspace.var("%s_EWKwzratio_stat_bin%d"%(self.cat,b)).setVal(0)

  hist.Draw()
  hist.Fit("gaus")
  #c.SaveAs("bin%d.pdf"%b)
  return rms, list_of_parameters

 def setup(self):
  self.data_Z = self.fit_file.Get("shapes_prefit/%s_ZEE/data"%(self.cat))
  self.AddTGraphs(self.data_Z,self.fit_file.Get("shapes_prefit/%s_ZMUMU/data"%(self.cat)))

  self.data_W = self.fit_file.Get("shapes_prefit/%s_WENU/data"%(self.cat))
  self.AddTGraphs(self.data_W,self.fit_file.Get("shapes_prefit/%s_WMUNU/data"%(self.cat)))

  backgrounds_ZR = ["TOP","VV","EWKW","WJETS"]
  backgrounds_WR = ["TOP","VV","QCD","EWKZll","DY"]


  self.backgroundZ = self.fit_file.Get("shapes_prefit/%s_ZEE/%s"%(self.cat,backgrounds_ZR[0]))
  self.backgroundW = self.fit_file.Get("shapes_prefit/%s_WENU/%s"%(self.cat,backgrounds_WR[0]))

  for ibg,bkg in enumerate(backgrounds_ZR): 
    if ibg==0:
      tadd = self.fit_file.Get("shapes_prefit/%s_ZMUMU/%s"%(self.cat,backgrounds_ZR[0]))
      try:
        self.backgroundZ.Add(tadd)
      except:  
        pass 
    else: 
      tadd = self.fit_file.Get("shapes_prefit/%s_ZEE/%s"%(self.cat,bkg))
      try :
         self.backgroundZ.Add(tadd)
      except : 
         pass 
      tadd2 = self.fit_file.Get("shapes_prefit/%s_ZMUMU/%s"%(self.cat,bkg))
      try :
         self.backgroundZ.Add(tadd2)
      except : 
         pass 
  
  for ibg,bkg in enumerate(backgrounds_WR): 
    if ibg==0:
      tadd = self.fit_file.Get("shapes_prefit/%s_WMUNU/%s"%(self.cat,backgrounds_WR[0]))
      try:
        self.backgroundW.Add(tadd)
      except:  
        pass 
    else: 
      tadd = self.fit_file.Get("shapes_prefit/%s_WENU/%s"%(self.cat,bkg))
      try :
         self.backgroundW.Add(tadd)
      except : 
         pass 
      tadd2 = self.fit_file.Get("shapes_prefit/%s_WMUNU/%s"%(self.cat,bkg))
      try :
         self.backgroundW.Add(tadd2)
      except : 
         pass 
         

 def calcRdata(self,b):


  Zd     = self.data_Z.GetY()[b-1]
  Zeu     = self.data_Z.GetErrorYhigh(b-1)
  Zed     = self.data_Z.GetErrorYlow(b-1)
  

  Wd     = self.data_W.GetY()[b-1]
  Weu     = self.data_W.GetErrorYhigh(b-1)
  Wed     = self.data_W.GetErrorYlow(b-1)

  # Remove the backgrounds!

  bZ_d = self.backgroundZ.GetBinContent(b)
  bW_d = self.backgroundW.GetBinContent(b)

  Wd -= (bW_d)
  Zd -= (bZ_d)
  
  rwz = Zd/Wd
  rwz_eu = abs(rwz) * ( ( (Zeu/Zd)**2 + (Weu/Wd)**2)**0.5 )
  rwz_ed = abs(rwz) * ( ( (Zed/Zd)**2 + (Wed/Wd)**2)**0.5 )

  return rwz, rwz_ed, rwz_eu

 
 


