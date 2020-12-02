import ROOT 

class TFSystematics: 
 def __init__(self,input_ws_file):

  self.fiws = ROOT.TFile.Open(input_ws_file)
  self.workspace = self.fiws.Get("w")

  self.nbins=9 
  self.cat = "MTR_2017"
  self.Numerator   = ""
  self.Denominator = ""
  self.Xvar = ""
 

 def calcR(self,b):

  icenter = (self.workspace.var(self.Xvar).getBinning()).binCenter(b-1)
  iwidth  = (self.workspace.var(self.Xvar).getBinning()).binWidth(b-1)
  self.workspace.var(self.Xvar).setVal(icenter)
  
  name_num = "shapeBkg_"+self.Numerator
  name_den = "shapeBkg_"+self.Denominator
 
  #print name_num+"__norm", name_den+"__norm"
  norm_N = self.workspace.function(name_num+"__norm").getVal(ROOT.RooArgSet())
  norm_D = self.workspace.function(name_den+"__norm").getVal(ROOT.RooArgSet())

  N = self.workspace.pdf(name_num).getVal(ROOT.RooArgSet(self.workspace.var(self.Xvar)))*norm_N*iwidth
  D = self.workspace.pdf(name_den).getVal(ROOT.RooArgSet(self.workspace.var(self.Xvar)))*norm_D*iwidth
  #print " at bin center %g --> N (%s) =%g, D (%s) =%g"%(icenter,name_num,N,name_den,D), " ratio (N/D) =", N/D 
  return N/D

 def getBins(self): 

  return (self.workspace.var(self.Xvar).getBinning()).array()

 def gimmeHist(self, par, h, v):
   
   oval = self.workspace.var(par.GetName()).getVal()
   self.workspace.var(par.GetName()).setVal(v)
   hn = h.Clone(); hn.SetName(par.GetName()+"_%g"%v)
   for b in range(1,(self.nbins)+1): 
     hn.SetBinContent(b,self.calcR(b))

   hn.SetLineWidth(1)
   self.workspace.var(par.GetName()).setVal(oval)
   return hn
  
 def list_of_parameters(self): 
  
  name_num = "shapeBkg_"+self.Numerator
  name_den = "shapeBkg_"+self.Denominator
  allpars_N   = self.workspace.pdf(name_num).getParameters(ROOT.RooArgSet(self.workspace.var(self.Xvar)))
  allpars_D   = self.workspace.pdf(name_den).getParameters(ROOT.RooArgSet(self.workspace.var(self.Xvar)))
  allpars_NN  = self.workspace.function(name_num+"__norm").getParameters(ROOT.RooArgSet())
  allpars_DD  = self.workspace.function(name_den+"__norm").getParameters(ROOT.RooArgSet())

  allpars_N.add(allpars_D)
  allpars_N.add(allpars_DD)
  allpars_N.add(allpars_NN)
  
  return allpars_N
