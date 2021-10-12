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
  self.ZProc = "mumu"
  self.WProc = "munu"
  self.ZR = "MUMU"
  self.WR = "MUNU"
  
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

 def calcR(self,b):

  zq = self.workspace.function("%s_QCDV_Z%s_bin%d"%(self.cat,self.ZProc,b)).getVal()
  ze = self.workspace.function("%s_EWKV_Z%s_bin%d"%(self.cat,self.ZProc,b)).getVal()
  wq = self.workspace.function("%s_QCDV_W%s_bin%d"%(self.cat,self.WProc,b)).getVal()
  we = self.workspace.function("%s_EWKV_W%s_bin%d"%(self.cat,self.WProc,b)).getVal()

  #print "%sQCDV_Z%s_bin%d"%(self.cat,self.ZProc,b), "%sQCDV_W%s_bin%d"%(self.cat,self.WProc,b)
  return (ze+zq)/(we+wq)


 def returnRMS(self,b,includeStat=False, includeAll=False): 

  r2=0
  mean=0 
  
  allpars  = self.workspace.function("%s_QCDV_W%s_bin%d"%(self.cat,self.WProc,b)).getParameters(ROOT.RooArgSet())
  allpars2 = self.workspace.function("%s_EWKV_W%s_bin%d"%(self.cat,self.WProc,b)).getParameters(ROOT.RooArgSet())
  allpars.add(allpars2)
  
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


 def calcRdata(self,b):

  print "shapes_prefit/%s_Z%s/data"%(self.cat,self.ZR)
  data_Z = self.fit_file.Get("shapes_prefit/%s_Z%s/data"%(self.cat,self.ZR))
  Zd     = data_Z.GetY()[b-1]
  Zeu     = data_Z.GetErrorYhigh(b-1)
  Zed     = data_Z.GetErrorYlow(b-1)
  
  data_W = self.fit_file.Get("shapes_prefit/%s_W%s/data"%(self.cat,self.WR))
  Wd     = data_W.GetY()[b-1]
  Weu     = data_W.GetErrorYhigh(b-1)
  Wed     = data_W.GetErrorYlow(b-1)

  backgrounds_ZR = ["TOP","VV","EWKW","WJETS"]
  backgrounds_WR = ["TOP","VV","QCD","EWKZll","DY"]

  backgroundZ  = (self.fit_file.Get("shapes_prefit/%s_Z%s/%s"%(self.cat,self.ZR,backgrounds_ZR[0]))).GetBinContent(b)
  for bkg in backgrounds_ZR[1:]:
    backgroundZ_h = self.fit_file.Get("shapes_prefit/%s_Z%s/%s"%(self.cat,self.ZR,bkg))
    try : 
      backgroundZ += backgroundZ_h.GetBinContent(b)
    except: 
      pass 

  backgroundW  = (self.fit_file.Get("shapes_prefit/%s_W%s/%s"%(self.cat,self.WR,backgrounds_WR[0]))).GetBinContent(b)

  for bkg in backgrounds_WR[1:]:
    backgroundW_h = (self.fit_file.Get("shapes_prefit/%s_W%s/%s"%(self.cat,self.WR,bkg)))
    try:
      backgroundW += backgroundW_h.GetBinContent(b)
    except:
      pass

  Wd -= (backgroundW)
  Zd -= (backgroundZ)
  
  rwz = Zd/Wd
  rwz_eu = abs(rwz) * ( ( (Zeu/Zd)**2 + (Weu/Wd)**2)**0.5 )
  rwz_ed = abs(rwz) * ( ( (Zed/Zd)**2 + (Wed/Wd)**2)**0.5 )

  return rwz, rwz_ed, rwz_eu

 
 


