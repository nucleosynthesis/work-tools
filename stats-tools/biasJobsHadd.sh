#!/bin/bash
what=$1
#hadd -f res_$what.root 	run1/scan_toy_$what\_/MultiDimFit/r/res* run2/scan_toy_$what\_/MultiDimFit/r/res* 
hadd -f res_$what.root 	scan_toy_$what\_/MultiDimFit/r/res* 
python makePull.py res_$what.root pull_$what.root
