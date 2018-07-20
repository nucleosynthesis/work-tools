# merged plots if the exist at all :)
#!/bin/bash

#python makeSplitPanel.py --lhc A1_5PD_lhc_A1_5PD.root --dashes 4,9,11,16,21 --sm theory_A1_5PD.root 

#--labels "(#sigma #upoint B)^{#gamma#gamma}_{ggF},(#sigma #upoint B)^{#gamma#gamma}_{VBF},(#sigma #upoint B)^{#gamma#gamma}_{WH},(#sigma #upoint B)^{#gamma#gamma}_{ZH},(#sigma #upoint B)^{#gamma#gamma}_{ttH},(#sigma #upoint B)^{ZZ}_{ggF},(#sigma #upoint B)^{ZZ}_{VBF},(#sigma #upoint B)^{WW}_{ggF},(#sigma #upoint B)^{WW}_{VBF},(#sigma #upoint B)^{WW}_{WH},(#sigma #upoint B)^{WW}_{ZH},(#sigma #upoint B)^{WW}_{ttH},(#sigma #upoint B)^{#tau#tau}_{ggF},(#sigma #upoint B)^{#tau#tau}_{VBF},(#sigma #upoint B)^{#tau#tau}_{WH},(#sigma #upoint B)^{#tau#tau}_{ZH},(#sigma #upoint B)^{#tau#tau}_{ttH},(#sigma #upoint B)^{bb}_{WH},(#sigma #upoint B)^{bb}_{ZH},(#sigma #upoint B)^{bb}_{ttH}"  

#assume order is atlas, cms, LHC 
# hmmm
python makeDoublePanelK2.py -b neg_lhc_K2_BSM.root neg_atlas_K2_BSM.root neg_cms_K2_BSM.root  neg_lhc_K2_BSM0.root   neg_atlas_K2_BSM0.root neg_cms_K2_BSM0.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-1.79:2.49"  --labels "#kappa_{Z},#kappa_{W},#kappa_{t},|#kappa_{#tau}|,|#kappa_{b}|,|#kappa_{g}|,|#kappa_{#gamma}|,B_{BSM}" -o PAPERPLOTS/plot_K2_K2_BRinv_per_exp_merged --colors 1,4,2 --legleft  --msizes 7.0,6.2,6.2 --status PAPER  --legdown --legfilled --negs 2 --sig2files 1:sig2_neg_atlas_K2_BSM.root --sig2files 2:sig2_neg_cms_K2_BSM.root --sig2files 0:sig2_neg_lhc_K2_BSM.root --sig2files 4:sig2_neg_atlas_K2_BSM0.root --sig2files 5:sig2_neg_cms_K2_BSM0.root --sig2files 3:sig2_neg_lhc_K2_BSM0.root --left "#splitline{|#kappa_{V}| #leq 1}{B_{BSM} #geq 0}" --right "B_{BSM} = 0" --widths 0.032,0.02,0.02

python makeChannelComp.py -b neg_lhc_K2_BSM.root neg_lhc_K2_BSM0.root   --markers 20,20 --groups "|#kappa_{V}| #leq 1,B_{BSM}=0"   --xl "Parameter value" --xr "-1.5:2"   --labels "#kappa_{Z},#kappa_{W},#kappa_{t},|#kappa_{#tau}|,|#kappa_{b}|,|#kappa_{g}|,|#kappa_{#gamma}|,B_{BSM}" -o PAPERPLOTS/plot_K2_K2_BRinv_merged --colors 1,8 --legleft --widths 0.024,0.024 --msizes 1.0,1.0 --smcen 1,8 --sig2files 0:sig2_neg_lhc_K2_BSM.root --sig2files 1:sig2_neg_lhc_K2_BSM0.root --status PAPER --negs 2 --legVerydown --legfilled


