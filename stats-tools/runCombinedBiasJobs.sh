#!/bin/bash

WS=hgg_datacard_mva_comb_multipdfMuScanMHProf.root
queue=8nh
JOBS=500
TOYS=2
#for i in {1..00}; do 
SEED=-1
  ##################### TESTING ##############
# python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w hggonecat.root -R scan_toy_testing_$i   --jobs $JOBS -m 125  -t 30 \
#	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0  --poiPoint=1   --expectSignal 1 "
# python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w hggonecat.root -R scan_toy_testing_$i   --jobs $JOBS -m 125  -t 30 \
#	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0  --poiPoint=1   --expectSignal 1 " -S -q 1nh
  ##################### TESTING ##############
 #THE BEST ONES Requires toysFrequentist
 python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w $WS -R scan_toy_bestfit_$i   --jobs $JOBS -m 125  -t $TOYS \
	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0 --poiPoint=1 --freezeNuisances MH  --expectSignal 1 --toysFrequentist  "
 python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w $WS -R scan_toy_bestfit_$i   --jobs $JOBS -m 125  -t $TOYS \
	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0 --poiPoint=1 --freezeNuisances MH  --expectSignal 1 --toysFrequentist  " -S -q $queue
exit 
# BERNSTEINS TRUTHS
 python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w $WS -R scan_toy_bernsteins_$i   --jobs $JOBS -m 125  -t $TOYS \
	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0  --poiPoint=1 --freezeNuisances MH  --expectSignal 1 --setPhysicsModelParameters pdfindex_7_7TeV=0,pdfindex_4_7TeV=0,pdfindex_0_7TeV=2,pdfindex_5_7TeV=1,pdfindex_8_7TeV=0,pdfindex_2_7TeV=1,pdfindex_9_7TeV=0,pdfindex_1_7TeV=1,pdfindex_3_7TeV=2,pdfindex_10_7TeV=0,pdfindex_6_7TeV=0,pdfindex_11_8TeV=0,pdfindex_9_8TeV=1,pdfindex_13_8TeV=0,pdfindex_12_8TeV=0,pdfindex_0_8TeV=1,pdfindex_10_8TeV=0,pdfindex_8_8TeV=0,pdfindex_7_8TeV=1,pdfindex_6_8TeV=1,pdfindex_2_8TeV=0,pdfindex_5_8TeV=0,pdfindex_1_8TeV=1,pdfindex_4_8TeV=1,pdfindex_3_8TeV=2"

 # POWER LAW TRUTHS
python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w $WS -R scan_toy_powerlaw_$i   --jobs $JOBS -m 125  -t $TOYS \
	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0  --poiPoint=1 --freezeNuisances MH  --expectSignal 1 --setPhysicsModelParameters pdfindex_7_7TeV=2,pdfindex_4_7TeV=2,pdfindex_0_7TeV=4,pdfindex_5_7TeV=4,pdfindex_8_7TeV=2,pdfindex_2_7TeV=4,pdfindex_9_7TeV=2,pdfindex_1_7TeV=4,pdfindex_3_7TeV=5,pdfindex_10_7TeV=2,pdfindex_6_7TeV=2,pdfindex_11_8TeV=2,pdfindex_9_8TeV=3,pdfindex_13_8TeV=3,pdfindex_12_8TeV=2,pdfindex_0_8TeV=4,pdfindex_10_8TeV=2,pdfindex_8_8TeV=2,pdfindex_7_8TeV=3,pdfindex_6_8TeV=3,pdfindex_2_8TeV=4,pdfindex_5_8TeV=2,pdfindex_1_8TeV=3,pdfindex_4_8TeV=4,pdfindex_3_8TeV=4"

 # EXPONENTIAL TRUTHS
 python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w $WS -R scan_toy_exponential_$i   --jobs $JOBS -m 125  -t $TOYS \
	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0  --poiPoint=1 --freezeNuisances MH  --expectSignal 1 --setPhysicsModelParameters pdfindex_7_7TeV=1,pdfindex_4_7TeV=1,pdfindex_0_7TeV=3,pdfindex_5_7TeV=3,pdfindex_8_7TeV=1,pdfindex_2_7TeV=3,pdfindex_9_7TeV=1,pdfindex_1_7TeV=3,pdfindex_3_7TeV=4,pdfindex_10_7TeV=1,pdfindex_6_7TeV=1,pdfindex_11_8TeV=1,pdfindex_9_8TeV=2,pdfindex_13_8TeV=2,pdfindex_12_8TeV=1,pdfindex_0_8TeV=3,pdfindex_10_8TeV=1,pdfindex_8_8TeV=1,pdfindex_7_8TeV=2,pdfindex_6_8TeV=2,pdfindex_2_8TeV=3,pdfindex_5_8TeV=1,pdfindex_1_8TeV=2,pdfindex_4_8TeV=2,pdfindex_3_8TeV=3"

 #LAURENT TRUTHS
 python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w $WS -R scan_toy_laurent_$i   --jobs $JOBS -m 125  -t $TOYS \
	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0  --poiPoint=1 --freezeNuisances MH  --expectSignal 1 --setPhysicsModelParameters pdfindex_7_7TeV=3,pdfindex_4_7TeV=3,pdfindex_0_7TeV=5,pdfindex_5_7TeV=5,pdfindex_8_7TeV=3,pdfindex_2_7TeV=5,pdfindex_9_7TeV=3,pdfindex_1_7TeV=5,pdfindex_3_7TeV=6,pdfindex_10_7TeV=3,pdfindex_6_7TeV=3,pdfindex_11_8TeV=3,pdfindex_9_8TeV=4,pdfindex_13_8TeV=4,pdfindex_12_8TeV=3,pdfindex_0_8TeV=5,pdfindex_10_8TeV=3,pdfindex_8_8TeV=3,pdfindex_7_8TeV=4,pdfindex_6_8TeV=4,pdfindex_2_8TeV=5,pdfindex_5_8TeV=3,pdfindex_1_8TeV=4,pdfindex_4_8TeV=5,pdfindex_3_8TeV=5"
 
 # SUBMIT THEM ------------------------------------------------------------------------------------------------------------------------------------------- 
 # BERNSTEINS TRUTHS
 python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w $WS -R scan_toy_bernsteins_$i   --jobs $JOBS -m 125  -t $TOYS \
	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0  --poiPoint=1 --freezeNuisances MH  --expectSignal 1 --setPhysicsModelParameters pdfindex_7_7TeV=0,pdfindex_4_7TeV=0,pdfindex_0_7TeV=2,pdfindex_5_7TeV=1,pdfindex_8_7TeV=0,pdfindex_2_7TeV=1,pdfindex_9_7TeV=0,pdfindex_1_7TeV=1,pdfindex_3_7TeV=2,pdfindex_10_7TeV=0,pdfindex_6_7TeV=0,pdfindex_11_8TeV=0,pdfindex_9_8TeV=1,pdfindex_13_8TeV=0,pdfindex_12_8TeV=0,pdfindex_0_8TeV=1,pdfindex_10_8TeV=0,pdfindex_8_8TeV=0,pdfindex_7_8TeV=1,pdfindex_6_8TeV=1,pdfindex_2_8TeV=0,pdfindex_5_8TeV=0,pdfindex_1_8TeV=1,pdfindex_4_8TeV=1,pdfindex_3_8TeV=2" -S -q $queue

 # POWER LAW TRUTHS
