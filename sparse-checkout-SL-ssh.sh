#!/bin/sh
set -x
set -e

mkdir stats-tools; cd stats-tools
git init
git remote add origin https://github.com/nucleosynthesis/work-tools
git config core.sparsecheckout true; 
 echo stats-tools/simplifiedLikelihood.C >> .git/info/sparse-checkout
 echo stats-tools/makeLHInputs.py >> .git/info/sparse-checkout
git pull origin master
popd