python makeChannelComp.py -b neg_lhc_K2.root   neg_atlas_K2.root neg_cms_K2.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-2:2.5"   --labels "#kappa_{Z},#kappa_{W},#kappa_{t},|#kappa_{#tau}|,|#kappa_{b}|,|#kappa_{g}|,|#kappa_{#gamma}|" -o PAPERPLOTS/plot_K2_merged --colors 1,4,2 --legleft --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --negs 2 --legVerydown --status PAPER --sig2files 1:sig2_neg_atlas_K2.root --sig2files 2:sig2_neg_cms_K2.root --sig2files 0:sig2_neg_lhc_K2.root --legfilled --negs 2


python makeChannelComp.py -b neg_lhc_K2_BSM.root   neg_atlas_K2_BSM.root neg_cms_K2_BSM.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-2:2.5"   --labels "#kappa_{Z},#kappa_{W},#kappa_{t},|#kappa_{#tau}|,|#kappa_{b}|,|#kappa_{g}|,|#kappa_{#gamma}|,B_{BSM}" -o PAPERPLOTS/plot_K2_BRinv_merged --colors 1,4,2 --legleft --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --status PAPER --sig2files 1:sig2_neg_atlas_K2_BSM.root --sig2files 2:sig2_neg_cms_K2_BSM.root --sig2files 0:sig2_neg_lhc_K2_BSM.root --legVerydown --legfilled --negs 2

python makeChannelComp.py -b lhc_K1.root   atlas_K1.root cms_K1.root 	     --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-2:3.5"  --labels "#kappa_{Z},#kappa_{W},#kappa_{t},|#kappa_{#tau}|,#kappa_{b}" -o PAPERPLOTS/plot_K1_merged --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --sig2files 0:sig2_lhc_K1.root  --sig2files 1:sig2_atlas_K1.root --sig2files 2:sig2_cms_K1.root --status PAPER

python makeChannelComp.py -b neg_lhc_K1_mm.root   neg_atlas_K1_mm.root neg_cms_K1_mm.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-2:3.5"  --labels "#kappa_{Z},#kappa_{W},#kappa_{t},|#kappa_{#tau}|,#kappa_{b},|#kappa_{#mu}|" -o PAPERPLOTS/plot_K1_merged_kmu --colors 1,4,2  --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --sig2files 0:sig2_neg_lhc_K1_mm.root  --sig2files 1:sig2_neg_atlas_K1_mm.root --sig2files 2:sig2_neg_cms_K1_mm.root --negs 2 --status PAPER

python makeChannelComp.py -b neg_lhc_L2_ldu.root   neg_atlas_L2_ldu.root neg_cms_L2_ldu.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-2.0:4.0"  --labels "#lambda_{du},#lambda_{Vu},#kappa_{uu}" -o PAPERPLOTS/plot_L2_du_merged --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --sig2files 0:sig2_neg_lhc_L2_ldu.root  --sig2files 1:sig2_neg_atlas_L2_ldu.root --sig2files 2:sig2_neg_cms_L2_ldu.root  --status PAPER --interval
                                                  
python makeChannelComp.py -b neg_lhc_L2_llq.root   neg_atlas_L2_llq.root neg_cms_L2_llq.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "0.:3.0"  --labels "|#lambda_{lq}|,#lambda_{Vq},#kappa_{qq}" -o PAPERPLOTS/plot_L2_lq_merged --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86   --sig2files 0:sig2_neg_lhc_L2_llq.root  --sig2files 1:sig2_neg_atlas_L2_llq.root --sig2files 2:sig2_neg_cms_L2_llq.root --status PAPER



python makeChannelComp.py -b neg_lhc_L1.root   neg_atlas_L1.root neg_cms_L1.root  --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-3.6:3.5"  --labels "#kappa_{gZ},#lambda_{Zg},#lambda_{tg},#lambda_{WZ},|#lambda_{#gammaZ}|,|#lambda_{#tauZ}|,|#lambda_{bZ}|" -o PAPERPLOTS/plot_L1_merged --colors 1,4,2  --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --legleft   --sig2files 0:sig2_neg_lhc_L1.root  --sig2files 1:sig2_neg_atlas_L1.root --sig2files 2:sig2_neg_cms_L1.root --legfilled --status PAPER --intervals --negs 0,1 --legSuperdown 


