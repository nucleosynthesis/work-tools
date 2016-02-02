{

  gROOT->ProcessLine(".L $CMSSW_BASE/lib/slc6_amd64_gcc481/libHiggsAnalysisCombinedLimit.so");
  gROOT->ProcessLine(".L makeLikelihoodRotation.C");
  //makeLikelihoodRotation("lduscan_neg_ext/3D/lduscan_neg_ext_3D.root","outplots-2hdm-rotatey.root",1.4,false);
  //makeLikelihoodRotation("lduscan_neg_ext_3/exp3D/lduscan_neg_ext_3_exp3D.root","outplots-2hdm-rotatey-exp.root",1.4,true);
  makeLikelihoodRotation("lduscan_neg_ext/3D/lduscan_neg_ext_3D.root","outplots-2hdm-1Dfindcrossing.root",1.4,false);
  makeLikelihoodRotation("lduscan_neg_ext_3/exp3D/lduscan_neg_ext_3_exp3D.root","outplots-2hdm-1Dfindcrossing-exp.root",1.4,true);

}
