entries = {
	'mu_XS_ggFbbH_BR_gamgam': [43.8,5.]
	,'mu_XS_VBF_BR_gamgam'	 : [3.6,0.2]
	,'mu_XS_WH_BR_gamgam'	 : [1.6,0.09]
	,'mu_XS_ZH_BR_gamgam'	 : [0.94,0.06]
	,'mu_XS_ttHtH_BR_gamgam' : [0.294,0.035]
	,'mu_XS_ggFbbH_BR_ZZ'	 : [513,57]
	,'mu_XS_VBF_BR_ZZ'	 : [42.2,2.0]
	,'mu_XS_WH_BR_ZZ'	 : [18.8,0.9]
	,'mu_XS_ZH_BR_ZZ'	 : [11.1,0.6]
	,'mu_XS_ttHtH_BR_ZZ'	 : [3.44,0.4]
	,'mu_XS_ggFbbH_BR_WW'	 : [4.15,0.47]
	,'mu_XS_VBF_BR_WW'	 : [0.341,0.017]
	,'mu_XS_WH_BR_WW'	 : [0.152,0.007]
	,'mu_XS_ZH_BR_WW'	 : [0.089,0.005]
	,'mu_XS_ttHtH_BR_WW'	 : [0.028,0.003]
	,'mu_XS_ggFbbH_BR_tautau': [1210,140]
	,'mu_XS_VBF_BR_tautau'	 : [99.5,6.2]
	,'mu_XS_WH_BR_tautau'	 : [44.3,2.8]
	,'mu_XS_ZH_BR_tautau'	 : [26.1,1.8]
	,'mu_XS_ttHtH_BR_tautau' : [8.13,1.0]
	,'mu_XS_ggFbbH_BR_bb'  	 : [11.0,1.2]
	,'mu_XS_VBF_BR_bb'  	 : [0.909,0.038]
	,'mu_XS_WH_BR_bb'  	 : [0.4,0.02]
	,'mu_XS_ZH_BR_bb'  	 : [0.24,0.01]
	,'mu_XS_ttHtH_BR_bb'  	 : [0.074,0.008]
	}


import parameters
for model in  ["A1_5PD","A1_5PD_minimal"]:
  params = parameters.parameter_order[model]
  print "python makeRooFile.py theory_%s "%(model),
  for p in params: print " 0,%g 0,%g 0,%g "%(1,float(entries[p][1])/entries[p][0],float(entries[p][1])/entries[p][0]),
  print

