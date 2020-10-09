#!/bin/sh
set -x
set -e

mkdir work-tools; cd work-tools
git init
git remote add origin https://github.com/nucleosynthesis/work-tools
git config core.sparsecheckout true; 
 echo hinv-tools/QCDEstimate >> .git/info/sparse-checkout
git pull origin master
cd hinv-tools
git fetch origin