python makeSplitPanel.py --lhc A1_5PD_lhc_A1_5PD.root --dashes 4,9,11,16,21 --sm theory_A1_5PD.root --status PAPER -o PAPERPLOTS/plot_A15PD



python makeChannelComp.py -b A1_5PD_lhc_A1_5PD_minimal.root  --xl "#sigma #upoint B norm. to SM prediction" --xr "-6.:10."  -o PAPERPLOTS/plot_A15PD_noth_merged --colors 1  --markers 20 --widths 0.01 --sm theory_A1_5PD_minimal.root --msizes 1.6  --smalllabs --longStyle --groups "Observed #pm1#kern[0.2]{#sigma}" --labels "#gamma#gamma,ZZ,WW,#tau#tau,#gamma#gamma,ZZ,WW,#tau#tau,#gamma#gamma,WW,#tau#tau,bb,#gamma#gamma,WW,#tau#tau,bb,#gamma#gamma,WW,#tau#tau,bb" --line 4 --line 8 --line 12 --line 16 --texlabels "ggF:0.12,0.8" --texlabels "VBF:0.12,0.64" --texlabels "WH:0.12,0.48" --texlabels "ZH:0.12,0.32" --texlabels "ttH:0.12,0.16" --status PAPER


python makeChannelComp.py -b lhc_A1_5D.root   atlas_A1_5D.root cms_A1_5D.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-1:4"  --labels "#mu^{#gamma#gamma},#mu^{ZZ},#mu^{WW},#mu^{#tau#tau},#mu^{bb}" -o PAPERPLOTS/plot_A1_5D_merged --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86  --sig2files 0:sig2_lhc_A1_5D.root  --sig2files 1:sig2_atlas_A1_5D.root --sig2files 2:sig2_cms_A1_5D.root --status PAPER 
                                             
python makeChannelComp.py -b lhc_A1_5P.root   atlas_A1_5P.root cms_A1_5P.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-1:4"  --labels "#mu_{ggF},#mu_{VBF},#mu_{WH},#mu_{ZH},#mu_{ttH},#mu" -o PAPERPLOTS/plot_A1_5P_merged --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --line 5  --sig2files 0:sig2_lhc_A1_5P.root  --sig2files 1:sig2_atlas_A1_5P.root --sig2files 2:sig2_cms_A1_5P.root --status PAPER  


python makeChannelComp.py -b lhc_B1ZZ.root  atlas_B1ZZ.root cms_B1ZZ.root  --xl "Parameter value norm. to SM prediction" --xr "-1.:6" --groups "ATLAS+CMS,ATLAS,CMS" --labels "#sigma(gg#rightarrowH#rightarrowZZ),#sigma_{VBF}/#sigma_{ggF},#sigma_{WH}/#sigma_{ggF},#sigma_{ZH}/#sigma_{ggF},#sigma_{ttH}/#sigma_{ggF},B^{WW}/B^{ZZ},B^{#gamma#gamma}/B^{ZZ},B^{#tau#tau}/B^{ZZ},B^{bb}/B^{ZZ}" -o PAPERPLOTS/plot_B1ZZ_noth_merged --colors 1,4,2 --markers 20,23,22 --widths 0.024,0.005,0.005  --sm SM_B1ZZ.root --msizes 1.0,0.86,0.86  --sig2files 0:sig2_lhc_B1ZZ.root  --sig2files 1:sig2_atlas_B1ZZ.root  --sig2files 2:sig2_cms_B1ZZ.root  --status PAPER --smalllabs 
                                          
