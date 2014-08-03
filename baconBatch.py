#!/usr/bin/env python

# baconBatch.py #############################################################################
# Python driver for Bacon Analyzer executable
# Original Author N.Wardle (CERN) 

# TODO : Provide output support to EOS
# For now assume output is small enough to store locally. 
# ------------------------------------------------------------------------------------

import sys, commands, os, fnmatch
from optparse import OptionParser
from optparse import OptionGroup
from numpy import arange
from itertools import product
#from BaconAna.Utils.makeFilelist import *
from makeFilelist import *

# I want to make jobs out of ANY executable and separate based on groups of files or [list] input parameters. Also need the input swap to be as generic as possible

# Ok this is dangerous since we pretty much have to assume some arguments for the exec
# Take WAnalysis as the standard command line style
# 'maxevents, input, isGen
#default_args = ['10000000','nothing.root','1'] #,output.root -> could add to analyzer
default_args = []

# Options
parser = OptionParser()
parser = OptionParser(usage="usage: %prog analyzer outputfile [options] \nrun with --help to get list of options")
parser.add_option("-d","--directory",default='',help="Pick up files from a particular directory. can also pass from /eos/. Will initiate split by files (note you must also pass which index the file goes to)")
parser.add_option("-o","--outdir",default='bacon',help="output for analyzer. This will always be the output for job scripts.")
parser.add_option("-a","--args",dest="args",default=[],action="append",help="Pass executable args n:arg OR named arguments name:arg. Multiple args can be passed with <val1,val2...> or lists of integers with [min,max,stepsize]")
parser.add_option("-v","--verbose",dest="verbose",default=False,action="store_true",help="Spit out more info")
parser.add_option("","--blacklist",dest="blacklist",default=[],action="append",help="Add blacklist file types (search for this string in files and ignore them")

# Make batch submission scripts options
parser.add_option("-n","--njobs",dest="njobs",type='int',default=1,help="Split into n jobs, will automatically produce submission scripts")
parser.add_option("-q","--queue",default='1nh',help="submission queue")

parser.add_option("--dryRun",default=False,action="store_true",help="Do nothing, just create jobs if requested")

# Monitor options (submit,check,resubmit failed)  -- just pass outodir as usual but this time pass --monitor sub --monitor check or --monitor resub
parser.add_option("--monitor",default='',help="Monitor mode (sub/resub/check directory of jobs)")

cwd = os.getcwd()
(options,args) = parser.parse_args()
if len(args)<2 and not options.monitor: sys.exit('Error -- must specify ANALYZER and OUTPUTNAME' )
njobs = options.njobs

def write_job(exec_line, out, analyzer, i, n):

	cwd = os.getcwd()
	sub_file = open('%s/sub_%s_job%d.sh'%(out,analyzer,i),'w')
	sub_file.write('#!/bin/bash\n')
	sub_file.write('# Job Number %d, running over %d files \n'%(i,n))
	sub_file.write('touch %s.run\n'%os.path.abspath(sub_file.name))
	sub_file.write('cd %s\n'%os.getcwd())
	sub_file.write('eval `scramv1 runtime -sh`\n')
	sub_file.write('cd -\n')
	sub_file.write('mkdir -p scratch\n')
	sub_file.write('cd scratch\n')
	#sub_file.write('cp -p $CMSSW_BASE/bin/$SCRAM_ARCH/%s .\n'%analyzer)
	sub_file.write('cp -p %s/%s .\n'%(cwd,analyzer))
	sub_file.write('mkdir -p %s\n'%(out))

	sub_file.write('if ( %s ) then\n'%exec_line)
	sub_file.write('\t hadd -f Output_job%d.root %s/*.root \n'%(i,(out)))
	sub_file.write('\t mv Output_job*.root %s\n'%os.path.abspath(out))
	sub_file.write('\t rm -rf ./bacon ./Output_job* \n')
	sub_file.write('\t touch %s.done\n'%os.path.abspath(sub_file.name))
	sub_file.write('else\n')
	sub_file.write('\t touch %s.fail\n'%os.path.abspath(sub_file.name))
	sub_file.write('fi\n')
	sub_file.write('rm -f %s.run\n'%os.path.abspath(sub_file.name))
	sub_file.close()
	os.system('chmod +x %s'%os.path.abspath(sub_file.name))
  
