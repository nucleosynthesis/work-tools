import sys
import numpy as np 
from scipy import interpolate 
from scipy.stats import chi2 
from scipy.stats import poisson
import matplotlib.pyplot as plt

def calculateExpectedSignificance(signal, background):
  
  sterm=0
  ogterms=0
  nchannel  = len(signal)

  if (len(background)!=nchannel): 
  	sys.exit(" background and signal vectors should be the same size!")

  for i in range(nchannel): 
    if signal[i]<=0: continue
    logterms+=(signal[i]+background[i])*np.log((signal[i]+background[i])/background[i])
    sterm+=signal[i]

  sig =  1.4142*np.sqrt(logterms - sterm)
  return sig

def calculateExpectedCLs(mu, signal,  background):
  logterms=0;
  nchannel  = len(signal)

  if (len(background)!=nchannel): 
  	sys.exit(" background and signal vectors should be the same size!")

  for i in range(nchannel):
    if not background[i]>0: continue
    bi = background[i]
    si = mu*signal[i]
    logterms+= bi*(np.log(si+bi) - np.log(bi)) - si
  
  qmu = -2*logterms
  # Note that we should take the 1-sided version but with CL_s = CL_s+b/CL_b, we cancel another factor of 0.5 as expected CL_b=0.5 always
  CLs = 1-chi2.cdf(qmu,1)
  return CLs

def calculateExpectedLimit(rlow, rhigh,  signal,  background,  np=20):

  step = (rhigh-rlow)/np
  mu = rlow

  CLs_vals = []
  mu_vals  = []
  for i in range(np):
    CLs = calculateExpectedCLs(mu,signal,background)
    
    print("At mu = ",mu, ", CLs = ",CLs)
    mu_vals.append(mu)
    CLs_vals.append(CLs)

    mu+=step

  plt.plot(mu_vals,CLs_vals)
  
  f = interpolate.interp1d(CLs_vals,mu_vals)
  res = f(0.05)
  plt.axvline(res,color='red',label="95%% upper limit on mu=%.4f"%res)
  plt.axhline(0.05,color='red')
  plt.legend()
  plt.show()
  return res

print("Upper limit on s from code",calculateExpectedLimit(0.1,20,[1],[10]))