python makeChannelComp.py -b lhc_B1WW.root  atlas_B1WW.root cms_B1WW.root  --xl "Parameter value norm. to SM prediction" --xr "-1.:6" --groups "ATLAS+CMS,ATLAS,CMS" --labels "#sigma(gg#rightarrowH#rightarrowWW),#sigma_{VBF}/#sigma_{ggF},#sigma_{WH}/#sigma_{ggF},#sigma_{ZH}/#sigma_{ggF},#sigma_{ttH}/#sigma_{ggF},B^{ZZ}/B^{WW},B^{#gamma#gamma}/B^{WW},B^{#tau#tau}/B^{WW},B^{bb}/B^{WW}" -o PAPERPLOTS/plot_B1WW_noth_merged --colors 1,4,2 --markers 20,23,22 --widths 0.024,0.005,0.005  --sm SM_B1WW.root --msizes 1.0,0.86,0.86  --sig2files 0:sig2_lhc_B1WW.root  --sig2files 1:sig2_atlas_B1WW.root  --sig2files 2:sig2_cms_B1WW.root  --status PAPER --smalllabs 

python makeChannelComp.py -b lhc_B2.root   atlas_B2.root cms_B2.root --xl "Parameter value norm. to SM prediction" --xr "-1.:6" --groups  "ATLAS,CMS,ATLAS+CMS" --labels "#sigma_{ggF}#timesB^{WW},#sigma_{VBF}#times B^{#tau#tau},#sigma_{WH}/#sigma_{VBF},#sigma_{ZH}/#sigma_{WH},#sigma_{ttH}/#sigma_{ggF},B^{ZZ}/B^{WW},B^{#gamma#gamma}/B^{WW},B^{#tau#tau}/B^{WW},B^{bb}/B^{#tau#tau}" -o PAPERPLOTS/plot_B2_noth_merged --colors 1,4,2   --markers 20,23,22 --widths 0.024,0.005,0.005  --sm SM_B2.root --msizes 1.0,0.86,0.86  --sig2files 0:sig2_lhc_B2.root  --sig2files 1:sig2_atlas_B2.root  --sig2files 2:sig2_cms_B2.root --status PAPER --smalllabs 


python makeChannelComp.py -b lhc_B1WW.root stat_lhc_B1WW.root sys_lhc_B1WW.root --xl "Normalised to SM prediction " --xr "-1.:5.6" --groups "Total,Stat,Sys"  -o PAPERPLOTS/plot_B1WW_noth_breakdown_lhc --colors 1,r.kAzure,r.kViolet  --smalllabs --noshift --markers 20,0,0 --widths 0.01,0.2,0.3 --sm SM_B1WW.root --msizes 0.6,0,0  --labels  "#sigma(gg#rightarrowH#rightarrowWW),#sigma_{VBF}/#sigma_{ggF},#sigma_{WH}/#sigma_{ggF},#sigma_{ZH}/#sigma_{ggF},#sigma_{ttH}/#sigma_{ggF},B^{ZZ}/B^{WW},B^{#gamma#gamma}/B^{WW},B^{#tau#tau}/B^{WW},B^{bb}/B^{WW}" --status PAPER --smalllabs


python makeChannelComp.py -b lhc_B1ZZ.root stat_lhc_B1ZZ.root sys_lhc_B1ZZ.root --xl "Normalised to SM prediction " --xr "-1.:5.6" --groups "Total,Stat,Sys"  -o PAPERPLOTS/plot_B1ZZ_noth_breakdown_lhc --colors 1,r.kAzure,r.kViolet  --smalllabs --noshift --markers 20,0,0 --widths 0.01,0.2,0.3 --sm SM_B1ZZ.root --msizes 0.6,0,0 --labels "#sigma(gg#rightarrowH#rightarrowZZ),#sigma_{VBF}/#sigma_{ggF},#sigma_{WH}/#sigma_{ggF},#sigma_{ZH}/#sigma_{ggF},#sigma_{ttH}/#sigma_{ggF},B^{WW}/B^{ZZ},B^{#gamma#gamma}/B^{ZZ},B^{#tau#tau}/B^{ZZ},B^{bb}/B^{ZZ}" --status PAPER 

