from scipy.optimize import minimize
from scipy import linalg 
import array,numpy,sys
from matplotlib import pyplot as plt

class simplified_likelihood_linear:
 def  __init__(self,model,options):
  self.inputs_ = model
  self.rmin = options.rMin
  self.rmax = options.rMax
  self.offset = options.offset

  self.set_correlation()
  self.scan(options.npoints)

 def set_correlation(self):
  v = self.inputs_.covariance
  self.inputs_.square_covariance = [v[i:i+self.inputs_.nbins] for i in range(0,len(v),self.inputs_.nbins)]
  self.inputs_.variance = [self.inputs_.square_covariance[i][i] for i in range(self.inputs_.nbins)]

  self.inputs_.square_correlation = [ [ self.inputs_.square_covariance[i][j]/((self.inputs_.variance[i]**0.5)*(self.inputs_.variance[j]**0.5))\
  				        for i in range(self.inputs_.nbins)]\
				        for j in range(self.inputs_.nbins)]

  self.inputs_.err_mat = numpy.array(self.inputs_.square_correlation)
  self.inputs_.err_mat = linalg.inv(self.inputs_.err_mat)

 def expected(self,r,X,S,B,dB):
  return [ r*s+b+x*(db**0.5) for s,b,x,db in zip(S,B,X,dB)]

 # Define the simplified likelihood 
 def neg_log_likelihood(self,x,*args):
  #print args,args[0] 
  r = args[0]
  exp = self.expected(r,x,self.inputs_.signal,self.inputs_.background,self.inputs_.variance) 
  # [-d*log(e) + e ]

  dlogs = [-1*d*numpy.log(e) + e for d,e in zip(self.inputs_.data,exp)]

  # add the constraint part
  xarr  = numpy.array(x)
  xarrT = xarr.T

  constr = 0.5*(xarrT.dot(self.inputs_.err_mat.dot(xarr)))
  
  return sum(dlogs)+constr

 def minimizer(self,r):

  init = [0 for i in range(self.inputs_.nbins)]
  xbest = minimize(self.neg_log_likelihood,init,args=(r))

  return 2*self.neg_log_likelihood(xbest.x,r)

 def scan(self,np): 

  # scan points 
  R = numpy.linspace(self.rmin, self.rmax, np)
  C = [self.minimizer(r) for r in R]
  if self.offset: 
    minC = min(C)
    C = [c-minC for c in C]
  #print zip(R, C)
  plt.plot(R,C)
  if self.offset: plt.ylabel("-2 $Delta$ Log($L$)")
  else: plt.ylabel("-2 Log($L$)")
  plt.xlabel("$\mu$")
  plt.show()
