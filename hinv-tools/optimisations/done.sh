#!/bin/bash

mkdir full nosys nosysSR

for maxdphicut in 3.1416 2.8 2.5 2.1 1.8 1.5 1.2 0.9 0.6 0.3
do 
	root -l -b -q 'plottingtons.C('${maxdphicut}',"alllims_full.root","full")'
	root -l -b -q 'plottingtons.C('${maxdphicut}',"alllims_no_sys.root","full")'
	root -l -b -q 'plottingtons.C('${maxdphicut}',"alllims_no_sys_SR.root","full")'

done
python plot1D.py alllims_no_sys.root   0.1 0.3 nosys/opt_no_sys
python plot1D.py alllims_no_sys_SR.root  0.05 0.27 nosysSR/opt_no_sys_no_SR
python plot1D.py alllims_full.root 0 1.4 full/opt_full