python makeChannelComp.py -b neg_lhc_L2_lfv.root   neg_atlas_L2_lfv.root neg_cms_L2_lfv.root  --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "0.:2.5"  --labels "|#lambda_{FV}|,#kappa_{VV}" -o PAPERPLOTS/plot_L2_FV_merged  --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --sig2files 1:sig2_neg_atlas_L2_lfv.root --sig2files 2:sig2_neg_cms_L2_lfv.root --sig2files 0:sig2_neg_lhc_L2_lfv.root --status PAPER


python makeChannelComp.py -b lhc_K3.root   atlas_K3.root cms_K3.root  --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr ".5:1.8"   --labels "#kappa_{V},#kappa_{F}" -o PAPERPLOTS/plot_K3_merged --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --sig2files 1:sig2_atlas_K3.root --sig2files 2:sig2_cms_K3.root --sig2files 0:sig2_lhc_K3.root --status PAPER 

python makeChannelComp.py -b  lhc_K3_5D.root  atlas_K3_5D.root cms_K3_5D.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "0:5"   --labels "#kappa_{V}^{#gamma#gamma},#kappa_{V}^{ZZ},#kappa_{V}^{WW},#kappa_{V}^{#tau#tau},#kappa_{V}^{bb},#kappa_{F}^{#gamma#gamma},#kappa_{F}^{ZZ},#kappa_{F}^{WW},#kappa_{F}^{#tau#tau},#kappa_{F}^{bb}" -o PAPERPLOTS/plot_K3_5D_merged --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --sig2files 1:sig2_atlas_K3_5D.root --sig2files 2:sig2_cms_K3_5D.root --sig2files 0:sig2_lhc_K3_5D.root --status PAPER 

python makeChannelComp.py -b  neg_lhc_K3_5D_N.root  neg_atlas_K3_5D_N.root neg_cms_K3_5D_N.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-5:7"   --labels "#kappa_{F}^{#gamma#gamma},#kappa_{F}^{ZZ},#kappa_{F}^{WW},#kappa_{F}^{#tau#tau},#kappa_{F}^{bb}" -o PAPERPLOTS/plot_K3_5D_N_merged --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --sig2files 1:sig2_neg_atlas_K3_5D_N.root --sig2files 2:sig2_neg_cms_K3_5D_N.root --sig2files 0:sig2_neg_lhc_K3_5D_N.root --status PAPER

python makeChannelComp.py -b lhc_A1_muVmuF.root   atlas_A1_muVmuF.root cms_A1_muVmuF.root  --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl " " --xr "-4.0:6.5"  --labels "#mu_{V}^{#gamma#gamma},#mu_{V}^{ZZ},#mu_{V}^{WW},#mu_{V}^{#tau#tau},#mu_{V}^{bb},#mu_{F}^{#gamma#gamma},#mu_{F}^{ZZ},#mu_{F}^{WW},#mu_{F}^{#tau#tau},#mu_{F}^{bb}" -o PAPERPLOTS/plot_A1_muVmuF_merged --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --sig2files 1:sig2_atlas_A1_muVmuF.root --sig2files 2:sig2_cms_A1_muVmuF.root --sig2files 0:sig2_lhc_A1_muVmuF.root --status PAPER

# Non standard or OLD versions .... ----------------

#python makeChannelComp.py -b atlas_K3_N.root cms_K3_N.root lhc_K3_N.root   --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-2:2"   --labels "#kappa_{V},#kappa_{F}" -o PAPERPLOTS/plot_K3_N_merged --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --sig2files 1:sig2_atlas_K3_N.root --sig2files 2:sig2_cms_K3_N.root --sig2files 0:sig2_lhc_K3_N.root 

