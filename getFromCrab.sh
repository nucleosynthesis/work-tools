#!/bin/bash
# run with 
# ./getFromCrab crab_folder 
BASE=${PWD}
#BFOLDER=$2
cd $BASE
#source /cvmfs/cms.cern.ch/crab3/crab.sh; 
#eval `scramv1 runtime -sh`

TIME=$(crab status $1 | grep "Task name" | cut -d ':' -f 2 | xargs)
BFOLDER=$(cat $1/crab.log | grep "outputPrimaryDataset" | cut -d "=" -f 2- | tr -d "'" | xargs)
FOLDER=$(crab status $1 | grep "Task name" | cut -d ':' -f 3 | xargs)
echo $BFOLDER/$FOLDER/
echo $TIME
prefix="nckw_crab_"
FOLDER=${FOLDER#"$prefix"}
ext=""

LOC="/store/user/nckw/${BFOLDER}/${FOLDER}/${TIME}/0000/"

#echo $(xrdfs root://gfe02.grid.hep.ph.ic.ac.uk:1097/store/ ls ${LOC})
#echo ${LOC}
#exit 
echo $LOC
RANDOMFILE=out_$RANDOM

mkdir -p output_crab/${BFOLDER}/$1
cd /tmp/nckw/
mkdir $RANDOMFILE
cd $RANDOMFILE
for FILE in $(xrdfs root://gfe02.grid.hep.ph.ic.ac.uk:1097/store/ ls ${LOC} | grep combine_output_); do
  xrdcp root://gfe02.grid.hep.ph.ic.ac.uk:1097/${FILE} .
done
for FILE in $(ls combine_out*.tar); do tar -xvf ${FILE}; done 
hadd -f output_${FOLDER}.root higgsCombine${ext}*.root 
mv output_${FOLDER}.root $BASE/output_crab/${BFOLDER}/$1
rm -f higgsCombine* *.tar
cd /tmp/nckw
rmdir $RANDOMFILE
exit 


