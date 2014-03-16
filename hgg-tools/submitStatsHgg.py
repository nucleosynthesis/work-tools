#!/usr/bin/env python

import sys,numpy,os
from optparse import OptionParser

mymasses = []
def cbackmasses(option,opt_str,value,parser):
  value = value.split(",")
  for v in value: mymasses.append(float(v))

Methods = []
def cbackmethods(option,opt_str,value,parser):
  value = value.split(",")
  for v in value: Methods.append(v.strip())

# UserInput
parser=OptionParser()
parser.add_option("-w","--workspace",type='str',help="Workspace for combine")
parser.add_option("-M","--methods",action="callback",callback=cbackmethods,type="string",help="Methods to be run in combine (comma separate)")
parser.add_option("-m","--masses",action="callback",callback=cbackmasses,type='string',help="Masses to run at (comma separate)")
parser.add_option("-l","--mHMin",default=110, type='float',help="Minimum mH (masses will replace it)")
parser.add_option("-u","--mHMax",default=150, type='float',help="Maximum mH (masses will replace it)")
parser.add_option("-s","--mHStep",default=0.5, type='float',help="mH step")
parser.add_option("-e","--expected",default=False,action='store_true',help="Run expected, mu=val, result. Default will be 1")
parser.add_option("","--noscan",default=False,action='store_true',help="For MultiDimFit, just do the best fit")
parser.add_option("","--runpull",default=False,action='store_true',help="For MultiDimFit, just do the deltaNLL")
parser.add_option("-S","--submit",default=False,action='store_true',help="Submit the scripts now")
parser.add_option("-q","--queue",default="8nh",type='str')
parser.add_option("-R","--rundir",default="",type="str",help="Directory for scripts and results")
parser.add_option("-O","--options",default="",type="str",help="Additional Options string")
parser.add_option("-t","--toys",default=0,type="int",help="throw a toy dataset (or use this number of toys from toysfile)")
parser.add_option("-T","--toysFile",default="",type="str",help="Use a toy dataset from this file for expected results")
parser.add_option("","--nCPU",default=1,type='int')


# These options are only for mu scan 
parser.add_option("-p","--poi",type='str', default="r", help="Parameter of interest, if r fix MH, if MH let r float ")
parser.add_option("-r","--rVal",default=1.0, type='float',help="mu value (for asimov throws)")
parser.add_option("","--rMin",default=0.,type='float')
parser.add_option("","--rMax",default=5.,type='float')
parser.add_option("","--points",default=20,type='int')
parser.add_option("","--jobs",default=-1,type='int')
(options,args)=parser.parse_args()

if options.runpull :options.noscan=True
if options.jobs==-1 :options.jobs=options.points # not can use this to run toys multiplied 

if options.jobs>options.points and not options.noscan: sys.exit("Cannot have more jobs than LH scan points")

if options.toysFile and not (options.expected or options.toys>0 or "Asimov" in Methods): 
  sys.exit("toys file only intended for expected result")

def writeScript(job,cmdline,rdir,name):
  
  setup = """set -x\n
cd %s\n
eval `scramv1 runtime -sh`\n
cd -\n
mkdir scratch\n
cd scratch\n
cp -p $CMSSW_BASE/bin/slc5_amd64_gcc472/combine . \n
cp -p %s/%s .\n"""%(rdir,os.getcwd(),options.workspace)
  if options.toysFile: 
   setup+="cp -p %s/%s . \n"%(os.getcwd(),options.toysFile)
   cmdline += " --toysFile %s "%(options.toysFile)
  job.write(setup)
  job.write("./combine %s "%(options.workspace)+cmdline+"\n")
  if options.toysFile : job.write("rm %s\n"%options.toysFile)
  job.write("hadd -f %s.root higgsCombineTest* \n"%(name))
  job.write("cp -f %s.root %s \n"%(name,rdir))
  job.write("cd ../ \n")
  job.write("rm -r scratch\n")
  job.write("echo 'DONE'\n")

