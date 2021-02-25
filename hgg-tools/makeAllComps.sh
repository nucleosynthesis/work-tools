#!/bin/bash

scanBestFits.py --poi r_ttH MultiPdf/mvaComb/Discrete/RProcScan_ttH/MultiPdf_mvaComb_Discrete_RProcScan_ttH.root -f -o ttH_cats
scanBestFits.py --poi r_ggH MultiPdf/mvaComb/Discrete/RProcScan_ggH/MultiPdf_mvaComb_Discrete_RProcScan_ggH.root -f -o ggH_cats
scanBestFits.py --poi r_VH MultiPdf/mvaComb/Discrete/RProcScan_VH/MultiPdf_mvaComb_Discrete_RProcScan_VH.root -f -o VH_cats
scanBestFits.py --poi r_qqH MultiPdf/mvaComb/Discrete/RProcScan_qqH/MultiPdf_mvaComb_Discrete_RProcScan_qqH.root -f -o qqH_cats

scanBestFits.py --poi r_ttH MultiPdf/mvaComb/NoDiscrete/RProcScan_ttH/MultiPdf_mvaComb_NoDiscrete_RProcScan_ttH.root -f -o ttH_cats_F
scanBestFits.py --poi r_ggH MultiPdf/mvaComb/NoDiscrete/RProcScan_ggH/MultiPdf_mvaComb_NoDiscrete_RProcScan_ggH.root -f -o ggH_cats_F
scanBestFits.py --poi r_VH MultiPdf/mvaComb/NoDiscrete/RProcScan_VH/MultiPdf_mvaComb_NoDiscrete_RProcScan_VH.root -f -o VH_cats_F
scanBestFits.py --poi r_qqH MultiPdf/mvaComb/NoDiscrete/RProcScan_qqH/MultiPdf_mvaComb_NoDiscrete_RProcScan_qqH.root -f -o qqH_cats_F

plotMultipleLHCurves.py MultiPdf/mvaComb/NoDiscrete/RProcScan_ggH/MultiPdf_mvaComb_NoDiscrete_RProcScan_ggH.root MultiPdf/mvaComb/Discrete/RProcScan_ggH/MultiPdf_mvaComb_Discrete_RProcScan_ggH.root -x r_ggH -o plot_ggH --yr 0:9 --labels "Fixed Choice,Profiled Choice"  -L -b -v 
plotMultipleLHCurves.py MultiPdf/mvaComb/NoDiscrete/RProcScan_qqH/MultiPdf_mvaComb_NoDiscrete_RProcScan_qqH.root MultiPdf/mvaComb/Discrete/RProcScan_qqH/MultiPdf_mvaComb_Discrete_RProcScan_qqH.root -x r_qqH -o plot_qqH --yr 0:9 --labels "Fixed Choice,Profiled Choice"  -L -b -v
plotMultipleLHCurves.py MultiPdf/mvaComb/NoDiscrete/RProcScan_VH/MultiPdf_mvaComb_NoDiscrete_RProcScan_VH.root MultiPdf/mvaComb/Discrete/RProcScan_VH/MultiPdf_mvaComb_Discrete_RProcScan_VH.root -x r_VH -o plot_VH --yr 0:9 --labels "Fixed Choice,Profiled Choice"  -L -b -v
plotMultipleLHCurves.py MultiPdf/mvaComb/NoDiscrete/RProcScan_ttH/MultiPdf_mvaComb_NoDiscrete_RProcScan_ttH.root MultiPdf/mvaComb/Discrete/RProcScan_ttH/MultiPdf_mvaComb_Discrete_RProcScan_ttH.root -x r_ttH -o plot_ttH --yr 0:9 --labels "Fixed Choice,Profiled Choice"  -L -b -v