exit 

                                           
python makeChannelComp.py -b lhc_K1_mm.root atlas_K1_mm.root cms_K1_mm.root    --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-0.5:2"  --labels "#kappa_{Z},#kappa_{W},#kappa_{t},#kappa_{#tau},#kappa_{b},#kappa_{#mu}" -o PAPERPLOTS/plot_K1_merged_kmu --colors 1,4,2 --legleft --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --sig2files 0:sig2_lhc_K1_mm.root  --sig2files 1:sig2_atlas_K1_mm.root --sig2files 2:sig2_cms_K1_mm.root --status PAPER

python makeChannelComp.py -b lhc_K2.root   atlas_K2.root cms_K2.root  --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-1.5:2"   --labels "#kappa_{Z},#kappa_{W},#kappa_{t},#kappa_{#tau},#kappa_{b},#kappa_{g},#kappa_{#gamma}" -o PAPERPLOTS/plot_K2_merged --colors 1,4,2 --legleft --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --negs 2 --legdown --status PAPER

python makeChannelComp.py -b lhc_K2_BSM.root  atlas_K2_BSM.root cms_K2_BSM.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-0.5:2"   --labels "#kappa_{Z},#kappa_{W},#kappa_{t},#kappa_{#tau},#kappa_{b},#kappa_{g},#kappa_{#gamma},B_{BSM}" -o PAPERPLOTS/plot_K2_BRinv_merged --colors 1,4,2 --legleft --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --status PAPER --legdown





python makeChannelComp.py -b lhc_K2_BSM.root lhc_K2_BSM0.root   --markers 20,20 --groups "#kappa_{V} #leq 1,B_{BSM}=0"   --xl "Parameter value" --xr "0.:2"   --labels "#kappa_{Z},#kappa_{W},#kappa_{t},#kappa_{#tau},#kappa_{b},#kappa_{g},#kappa_{#gamma},B_{BSM}" -o PAPERPLOTS/plot_K2_K2_BRinv_merged --colors 1,r.kOrange --legleft --widths 0.024,0.024 --msizes 1.0,1.0 --smcen 1,8 --sig2files 0:sig2_lhc_K2_BSM.root --sig2files 1:sig2_lhc_K2_BSM0.root --status PAPER


python makeChannelComp.py -b neg_lhc_L2_ldu.root   --markers 20 --groups "Observed #pm1#sigma"  --xl "Parameter value" --xr "-1.5:2."  --labels "#lambda_{du},#lambda_{Vu},#kappa_{uu}" -o PAPERPLOTS/plot_L2_du_merged_lhconly --colors 1 --widths 0.024 --msizes 1.0 --negs 0 --sig2files 0:sig2_neg_lhc_L2_ldu.root --status PAPER

python makeChannelComp.py -b neg_lhc_L2_llq.root   --markers 20 --groups "Observed #pm1#sigma"  --xl "Parameter value" --xr "-1.5:2."  --labels "#lambda_{lq},#lambda_{Vq},#kappa_{qq}" -o PAPERPLOTS/plot_L2_lq_merged_lhconly --colors 1 --widths 0.024 --msizes 1.0 --negs 0 --sig2files 0:sig2_neg_lhc_L2_llq.root --status PAPER


python makeChannelComp.py -b --addnumber 2 --smalllabs atlas_A1_5D.root cms_A1_5D.root lhc_A1_5D.root   --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "0:4"  --labels "#mu^{#gamma#gamma},#mu^{ZZ},#mu^{WW},#mu^{#tau#tau},#mu^{bb}" -o PAPERPLOTS/plot_A1_5D_merged_numbers --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86  --status PAPER

python makeChannelComp.py -b --addnumber 2 --smalllabs atlas_A1_5P.root cms_A1_5P.root lhc_A1_5P.root   --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "0:4"  --labels "#mu_{ggF},#mu_{VBF},#mu_{WH},#mu_{ZH},#mu_{ttH},#mu" -o PAPERPLOTS/plot_A1_5P_merged_numbers --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --line 5 --status PAPER 

