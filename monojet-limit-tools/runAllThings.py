import ROOT 
import sys,os 

from itertools import product

mmed  = [50,60,70,80,90,100,125,150,175,200,300,325,400,525,600,725,800,925,1000,1125,1200,1325,1400,1525,1600,1725,1800,1925,2000,2500,3000,3500,4000,5000]
mmedS = [10,20,30,40,50,60,70,80,90,100,125,150,175,200,300,325,400,525,600,725,800,925,1000,1125,1200,1325,1400,1525,1600,1725,1800,1925,2000,2500,3000,3500,4000,5000]
mdm  = [1,5,10,25,50,100,150,200,300,400,500,600,700,800,900,1000,1250,1500,1750,2000]
expV  = [ '800%04d%04d'%(i,j) for i,j in product(mmed,mdm) ] 
expA  = [ '801%04d%04d'%(i,j) for i,j in product(mmed,mdm) ] 
expP  = [ '806%04d%04d'%(i,j) for i,j in product(mmedS,mdm) ] 
expS  = [ '805%04d%04d'%(i,j) for i,j in product(mmedS,mdm) ] 

# make a crazy string 
striA = ",".join(expA)
striP = ",".join(expP)
striV = ",".join(expV)
striS = ",".join(expS)

# For each plot, dive into the signal file and calculate the number of signal events (expected)

opts = " --freezeNuisances sigscale --setPhysicsModelParameters sigscale="

#os.system('combineTool.py -M Asymptotic combined_card.txt -m %s --job-mode lxbatch --task-name "Adish_FULLMU_AXIAL"   	   -n MU %s1  --sub-opts "-q 1nh " --merge 30 --cl 0.90  '%(striA,opts))
#os.system('combineTool.py -M Asymptotic combined_card.txt -m %s --job-mode lxbatch --task-name "Adish_FULLMU_VECTOR"       -n MU %s1  --sub-opts "-q 1nh " --merge 30 --cl 0.90  '%(striV,opts))
#os.system('combineTool.py -M Asymptotic combined_card_ps.txt -m %s --job-mode lxbatch --task-name "Adish_FULLMU_PSEUDOSCALAR" -n MU %s1  --sub-opts "-q 1nh " --merge 30 --cl 0.90  '%(striP,opts))
#os.system('combineTool.py -M Asymptotic combined_card_ps.txt -m %s --job-mode lxbatch --task-name "Adish_FULLMU_SCALAR"       -n MU %s1  --sub-opts "-q 1nh " --merge 30 --cl 0.90  '%(striS,opts))


#os.system('mkdir -p CENTRAL; cd CENTRAL')
#os.system('combineTool.py -M Asymptotic combined_card.txt -m %s --job-mode lxbatch --task-name "Adish_CENTRAL_AXIAL"        -n CENTRAL %s1  --sub-opts "-q 1nh " --merge 30  --singlePoint 1'%(striA,opts))
#os.system('combineTool.py -M Asymptotic combined_card.txt -m %s --job-mode lxbatch --task-name "Adish_CENTRAL_VECTOR"       -n CENTRAL %s1  --sub-opts "-q 1nh " --merge 30  --singlePoint 1'%(striV,opts))
#os.system('combineTool.py -M Asymptotic combined_card_ps.txt -m %s --job-mode lxbatch --task-name "Adish_CENTRAL_PSEUDOSCALAR" -n CENTRAL %s1  --sub-opts "-q 1nh " --merge 10  --singlePoint 1'%(striP,opts))
os.system('combineTool.py -M Asymptotic combined_card_ps.txt -m %s --job-mode lxbatch --task-name "Adish_CENTRAL_SCALAR"       -n CENTRAL %s1  --sub-opts "-q 1nh " --merge 10  --singlePoint 1'%(striS,opts))


# repeat but for scale up/down
#os.system('cd ../')
#os.system('mkdir -p SCALEUP; cd SCALEUP')
#os.system('combineTool.py -M Asymptotic combined_card.txt -m %s --job-mode lxbatch --task-name    "Adish_UP_AXIAL"   -n SCALEUP     %s1.2  --sub-opts "-q 1nh" --singlePoint 1 --merge 30'%(striA,opts))
#os.system('combineTool.py -M Asymptotic combined_card.txt -m %s --job-mode lxbatch --task-name    "Adish_UP_VECTOR"  -n SCALEUP     %s1.2  --sub-opts "-q 1nh" --singlePoint 1 --merge 30'%(striV,opts))
#os.system('combineTool.py -M Asymptotic combined_card_ps.txt -m %s --job-mode lxbatch --task-name "Adish_UP_SCALAR"        -n SCALEUP  %s1.3  --sub-opts "-q 1nh" --singlePoint 1 --merge 30'%(striS,opts))
#os.system('combineTool.py -M Asymptotic combined_card_ps.txt -m %s --job-mode lxbatch --task-name "Adish_UP_PSEUDOSCALAR"  -n SCALEUP  %s1.3  --sub-opts "-q 1nh" --singlePoint 1 --merge 30'%(striP,opts))

#os.system('cd ../')
#os.system('mkdir -p SCALEDN; cd SCALEDN')
#os.system('combineTool.py -M Asymptotic combined_card.txt -m %s --job-mode lxbatch --task-name  "Adish_DN_AXIAL"     -n SCALEDN  %s0.8  --sub-opts "-q 1nh" --singlePoint 1 --merge 30'%(striA,opts))
#os.system('combineTool.py -M Asymptotic combined_card.txt -m %s --job-mode lxbatch --task-name  "Adish_DN_VECTOR"    -n SCALEDN  %s0.8  --sub-opts "-q 1nh" --singlePoint 1 --merge 30'%(striV,opts))
#os.system('combineTool.py -M Asymptotic combined_card_ps.txt -m %s --job-mode lxbatch --task-name  "Adish_DN_SCALAR"       -n SCALEDN  %s0.7  --sub-opts "-q 1nh" --singlePoint 1 --merge 30'%(striS,opts))
#os.system('combineTool.py -M Asymptotic combined_card_ps.txt -m %s --job-mode lxbatch --task-name  "Adish_DN_PSEUDOSCALAR" -n SCALEDN  %s0.7  --sub-opts "-q 1nh" --singlePoint 1 --merge 30'%(striP,opts))

#os.system('combineTool.py -M ProfileLikelihood combined_card.txt --significance -m %s --job-mode lxbatch --task-name "Adish_PL_AXIAL"        --toysFreq -t -1 --expectSignal 1 %s1 --merge 30 --sub-opts "-q 1nh"'%(striA,opts))
#os.system('combineTool.py -M ProfileLikelihood combined_card.txt --significance -m %s --job-mode lxbatch --task-name "Adish_PL_VECTOR"       --toysFreq -t -1 --expectSignal 1 %s1 --merge 30 --sub-opts "-q 1nh"'%(striV,opts))
#os.system('combineTool.py -M ProfileLikelihood combined_card_ps.txt --significance -m %s --job-mode lxbatch --task-name "Adish_PL_SCALAR"       --toysFreq -t -1 --expectSignal 1 %s1 --merge 30 --sub-opts "-q 1nh"'%(striS,opts))
#os.system('combineTool.py -M ProfileLikelihood combined_card_ps.txt --significance -m %s --job-mode lxbatch --task-name "Adish_PL_PSEUDOSCALAR" --toysFreq -t -1 --expectSignal 1 %s1 --merge 30 --sub-opts "-q 1nh"'%(striP,opts))