masses = numpy.arange(options.mHMin,options.mHMax+options.mHStep,options.mHStep)
if len(mymasses)>0: masses = mymasses
# Now setup to write the submission scripts
allowedMethods = {
		"MultiDimFit":"prop"
		,"Asymptotic":"search"
		,"AsymptoticGrid":"search"
		,"MaxLikelihoodFit":"search"
		,"ProfileLikelihood":"search"
		}

for M in Methods: 
	if M not in allowedMethods.keys(): sys.exit("No method known -- %s"%(M))
if "MultiDimFit" in Methods and len(masses)>1 : sys.exit("Cannot run MultiDimFit at more than 1 mass")

runDirectory = os.getcwd()+"/"+options.rundir
if options.rundir: os.system("mkdir -p %s"%(options.rundir))
for M in Methods: 
	os.system("mkdir -p %s/%s"%(runDirectory,M))

# write the sumbission scripts
if not options.submit:
 for M in Methods:
  ext=""
  if options.expected: ext = "expected"
  rdir = runDirectory+"/"+M

  print "Writing scripts for --",M,ext

  if allowedMethods[M]=="prop":
	if options.poi=="MH": print "Warning -- you must be running with floatingHiggsMass workspace to run MH as poi"
	rdir+=("/"+options.poi)
	os.system("mkdir -p %s"%rdir)	
	
	tperjob=int(options.points/options.jobs)
	fpoint=0

	for i in range(options.jobs):
	  lpoint=fpoint+(tperjob-1)
	  if options.poi == "r": 
	  	if options.noscan: 
			#cmdline = """ -M MultiDimFit --X-rtd ADDNLL_FASTEXIT --cminDefaultMinimizerType Minuit2 -m %g  """%(masses[0]) 
			cmdline = """ -M MultiDimFit --cminDefaultMinimizerType Minuit2 -m %g  """%(masses[0]) 
			if options.runpull : cmdline+=" --algo deltaNLL "
		else: 
			#cmdline = """ -M MultiDimFit --X-rtd ADDNLL_FASTEXIT --algo grid --points %d  --cminDefaultMinimizerType Minuit2 -m %g  --setPhysicsModelParameterRanges %s=%g,%g """%(options.points,masses[0],options.poi,options.rMin,options.rMax)
			cmdline = """ -M MultiDimFit  --algo grid --points %d  --cminDefaultMinimizerType Minuit2 -m %g  --setPhysicsModelParameterRanges %s=%g,%g """%(options.points,masses[0],options.poi,options.rMin,options.rMax)
	  elif options.poi=="MH":
	  	if options.noscan: 
	 	  #cmdline = """ -M MultiDimFit --X-rtd ADDNLL_FASTEXIT  --cminDefaultMinimizerType Minuit2 -m %g  """%(masses[0])
	 	  cmdline = """ -M MultiDimFit  --cminDefaultMinimizerType Minuit2 -m %g  """%(masses[0])
		  if options.runpull : cmdline+=" --algo deltaNLL "
		else: 
	 	  #cmdline = """ -M MultiDimFit --X-rtd ADDNLL_FASTEXIT --algo grid --points %d  --cminDefaultMinimizerType Minuit2 -m %g  --setPhysicsModelParameterRanges %s=%g,%g --redefineSignalPOIs r,MH --poi %s --floatOtherPOIs 1 """%(options.points,masses[0],options.poi,options.rMin,options.rMax,options.poi)
	 	  cmdline = """ -M MultiDimFit --algo grid --points %d  --cminDefaultMinimizerType Minuit2 -m %g  --setPhysicsModelParameterRanges %s=%g,%g --redefineSignalPOIs r,MH --poi %s --floatOtherPOIs 1 """%(options.points,masses[0],options.poi,options.rMin,options.rMax,options.poi)

          # poi is something else or its 2D 
          #else: cmdline = """ -M  MultiDimFit --X-rtd ADDNLL_FASTEXIT --algo grid --points %d  --cminDefaultMinimizerType Minuit2 -m %g """%(options.points,masses[0])
          else: cmdline = """ -M  MultiDimFit  --algo grid --points %d  --cminDefaultMinimizerType Minuit2 -m %g """%(options.points,masses[0])
	  finame = "%s/sub_%s_%d.sh"%(rdir,M+ext,i)
  	  fi = open(finame,"w")
  	  if not options.noscan: cmdline += " --firstPoint %d  --lastPoint %d "%(fpoint,lpoint)
	  cmdline += options.options
	  if options.expected>0:
		#cmdline+=" -t -1 --toysFrequentist --expectSignal %g "%(options.rVal)
		cmdline+=" -t -1 --expectSignal %g "%(options.rVal)
		if options.poi=="MH": cmdline+=" --expectSignalMass %g "%(masses[0])
	  if options.toys>0 and not options.expected: cmdline+= " -t %d "%(options.toys)
	  writeScript(fi,cmdline,rdir,"res_%s_%d"%(M+ext,i))
          os.system("chmod 755 %s"%(finame))
	  fpoint = lpoint+1 

  else: 
    if M=="Asymptotic" : ext=""
    for m in masses:
	if M=="AsymptoticGrid" : 