python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w $WS -R scan_toy_powerlaw_$i   --jobs $JOBS -m 125  -t $TOYS \
	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0  --poiPoint=1 --freezeNuisances MH  --expectSignal 1 --setPhysicsModelParameters pdfindex_7_7TeV=2,pdfindex_4_7TeV=2,pdfindex_0_7TeV=4,pdfindex_5_7TeV=4,pdfindex_8_7TeV=2,pdfindex_2_7TeV=4,pdfindex_9_7TeV=2,pdfindex_1_7TeV=4,pdfindex_3_7TeV=5,pdfindex_10_7TeV=2,pdfindex_6_7TeV=2,pdfindex_11_8TeV=2,pdfindex_9_8TeV=3,pdfindex_13_8TeV=3,pdfindex_12_8TeV=2,pdfindex_0_8TeV=4,pdfindex_10_8TeV=2,pdfindex_8_8TeV=2,pdfindex_7_8TeV=3,pdfindex_6_8TeV=3,pdfindex_2_8TeV=4,pdfindex_5_8TeV=2,pdfindex_1_8TeV=3,pdfindex_4_8TeV=4,pdfindex_3_8TeV=4" -S -q $queue

 # EXPONENTIAL TRUTHS
 python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w $WS -R scan_toy_exponential_$i   --jobs $JOBS -m 125  -t $TOYS \
	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0  --poiPoint=1 --freezeNuisances MH  --expectSignal 1 --setPhysicsModelParameters pdfindex_7_7TeV=1,pdfindex_4_7TeV=1,pdfindex_0_7TeV=3,pdfindex_5_7TeV=3,pdfindex_8_7TeV=1,pdfindex_2_7TeV=3,pdfindex_9_7TeV=1,pdfindex_1_7TeV=3,pdfindex_3_7TeV=4,pdfindex_10_7TeV=1,pdfindex_6_7TeV=1,pdfindex_11_8TeV=1,pdfindex_9_8TeV=2,pdfindex_13_8TeV=2,pdfindex_12_8TeV=1,pdfindex_0_8TeV=3,pdfindex_10_8TeV=1,pdfindex_8_8TeV=1,pdfindex_7_8TeV=2,pdfindex_6_8TeV=2,pdfindex_2_8TeV=3,pdfindex_5_8TeV=1,pdfindex_1_8TeV=2,pdfindex_4_8TeV=2,pdfindex_3_8TeV=3" -S -q $queue

 #LAURENT TRUTHS
 python $WORK/private/tools/hgg-tools/submitStatsHgg.py -M MultiDimFit --runpull -p r --rMin -0.5 --rMax 3.5 -w $WS -R scan_toy_laurent_$i   --jobs $JOBS -m 125  -t $TOYS \
	-O " -s $SEED -S 0 -P r --cminDefaultMinimizerAlgo migrad --minimizerTolerance 0.001 --minimizerStrategy 0  --poiPoint=1 --freezeNuisances MH  --expectSignal 1 --setPhysicsModelParameters pdfindex_7_7TeV=3,pdfindex_4_7TeV=3,pdfindex_0_7TeV=5,pdfindex_5_7TeV=5,pdfindex_8_7TeV=3,pdfindex_2_7TeV=5,pdfindex_9_7TeV=3,pdfindex_1_7TeV=5,pdfindex_3_7TeV=6,pdfindex_10_7TeV=3,pdfindex_6_7TeV=3,pdfindex_11_8TeV=3,pdfindex_9_8TeV=4,pdfindex_13_8TeV=4,pdfindex_12_8TeV=3,pdfindex_0_8TeV=5,pdfindex_10_8TeV=3,pdfindex_8_8TeV=3,pdfindex_7_8TeV=4,pdfindex_6_8TeV=4,pdfindex_2_8TeV=5,pdfindex_5_8TeV=3,pdfindex_1_8TeV=4,pdfindex_4_8TeV=5,pdfindex_3_8TeV=5" -S -q $queue

#done