def submit_jobs(lofjobs):
   for sub_file in lofjobs:
    os.system('rm -f %s.done'%os.path.abspath(sub_file))
    os.system('rm -f %s.fail'%os.path.abspath(sub_file))
    os.system('rm -f %s.log'%os.path.abspath(sub_file))
    os.system('bsub -q %s -o %s.log %s'%(options.queue,os.path.abspath(sub_file),os.path.abspath(sub_file)))
  
if options.monitor: 
  if options.monitor not in ['sub','check','resub']: sys.exit('Error -- Unknown monitor mode %s'%options.monitor)
  dir = options.outdir

  if options.monitor == 'sub' or options.monitor == 'resub': 
    # pick up job scripts in output directory (ends in .sh)
    lofjobs = []
    for root,dirs,files in os.walk(dir):
     for file in fnmatch.filter(files,'*.sh'):
       if options.monitor == 'resub' and not os.path.isfile('%s/%s.fail'%(root,file)): continue
       lofjobs.append('%s/%s'%(os.path.abspath(root),file))
    print 'Submitting %d jobs from directory %s'%(len(lofjobs),dir)
    submit_jobs(lofjobs) 

  if options.monitor == 'check': 
    failjobs = []
    runjobs  = []
    donejobs = []
    number_of_jobs = 0
    for root,dirs,files in os.walk(dir):
     for file in fnmatch.filter(files,'*.sh'):
       if os.path.isfile('%s/%s.fail'%(root,file)): failjobs.append('%s'%file)
       if os.path.isfile('%s/%s.done'%(root,file)):
       		if not '%s.sh'%file in failjobs : donejobs.append('%s'%file)
       if os.path.isfile('%s/%s.run'%(root,file)): runjobs.append('%s'%file)
       number_of_jobs+=1
    print 'Status of jobs directory ', dir
    print '  Total of %d jobs'%number_of_jobs 
    print '  %d in status Fail -> (resub them with --monitor resub)'%len(failjobs)
    for job in failjobs : print '\t %s'%job
    print '  %d in status Running -> '%len(runjobs)
    for job in runjobs : print '\t %s'%job
    print '  %d in status Done -> '%len(donejobs)
    for job in donejobs : print '\t %s'%job

  sys.exit('Finished Monitor -- %s'%options.monitor)

def parse_to_dict(l_list):
  if len(l_list)<1: return {}
  ret = {}
  nkey = 0
  for item in l_list: 
    ni,varg = item.split(':') # should put a try here
    if not '-' in ni: 
    	ni = int(ni)
	nkey+=1
    if not "[" in item and "<" not in item:
     ret[(ni)]=['',[varg]]
    else :
     if "[" in varg:
       varg = varg.replace("[","")
       varg = varg.replace("]","")
       min,max,step = varg.split(",")
       ret[(ni)] = ['',arange(int(min),int(max),int(step))]
     elif "<" in varg:
       varg  = varg.replace("<","")
       varg  = varg.replace(">","")
       largs = varg.split(",")
       ret[(ni)] = ['',largs]
  
  iskey = 0
  for kr in ret.keys():
  	if type(kr)==type(''):
		ll = ret.pop(kr)
		
		ll[1] = [kr+' '+str(l) for l in ll[1]] 
		ret[nkey+iskey]=ll
		iskey+=1
  return ret

def getFilesJob(dirin,job,njobs):
  if njobs == 1 : 
  	njobs = -1
	job = 0
  infiles = []
  if "," in dirin : alldirs = dirin.split(',')
  else : alldirs=[dirin]
  infiles = []
  for dir in alldirs:
    if '/store/' in dir : infiles.extend(makeCaFiles(dir,options.blacklist,njobs,job))
    else : infiles.extend(makeFiles(dir,options.blacklist,njobs,job))
  if options.verbose: print "VERB -- Found following files for dir %s --> "%dir, infiles
  return infiles

