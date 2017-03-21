#!/bin/bash
for mindetacut in 2.5 3.0 3.5 4.0 4.5 5.0
do
  for maxdphicut in  3.1416 2.8 2.5 2.1 1.8 1.5 1.2 0.9 0.6 0.3 
  #for maxdphicut in  0.3 3.1416 
   do 
    for minjjcut in 701 801 901 1001 1101 1201 1301 1401
    do
     cardname=combined_card_${mindetacut}_${maxdphicut}_${minjjcut}.txt
     #combineCards.py -S qcd=qcd/vbfhinv_qcd_13TeV_$mindetacut\_$maxdphicut\_$minjjcut\.txt \
     combineCards.py -S \
   	enu=enu/vbfhinv_enu_13TeV_$mindetacut\_$maxdphicut\_$minjjcut\.txt \
   	munu=munu/vbfhinv_munu_13TeV_$mindetacut\_$maxdphicut\_$minjjcut\.txt \
   	mumu=mumu/vbfhinv_mumu_13TeV_$mindetacut\_$maxdphicut\_$minjjcut\.txt \
   	ee=ee/vbfhinv_ee_13TeV_$mindetacut\_$maxdphicut\_$minjjcut\.txt \
   	taunu=taunu/vbfhinv_taunu_13TeV_$mindetacut\_$maxdphicut\_$minjjcut\.txt \
   	nunu=nunu/vbfhinv_nunu_13TeV_$mindetacut\_$maxdphicut\_$minjjcut\.txt \
	> silly_$cardname
     cat silly_$cardname | grep -v "nuisance edit"  > $cardname
     echo "ggH_kill rateParam * ggH 0 " >> $cardname
     echo "nuisance edit freeze ggH_kill " >> $cardname
     echo "lumiscale rateParam * * 2.82 " >> $cardname
     echo "nuisance edit freeze lumiscale " >> $cardname
     python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/systematicsAnalyzer.py --format html $cardname  > ${cardname}.html

     combineCards.py -S \
   	nunu=nunu/vbfhinv_nunu_13TeV_$mindetacut\_$maxdphicut\_$minjjcut\.txt \
	> silly_SR_$cardname
	cat silly_SR_$cardname | grep -v "nuisance edit"  > SR_$cardname
	echo "ggH_kill rateParam * ggH 0 " >> SR_$cardname
	echo "nuisance edit freeze ggH_kill " >> SR_$cardname
	echo "lumiscale rateParam * * 2.82 " >> SR_$cardname
	echo "nuisance edit freeze lumiscale " >> SR_$cardname
	echo "nuisance edit freeze WZ_xsection " >> SR_$cardname
     
     combine $cardname -M Asymptotic --run blind  --trackParameters dphi_jj,deta_jj,mjj -n params_${cardname} --freezeNuisances mjj,deta_jj,dphi_jj,QCD_xsection
#     combine $cardname -M Asymptotic --run blind  --trackParameters dphi_jj,deta_jj,mjj -n no_sys_params_${cardname} -S 0 --freezeNuisances mjj,deta_jj,dphi_jj,QCD_xsection

 #    combine SR_$cardname -M Asymptotic --run blind -S 0 --trackParameters dphi_jj,deta_jj,mjj -n SR_params_${cardname} --freezeNuisances mjj,deta_jj,dphi_jj,QCD_xsection,WZ_xsection
    done 
   done
done 
