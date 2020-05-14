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

 def calcR(self,b):

  zq = self.workspace.function("%sQCDV_Z%s_bin%d"%(self.cat,self.ZProc,b)).getVal()
  ze = self.workspace.function("%sEWKV_Z%s_bin%d"%(self.cat,self.ZProc,b)).getVal()
  wq = self.workspace.function("%sQCDV_W%s_bin%d"%(self.cat,self.WProc,b)).getVal()
  we = self.workspace.function("%sEWKV_W%s_bin%d"%(self.cat,self.WProc,b)).getVal()

  #print "%sQCDV_Z%s_bin%d"%(self.cat,self.ZProc,b), "%sQCDV_W%s_bin%d"%(self.cat,self.WProc,b)
  return (ze+zq)/(we+wq)


 def returnRMS(self,b,includeStat=False, includeAll=False): 

  r2=0
  mean=0 
  
  allpars  = self.workspace.function("%sQCDV_W%s_bin%d"%(self.cat,self.WProc,b)).getParameters(ROOT.RooArgSet())
  allpars2 = self.workspace.function("%sEWKV_W%s_bin%d"%(self.cat,self.WProc,b)).getParameters(ROOT.RooArgSet())
  allpars.add(allpars2)
  
  c = ROOT.TCanvas()
  rwzcental = self.calcR(b)
  hist = ROOT.TH1F("histo","",50,0.75*rwzcental,1.25*rwzcental)
  SRCAT = "MTR_" if "MTR" in self.cat else "VTR_" 
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
       self.workspace.var(tpar.GetName()).setVal(self.r.Gaus(0,1))

  
    else:
      self.workspace.var("%sQCDwzratioQCDcorrSyst_pdf"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sQCDwzratioQCDcorrSyst_muF"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sQCDwzratioQCDcorrSyst_muR"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sQCDwzratio_EWK_corr_on_Strong_bin%d"%(SRCAT,b)).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sEWKwzratioQCDcorrSyst_pdf"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sEWKwzratioQCDcorrSyst_muF"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sEWKwzratioQCDcorrSyst_muR"%SRCAT).setVal(self.r.Gaus(0,1))
      self.workspace.var("%sEWKwzratio_EWK_corr_on_Strong_bin%d"%(SRCAT,b)).setVal(self.r.Gaus(0,1))
   

      if (includeStat):
        self.workspace.var("%sQCDwzratio_stat_bin%d"%(self.cat,b)).setVal(self.r.Gaus(0,1))
        self.workspace.var("%sEWKwzratio_stat_bin%d"%(self.cat,b)).setVal(self.r.Gaus(0,1))

    
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
      self.workspace.var("%sQCDwzratio_stat_bin%d"%(self.cat,b)).setVal(0)
      self.workspace.var("%sEWKwzratio_stat_bin%d"%(self.cat,b)).setVal(0)

  hist.Draw()
  hist.Fit("gaus")
  c.SaveAs("bin%d.pdf"%b)
  return rms 


 def calcRdata(self,b):

  data_Z = self.fit_file.Get("shapes_prefit/Z%s/data"%self.ZR)
  Zd     = data_Z.GetY()[b-1]
  Ze     = 0.5*(data_Z.GetErrorYhigh(b-1)+data_Z.GetErrorYlow(b-1))
  
  data_W = self.fit_file.Get("shapes_prefit/W%s/data"%self.WR)
  Wd     = data_W.GetY()[b-1]
  We     = 0.5*(data_W.GetErrorYhigh(b-1)+data_W.GetErrorYlow(b-1))

  # Remove the backgrounds!
  TT_Z  = self.fit_file.Get("shapes_prefit/Z%s/TOP"%self.ZR)
  ttZ_d = TT_Z.GetBinContent(b)
  VV_Z  = self.fit_file.Get("shapes_prefit/Z%s/VV"%self.ZR)
  VVZ_d = VV_Z.GetBinContent(b)
  
  # Remove the backgrounds!
  TT_W  = self.fit_file.Get("shapes_prefit/W%s/TOP"%self.WR)
  ttW_d = TT_W.GetBinContent(b)
  VV_W  = self.fit_file.Get("shapes_prefit/W%s/VV"%self.WR)
  VVW_d = VV_W.GetBinContent(b)
  EZll_W  = self.fit_file.Get("shapes_prefit/W%s/EWKZll"%self.WR)
  EZllW_d = EZll_W.GetBinContent(b)
  QZll_W  = self.fit_file.Get("shapes_prefit/W%s/DY"%self.WR)
  QZllW_d = QZll_W.GetBinContent(b)

  Wd -= (ttW_d+VVW_d+EZllW_d+QZllW_d)
  Zd -= (ttZ_d+VVZ_d)
  
  rwz = Zd/Wd
  rwz_e = rwz * ( ( (Ze/Zd)**2 + (We/Wd)**2)**0.5 )

  return rwz, rwz_e

 
 


