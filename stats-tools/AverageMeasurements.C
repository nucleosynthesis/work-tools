void AverageMeasurements(float x1=58.9, float dx1stat=3.4, float dx1uncorr=1.5, float dx1corr=2.4, float x2=68.7, float dx2stat=2.8, float dx2uncorr=0.3, float dx2corr=3.9)
{
  // 2 measurements x1 and x2 of the parameter m are averaged with the generalized
  // inverse variance weighted mean. The measurements have statistical uncertainties
  // dx1stat and dx2stat with uncorrelated systematic uncertainties dx1uncorr and dx2uncorr
  // and with 100% correlated uncertainties dx1corr and dx2corr.
  //
  // A. Read 19.03.2011, assisted by M. K. Bugge and O. M. R{\o}hne
  // Formulae validated against: 
  //    M G Cox et al 2006 Metrologia  43 S268 doi: 10.1088/0026-1394/43/4/S14
  //    "The generalized weighted mean of correlated quantities" 
  //    http://dx.doi.org/10.1088/0026-1394/43/4/S14

  // Specification of the measurements.
  // xi +- dxistat (statisical) +- dxiuncorr (unncorrelated systematics) +- dxicor (correlated systematics)

  // Enable these 3 lines to study the very special case of only (!) correlated systematic uncertainty
  //cout << "****** WARNING! You have disabled all but the correlated uncertainties! ******" << endl << endl;;
  //dx1stat = 0; dx1uncorr = 0; 
  //dx2stat = 0; dx2uncorr = 0; 
  
  // Enable these 2 lines to compare exact and approximate formulae without correlations. They should
  // give the same results.
  //cout << "****** WARNING! You have disabled the correlated uncertainties! ******" << endl << endl;
  //dx1corr = 0; dx2corr = 0;

  // Total uncertainties for both measurements
  float dx1 = sqrt(dx1stat*dx1stat + dx1uncorr*dx1uncorr + dx1corr*dx1corr);
  float dx2 = sqrt(dx2stat*dx2stat + dx2uncorr*dx2uncorr + dx2corr*dx2corr);

  // Just report what we are averaging
  cout << "The measurements being averaged:" << endl;
  cout << "-------------------------------" << endl;
  cout << "x1 = " << x1 << " +- " << dx1stat << " (stat) +- " << dx1uncorr  << " (uncorr syst) +- " << dx1corr << " (corr syst)" << endl; 
  cout << "   = " << x1 << " +- " << dx1 << " (total)" << endl;
  cout << endl;
  cout << "x2 = " << x2 << " +- " << dx2stat << " (stat) +- " << dx2uncorr  << " (uncorr syst) +- " << dx2corr << " (corr syst)" << endl; 
  cout << "   = " << x2 << " +- " << dx2 << " (total)" << endl;
  cout << endl;

  // The results
  cout << "Results for the generalized weighted average" << endl;
  cout << "--------------------------------------------" << endl;

  // Report the computed correlation coefficient (rho)
  float corrcoeff = dx1corr*dx2corr/(dx1*dx2);
  cout << "Correlation coefficient (rho) = " << corrcoeff << endl;
  cout << endl;

  // If the correlation is truely 100% then the measurements must be equal.
  // If that is the case, take the meausurement with the smallest uncertainty.
  if(corrcoeff>=1.0) {
    cout << "Very (!) special case for rho=1!!!" << endl;
    cout << "----------------------------------" << endl;
    if(fabs(x1-x2)>1e-50) {
      cout << "Sorry, for 100% correlation the measurements MUST be equal!!!" << endl;
      return;
    }
    float m = x1;
    float dm;
    if(abs(dx1corr) < abs(dx2corr)) 
      dm = fabs(dx1corr);
    else
      dm = fabs(dx2corr);
    cout << "m = " << m << " +- " << dm << " (syst)" << endl;
    cout << endl;
    return;
  }

  // Total uncertainty and generalized weighted mean
  float dm = sqrt( (1.0-corrcoeff*corrcoeff)/(1.0/(dx1*dx1) + 1.0/(dx2*dx2) - 2.0*corrcoeff/(dx1*dx2)) );
  float m = (x1/(dx1*dx1) + x2/(dx2*dx2) - corrcoeff*(x1+x2)/(dx1*dx2)) / (1.0/(dx1*dx1) + 1.0/(dx2*dx2) - 2.0*corrcoeff/(dx1*dx2));

  // Decompose uncertainty into statistical and systematic components
  float dmstat = 1.0/sqrt(1.0/(dx1stat*dx1stat) + 1.0/(dx2stat*dx2stat));
  float dmsyst = sqrt(dm*dm-dmstat*dmstat);

  // Report the results, including the generalized chi-squared
  cout << "m = " << m << " +- " << dmstat << " (stat) +- " << dmsyst << " (syst)" << endl;
  cout << "  = " << m << " +- " << dm << " (total)" << endl;
  cout << endl;

  float chisq = 1.0/(1.0-corrcoeff*corrcoeff) * ( (x1-m)*(x1-m)/(dx1*dx1) + (x2-m)*(x2-m)/(dx2*dx2) -2.0*corrcoeff*(x1-m)*(x2-m)/(dx1*dx2) );
  cout << "Generalized chi-squared = " << chisq << endl;
  cout << endl;
  
  //===============================================================================================================================

  // Some make approximate treatments of the generalized weighted mean. This is one.
  // The estimate of the mean is weighted by the inverse uncorrelated variances. The total
  // correlated systematic uncertainty is taken as the average of the two correlated systematic
  // uncertainties. The total uncertainty is decomposed into statistical and systematic contributions.

  cout << "Approximate, simple formulae" << endl;
  cout << "----------------------------" << endl;
  float dmcorr = 0.5*(dx1corr + dx2corr);
  // The subtotal uncertainties are the uncorrelated (statistical and uncorrelated systematic)
  // uncertainties.
  float dx1subtot = sqrt(dx1stat*dx1stat + dx1uncorr*dx1uncorr);
  float dx2subtot = sqrt(dx2stat*dx2stat + dx2uncorr*dx2uncorr);
  float dmsubtot = 1.0/sqrt(1.0/(dx1subtot*dx1subtot) + 1.0/(dx2subtot*dx2subtot));

  // The approximate generalized mean with decomposed and total uncertainty.
  // Note that the correlation is not taken into account in the estimate of the mean.
  m = (x1/(dx1subtot*dx1subtot) + x2/(dx2subtot*dx2subtot)) * dmsubtot*dmsubtot;
  dm = sqrt(dmsubtot*dmsubtot + dmcorr*dmcorr);
  dmsyst = sqrt(dm*dm - dmstat*dmstat);
  cout << "m = " << m << " +- " << dmstat << " (stat) +- " << dmsyst << " (syst)" << endl;
  cout << "  = " << m << " +- " << dm << " (total)" << endl;
  cout << endl;

  // This is the generalized chi-squared with the approximate minimum (m got recomputed). 
  // Note that I dare to compute it without taking the absolute value - it will be positive!
  float achisq = 1.0/(1.0-corrcoeff*corrcoeff) * ( (x1-m)*(x1-m)/(dx1*dx1) + (x2-m)*(x2-m)/(dx2*dx2) -2.0*corrcoeff*(x1-m)*(x2-m)/(dx1*dx2) );
  cout << "Generalized chi-squared = " << achisq << " (for the approximate minimum)" << endl;
  cout << "Delta chi-squared with respect to exact minimum = " << achisq-chisq << endl;
  if (achisq < chisq) {
    cout << endl;
    cout << "*** Hmmm, must be something wrong here, it shouldn't be possible for the ***" << endl;
    cout << "*** approximate formulae to find a lower minimum than the exact solution. ***" << endl;
  }
}