#	  os.system("mkdir -p %s/%g"%(rdir,m))
	  ncpu = options.nCPU
	  opttuple = (options.workspace,m,options.points,options.rMin,options.rMax,ncpu,rdir)
	  line = " -w %s -m %.1f -n %d -l -r %g %g --runLimit --nCPU %d --directory %s "%opttuple
#	  line = " -w %s -m %.1f -n %d -l -r %g %g --directory %s "%opttuple
	  if options.options : os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/makeAsymptoticGrid.py %s -O ' %s ' "%(line,options.options))
	  else: os.system("python $CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/test/makeAsymptoticGrid.py %s "%(line))
	else: 
	  finame = "%s/sub_%s_%.2f.sh"%(rdir,M+ext,m)
  	  fi = open(finame,"w")
	  cmdline = """ -M %s -m %g --cminDefaultMinimizerType Minuit2"""%(M,m)
	  if options.expected and M!="Asymptotic": 
		cmdline+=" -t -1  --expectSignal %g "%options.rVal  # this should also have --toysFrequentist but its broken!
	  if M=="ProfileLikelihood" : cmdline+= " --signif --pval " 
	  if M=="MaxLikelihoodFit": cmdline+=" --rMin -10 "
	  cmdline += " %s "%options.options
	  writeScript(fi,cmdline,rdir,"res_%s_%.2f"%(M+ext,m))
          os.system("chmod 755 %s"%(finame))

 print "Finished Writing Scripts"

# Now run through and submit if submit flag is on
else:
 for M in Methods:

  ext=""
  if options.expected: ext = "expected"
  rdir = runDirectory+"/"+M

  if allowedMethods[M]=="prop":
   rdir+=("/"+options.poi)
   for i in range(options.jobs):
   	  finame = "%s/sub_%s_%d.sh"%(rdir,M+ext,i)
  	  if os.path.isfile(finame): os.system("bsub -q %s -o %s.log %s"%(options.queue,finame,finame))
  	  else : print "Expected to find file, %s, skipping"%finame
  else:
    if M=="Asymptotic" : ext=""
    for m in masses:
	  addsub = ''
	  if M=="AsymptoticGrid": 
		finame  =  "%s/limitgrid_%.1f.sh"%(rdir,m)
		addsub = ' -n %d  -R "span[hosts=1] -X " '%options.nCPU if options.nCPU>1  else ""
	  else : 
		finame = "%s/sub_%s_%.2f.sh"%(rdir,M+ext,m)
		addsub = "" 
  	  if os.path.isfile(finame): os.system("bsub -q %s %s -o %s.log %s "%(options.queue,addsub,finame,finame))
  	  else : print "Expected to find file, %s, skipping"%finame

 print "Finished Submitting"  
