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

  zq = self.workspace.function("%s_QCDV_%s_bin%d"%(self.cat,self.ZProc,b)).getVal()
  ze = self.workspace.function("%s_EWKV_%s_bin%d"%(self.cat,self.ZProc,b)).getVal()
  wq = self.workspace.function("%s_QCDV_%s_bin%d"%(self.cat,self.WProc,b)).getVal()
  we = self.workspace.function("%s_EWKV_%s_bin%d"%(self.cat,self.WProc,b)).getVal()

  return (ze+zq)/(we+wq)


 def returnRMS(self,b,includeStat=False): 

  r2=0
  mean=0 
 
  allpars  = self.workspace.function("%s_QCDV_%s_bin%d"%(self.cat,self.ZProc,b)).getParameters(ROOT.RooArgSet())
  allpars2 = self.workspace.function("%s_EWKV_%s_bin%d"%(self.cat,self.ZProc,b)).getParameters(ROOT.RooArgSet())
  allpars.add(allpars2)

  npar = allpars.getSize()

  vetonames = ["QCDZ_SR_bin","TF_syst_fnlo_SF","ewkqcdratio_stat","TR_fnlo_SF","NLOSF_","W_SR_freebin"]
  collactedParams = []  
  for t in range(self.ntoys): 

    #for n in range(npar): 
    iter = allpars.createIterator()
    while 1:
     tpar = iter.Next() # allpars.at(n)
     if tpar == None : break
	
     # ignore nonsense
     veto = False
     for v in vetonames: 
       if v in tpar.GetName(): 
       	veto=True 
      	break
     if veto: continue 
     # ignore theory uncertainties - also of course, ignore scale factors (float params)
     # not even sure of the first 2 but they are constant at least

     if "QCDwzratioQCDcorrSyst" in tpar.GetName(): continue 
     if "EWKwzratioQCDcorrSyst" in tpar.GetName(): continue 
     if "QCDwzratio_EWK_corr_on_Strong" in tpar.GetName(): continue 
     if "EWKwzratio_EWK_corr_on_Strong_bin" in tpar.GetName(): continue 
     if "QCDwzratio_stat_bin" in tpar.GetName(): continue
     if "EWKwzratio_stat_bin" in tpar.GetName(): continue
     
     if t==0: collactedParams.append(tpar.GetName())
     self.workspace.var(tpar.GetName()).setVal(self.r.Gaus(0,1))
    
    rwz = self.calcR(b)
    #print rwz
    r2   += rwz*rwz
    mean += rwz

  mean /=self.ntoys 
  rms = (r2/self.ntoys - mean*mean)**0.5
   
  #print " Parameters for ", self.cat, self.ZProc, " -> "
  #for p in collactedParams: print p
  #print " ---------------------------------------------"
  # Reset
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

   if "QCDwzratioQCDcorrSyst" in tpar.GetName(): continue 
   if "EWKwzratioQCDcorrSyst" in tpar.GetName(): continue 
   if "QCDwzratio_EWK_corr_on_Strong" in tpar.GetName(): continue 
   if "EWKwzratio_EWK_corr_on_Strong_bin" in tpar.GetName(): continue 
   if "QCDwzratio_stat_bin" in tpar.GetName(): continue
   if "EWKwzratio_stat_bin" in tpar.GetName(): continue
   
   self.workspace.var(tpar.GetName()).setVal(0)

  return rms 


 def calcRdata(self,b):

  data_Z = self.fit_file.Get("shapes_prefit/%s_%s/data"%(self.cat,self.ZR))
  Zd     = data_Z.GetY()[b-1]
  Ze     = 0.5*(data_Z.GetErrorYhigh(b-1)+data_Z.GetErrorYlow(b-1))
  
  data_W = self.fit_file.Get("shapes_prefit/%s_%s/data"%(self.cat,self.WR))
  Wd     = data_W.GetY()[b-1]
  We     = 0.5*(data_W.GetErrorYhigh(b-1)+data_W.GetErrorYlow(b-1))

  # Remove the backgrounds!
  TT_Z  = self.fit_file.Get("shapes_prefit/%s_%s/TOP"%(self.cat,self.ZR))
  ttZ_d = TT_Z.GetBinContent(b)
  VV_Z  = self.fit_file.Get("shapes_prefit/%s_%s/VV"%(self.cat,self.ZR))
  VVZ_d = VV_Z.GetBinContent(b)
  
  # Remove the backgrounds!
  TT_W  = self.fit_file.Get("shapes_prefit/%s_%s/TOP"%(self.cat,self.WR))
  ttW_d = TT_W.GetBinContent(b)
  VV_W  = self.fit_file.Get("shapes_prefit/%s_%s/VV"%(self.cat,self.WR))
  VVW_d = VV_W.GetBinContent(b)

  Wd -= (ttW_d+VVW_d)
  Zd -= (ttZ_d+VVZ_d)
  
  rwz = Zd/Wd
  rwz_e = rwz * ( ( (Ze/Zd)**2 + (We/Wd)**2)**0.5 )

  return rwz, rwz_e

 
 