python makeChannelComp.py -b --addnumber 2 --smalllabs atlas_K1.root cms_K1.root lhc_K1.root   --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-0.5:2"  --labels "#kappa_{Z},#kappa_{W},#kappa_{t},#kappa_{#tau},#kappa_{b}" -o PAPERPLOTS/plot_K1_merged_numbers --colors 1,4,2 --legleft --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --status PAPER

python makeChannelComp.py -b --addnumber 2 --smalllabs atlas_K2.root cms_K2.root lhc_K2.root   --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-0.5:2"   --labels "#kappa_{Z},#kappa_{W},#kappa_{t},#kappa_{#tau},#kappa_{b},#kappa_{g},#kappa_{#gamma}" -o PAPERPLOTS/plot_K2_merged_numbers --colors 1,4,2 --legleft --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --status PAPER 

python makeChannelComp.py -b --addnumber 2 --smalllabs atlas_K2_BSM.root cms_K2_BSM.root lhc_K2_BSM.root   --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "-0.5:2"   --labels "#kappa_{Z},#kappa_{W},#kappa_{t},#kappa_{#tau},#kappa_{b},#kappa_{g},#kappa_{#gamma},B_{BSM}" -o PAPERPLOTS/plot_K2_BRinv_merged_numbers --colors 1,4,2 --legleft --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --status PAPER

python makeChannelComp.py -b --addnumber 2 --smalllabs atlas_K3.root cms_K3.root lhc_K3.root   --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "0.5:1.8"   --labels "#kappa_{V},#kappa_{F}" -o PAPERPLOTS/plot_K3_merged_numbers --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --status PAPER

python makeChannelComp.py -b --addnumber 2 --smalllabs atlas_L2_lfv.root cms_L2_lfv.root lhc_L2_lfv.root   --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "0.5:2."  --labels "#lambda_{FV},#kappa_{VV}" -o PAPERPLOTS/plot_L2_FV_merged_numbers  --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --status PAPER 

python makeChannelComp.py -b --addnumber 2 --smalllabs atlas_L2_ldu.root cms_L2_ldu.root lhc_L2_ldu.root   --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "0.:2.5"  --labels "#lambda_{du},#lambda_{Vu},#kappa_{uu}" -o PAPERPLOTS/plot_L2_du_merged_numbers --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --status PAPER

python makeChannelComp.py -b --addnumber 2 --smalllabs atlas_L2_llq.root cms_L2_llq.root lhc_L2_llq.root   --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "0:2.5"  --labels "#lambda_{lq},#lambda_{Vq},#kappa_{qq}" -o PAPERPLOTS/plot_L2_lq_merged_numbers --colors 1,4,2 --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --status PAPER 

#python makeChannelComp.py -b lhc_K1_mm.root   atlas_K1_mm.root cms_K1_mm.root --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "0.:3.0"  --labels "#kappa_{Z},#kappa_{W},#kappa_{t},#kappa_{#tau},#kappa_{b},#kappa_{#mu}" -o PAPERPLOTS/plot_K1_merged_kmu --colors 1,4,2  --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --sig2files 0:sig2_lhc_K1_mm.root  --sig2files 1:sig2_atlas_K1_mm.root --sig2files 2:sig2_cms_K1_mm.root --status PAPER

python makeChannelComp.py -b --addnumber 2 --smalllabs atlas_L1.root cms_L1.root lhc_L1.root   --markers 20,23,22 --groups "ATLAS+CMS,ATLAS,CMS"   --xl "Parameter value" --xr "0.:3"  --labels "#kappa_{gZ},#lambda_{Zg},#lambda_{tg},#lambda_{WZ},#lambda_{#gammaZ},#lambda_{#tauZ},#lambda_{bZ}" -o PAPERPLOTS/plot_L1_merged_numbers --colors 1,4,2  --widths 0.024,0.005,0.005  --msizes 1.0,0.86,0.86 --status PAPER 