def getArgsJob(interationsobject,job_id,njobs):
   injobs = []
#   nf = 0
   ifile = 0
   for ff in iterationsobject:
     if (njobs > 0) and (ifile % njobs != job_id):
        injobs.append((ff,False))
     else:
        injobs.append((ff,True))
     ifile += 1

   return injobs

# -- MAIN
os.system('mkdir -p %s/%s'%(cwd,options.outdir)) 

mindeces   = []
analyzer   = args[0]
outfile = args[1]
analyzer_args = parse_to_dict(options.args)
exec_line = './%s'%analyzer

if options.directory :
  filepos,options.directory = options.directory.split(':')
  analyzer_args[int(filepos)]=['',"fileinput"]

#for arg_i,arg in enumerate(default_args):
#  if arg_i in analyzer_args.keys(): 
#  	arg = analyzer_args[arg_i]
#	if type(arg)==type(list): exec_line+= ' MULTARG_%d '%arg_i
#  exec_line+=' %s '%arg

# NEED TO ITERATE OF MAP OF ARGS, FORGET DEFAULT ARGGS I THINK, forec them set!!!!!
#for arg_i,arg in enumerate(default_args):
sortedkeys = analyzer_args.keys()
if len(sortedkeys): sortedkeys.sort()

for key in sortedkeys:
#  if arg_i in analyzer_args.keys(): 
  	arg = analyzer_args[key][1]
	if arg=='fileinput':
		exec_line+= ' fileinput '
	elif    len(arg)>1: 
		mindeces.append(key)
		exec_line+= ' MULTARG_%d '%key
	else:  exec_line+=' %s '%arg[0]


# check that from max to 0 all arguments are accounted for (could always add defaults above) !
for arg_c in range(0,max(analyzer_args.keys())):
  if arg_c not in analyzer_args.keys(): sys.exit("ERROR -- missing argument %d"%arg_c)

print 'running executable -- (default call) \n\t%s'%exec_line

if not options.dryRun and njobs > 1:
	print 'Writing %d Submission Scripts to %s (submit after with --monitor sub)'%(njobs,options.outdir)


for job_i in range(njobs):
 ################################ WHY does this need to be recreate?
 # This must be the sorted set of keys from the dictionary to build the iterations
 listoflists = [analyzer_args[k][1] for k in sortedkeys ]
 #itertools section, make object containing all args to be considered
 #i.e it iterates over all combinations of arguments in the args list 
 iterationsobject = product(*listoflists)
 ################################
 if options.directory:          files = getFilesJob(options.directory,job_i,njobs)
 else: files = getArgsJob(iterationsobject,job_i,njobs)# use itertools to split up any arglists into jobs 
 #else: files=[]
 job_exec = ''
 

 nfiles_i = 0
 for fil_i,fil in enumerate(files):
   #if options.directory : 
   if not fil[1]: continue
   if options.directory: exec_line_i = exec_line.replace('fileinput'," "+fil[0]+" ")
   else: 
    exec_line_i = exec_line
    for i,m in enumerate(fil[0]):  # no defaults so guarantee (make the check) that all of the args are there)  
		exec_line_i = exec_line_i.replace(" MULTARG_%d "%i," "+str(m)+" " ) #LIST  OVER iterated arguments and produce and replace MULTIARG_i with arguemnt at i in list ?
   job_exec+=exec_line_i+'; mv %s %s/%s_job%d_file%d.root; '%(outfile,options.outdir,outfile,job_i,fil_i) 
   nfiles_i += 1
 if options.verbose: print "VERB -- job exec line --> ",job_exec

 if options.dryRun : 
 	print 'job %d/%d -> '%(job_i+1,njobs), job_exec
 elif njobs > 1: 
   write_job(job_exec, options.outdir, analyzer, job_i, nfiles_i)
 else: os.system(job_exec) 
