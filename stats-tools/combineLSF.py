#!/usr/bin/env python

# A Tool to submit jobs for likelihood scans with MultiDimFit
# monitor allows to submit, check, resub jobs to batch

import ROOT
import os
import numpy
import sys
import fnmatch
from copy import deepcopy as copy

from optparse import OptionParser
from optparse import OptionGroup

from Queue import Queue

from threading import Thread, Semaphore
from multiprocessing import cpu_count

end = ".txt"
class Wrap:
    def __init__(self, func, args, queue):
        self.queue = queue
        self.func = func
        self.args = args
        
    def __call__(self):
        ret = self.func( *self.args )
        self.queue.put( ret  )

    
class Parallel:
    def __init__(self,ncpu):
        self.running = Queue(ncpu)
        self.returned = Queue()
	self.njobs = 0
	
    def run(self,cmd,args):
        wrap = Wrap( self, (cmd,args), self.returned )
	self.njobs += 1
        thread = Thread(None,wrap)
        thread.start()
        
    def __call__(self,cmd,args):
        if type(cmd) == str:
            print cmd
            for a in args:
                cmd += " %s " % a
            args = (cmd,)
            cmd = commands.getstatusoutput
        self.running.put((cmd,args))
        ret = cmd( *args ) 
        self.running.get()
        self.running.task_done()
        return ret


parser = OptionParser()
parser.add_option("-d","--datfile",help="Pick up running options from datfile")
parser.add_option("-q","--queue",help="Which batch queue")
parser.add_option("--dryRun",default=False,action="store_true",help="Dont submit")
parser.add_option("--parallel",default=False,action="store_true",help="Run local fits in multithreading")
parser.add_option("--runLocal",default=False,action="store_true",help="Run locally")
parser.add_option("--hadd",help="Trawl passed directory and hadd files. To be used when jobs are complete.")
parser.add_option("-v","--verbose",default=False,action="store_true")
parser.add_option("--monitor",default='',help="Monitor mode - sub/resub/check/resub-missing directory of jobs (from --outDir) ")
specOpts = OptionGroup(parser,"Specific options")
specOpts.add_option("--files",default=None)
specOpts.add_option("-o","--outDir",default=None)
specOpts.add_option("--method",default=None)
specOpts.add_option("--wspace",type="str",default=None)
specOpts.add_option("--poi",type="str",default=None)
specOpts.add_option("--jobs",type="int",default=None)
specOpts.add_option("--pointsperjob",type="int",default=1)
specOpts.add_option("--toysFile",default=None)
specOpts.add_option("--additionalOptions",default="",type="string")
parser.add_option_group(specOpts)
(opts,args) = parser.parse_args()

if not os.path.exists(os.path.expandvars('$CMSSW_BASE/bin/$SCRAM_ARCH/combine')):
	sys.exit('ERROR - CombinedLimit package must be installed')
if not os.path.exists(os.path.expandvars('$CMSSW_BASE/bin/$SCRAM_ARCH/text2workspace.py')):
	sys.exit('ERROR - CombinedLimit package must be installed')
if not os.path.exists(os.path.expandvars('$CMSSW_BASE/bin/$SCRAM_ARCH/combineCards.py')):
	sys.exit('ERROR - CombinedLimit package must be installed')

cwd = os.getcwd()

def system(exec_line):
	if opts.verbose: print '\t', exec_line
	os.system(exec_line)

if opts.monitor: 
  if opts.monitor not in ['sub','check','resub','resub-missing','show-fail','show-done','show-run']: sys.exit('Error -- Unknown monitor mode %s'%opts.monitor)
  dir = opts.outDir

  if opts.monitor == 'sub' or opts.monitor == 'resub' or opts.monitor == 'resub-missing': 
    # pick up job scripts in output directory (ends in .sh)
    lofjobs = []
    for root,dirs,files in os.walk(dir):
     for file in fnmatch.filter(files,'*.sh'):
       if opts.monitor == 'resub' and not os.path.isfile('%s/%s.fail'%(root,file)): continue
       elif opts.monitor == 'resub-missing' :
         job_number=int( file[file.find('job'):file.find('.sh')].strip('job') )
	 if 'Job%d.'%job_number in ' '.join(filter(lambda x: '.root' in x, files)): continue
       #lofjobs.append('%s/%s'%(os.path.abspath(root),file))
       fpath = os.path.abspath("%s/%s"%(root,file))
       do_it_system = 'bsub -q %s -o %s.log  < %s'%(opts.queue,fpath,fpath)
       if not opts.dryRun:
         system('rm -f %s/%s.done'%(root,file))
         system('rm -f %s/%s.fail'%(root,file))
         system('rm -f %s/%s.log'%(root,file))
         system(do_it_system)
       elif opts.verbose: print "\t -> ", do_it_system
   # print 'Submitting %d jobs from directory %s'%(len(lofjobs),dir)
   # submit_jobs(lofjobs) 

  if opts.monitor == 'check' or 'show' in opts.monitor: 
    failjobs = []
    runjobs  = []
    donejobs = []
    number_of_jobs = 0
    for root,dirs,files in os.walk(dir):
     for file in fnmatch.filter(files,'*.sh'):
       if os.path.isfile('%s/%s.fail'%(root,file)): failjobs.append('%s/%s'%(root,file))
       if os.path.isfile('%s/%s.done'%(root,file)):
       		if not '%s.sh'%file in failjobs : donejobs.append('%s/%s'%(root,file))
       if os.path.isfile('%s/%s.run'%(root,file)): runjobs.append('%s/%s'%(root,file))
       number_of_jobs+=1
    print 'Status of jobs directory ', dir
    print '  Total of %d jobs'%number_of_jobs 
    if opts.monitor=='show-fail' or 'show' not in opts.monitor:
      print '  %d in status Fail -> (resub them with --monitor resub)'%len(failjobs)
      for job in failjobs : print '\t FAIL %s'%job
    if opts.monitor=='show-run' or 'show' not in opts.monitor:
      print '  %d in status Running -> '%len(runjobs)
      for job in runjobs : print '\t RUN %s'%job
    if opts.monitor=='show-done' or 'show' not in opts.monitor:
      print '  %d in status Done -> '%len(donejobs)
      for job in donejobs : print '\t DONE %s'%job
    print "\n  %d/%d Running, %d/%d Done, %d/%d Failed (resub with --monitor resub)"\
    	%(len(runjobs),number_of_jobs,len(donejobs),number_of_jobs,len(failjobs),number_of_jobs)
		
  sys.exit('Finished Monitor -- %s'%opts.monitor)

if opts.parallel:
    parallel = Parallel(cpu_count())

defaults = copy(opts)

def strtodict(lstr):
	retdict = {}
	if not len(lstr): return retdict
	objects = lstr.split(':')
	for o in objects:
	  k,vs = o.split('[')
	  vs = vs.rstrip(']')
	  vs = vs.split(',')
	  retdict[k] = [float(vs[0]),float(vs[1])]
	return retdict


def writePreamble(sub_file):
	sub_file.write('#!/bin/bash\n')
	sub_file.write('touch %s.run\n'%os.path.abspath(sub_file.name))
	sub_file.write('cd %s\n'%os.getcwd())
	sub_file.write('eval `scramv1 runtime -sh`\n')
	sub_file.write('cd -\n')
	sub_file.write('mkdir -p scratch\n')
	sub_file.write('cd scratch\n')
	sub_file.write('cp -p $CMSSW_BASE/bin/$SCRAM_ARCH/combine .\n')
	#sub_file.write('cp -p %s .\n'%os.path.abspath(opts.datacard))
	sub_file.write('cp -f %s ./DATACARD.root\n'%(os.path.abspath(opts.datacard)))
	#opts.datacard = "DATACARD"
	if opts.toysFile: 
		for f in opts.toysFile.split(','):
			sub_file.write('cp -p %s .\n'%os.path.abspath(f))
	if opts.files:
	  for file in opts.files.split(','):
	  	if file: sub_file.write('cp -p %s .\n'%os.path.abspath(file))

def writePostamble(sub_file, exec_line):

	sub_file.write('if ( %s ) then\n'%exec_line)
	sub_file.write('\t mv higgsCombine*.root %s\n'%os.path.abspath(opts.outDir))
	# Add additional output files?
	sub_file.write('\t touch %s.done\n'%os.path.abspath(sub_file.name))
	sub_file.write('else\n')
	sub_file.write('\t touch %s.fail\n'%os.path.abspath(sub_file.name))
	sub_file.write('fi\n')
	sub_file.write('rm -f %s.run\n'%os.path.abspath(sub_file.name))
	sub_file.close()
	system('chmod +x %s'%os.path.abspath(sub_file.name))
	if not opts.dryRun and opts.queue:
		system('rm -f %s.done'%os.path.abspath(sub_file.name))
		system('rm -f %s.fail'%os.path.abspath(sub_file.name))
		system('rm -f %s.log'%os.path.abspath(sub_file.name))
		system('bsub -q %s -o %s.log %s'%(opts.queue,os.path.abspath(sub_file.name),os.path.abspath(sub_file.name)))
	if opts.runLocal:
		if opts.parallel:
			parallel.run(system,['bash %s'%os.path.abspath(sub_file.name)])
		else:
			system('bash %s'%os.path.abspath(sub_file.name))

	
def writeMultiDimFit(method=None,wsOnly=False):

	print 'Writing MultiDim Scan'
	dname = "DATACARD.root"
	for i in range(opts.jobs):
		file = open('%s/sub_m%1.5g_job%d.sh'%(opts.outDir,getattr(opts,"mh",0.),i),'w')
		writePreamble(file)
		exec_line = 'combine %s -M MultiDimFit --algo=grid  %s --points=%d --firstPoint=%d --lastPoint=%d -n %sJob%d'%(dname,combine_args[method],opts.pointsperjob*opts.jobs,i*opts.pointsperjob,(i+1)*opts.pointsperjob-1,method,i)
		if getattr(opts,"mh",None): exec_line += ' -m %6.2f'%opts.mh
		if opts.additionalOptions: exec_line += ' %s'%opts.additionalOptions
		if opts.toysFile: exec_line += ' --toysFile %s'%opts.toysFile
		if opts.verbose: print '\t', exec_line
		writePostamble(file,exec_line)

	opts.datacard = backupcard 

def run():
	# setup
	opts.outDir=os.path.join(opts.prefix,opts.outDir)
	system('mkdir -p %s'%opts.outDir)
	if opts.verbose: print 'Made directory', opts.outDir
	checkValidMethod()
	# submit
	writeMultiDimFit()

def resetDefaultConfig():
    global opts
    opts = copy(defaults)
    ### for opt in specOpts.option_list:
    ###     opt_name = opt.dest.strip('--')
    ###     if opt_name=='datacard' or opt_name=='files': continue
    ###     else: setattr(opts,opt_name,None)

def configure(config_line):
	# could automate this but makes it easier to read and add options this way
	resetDefaultConfig()
	if opts.verbose: print config_line
	for option in config_line.split():
		if option.startswith('outDir='): opts.outDir = option.split('=')[1]
		if option.startswith('jobs='): opts.jobs = int(option.split('=')[1])
		if option.startswith('pointsperjob='): opts.pointsperjob = int(option.split('=')[1])
		if option.startswith('toysFile='): opts.toysFile = option.split('=')[1]
		if option.startswith('mh='): opts.mh = float(option.split('=')[1])
		if option.startswith('poi='): 
			poiopt = option.split('=')[1]
			if ',' in poiopt:
				opts.poi = " -P ".join(poiopt.split(','))
			else: opts.poi = option.split('=')[1]
		if option.startswith('wspace='): opts.wspace = str(option.split('=')[1])
		if option.startswith('opts='): 
			addoptstr = option.split("=")[1:]
			addoptstr = "=".join(addoptstr)
			opts.additionalOptions =  addoptstr.replace('+',' ')
			opts.additionalOptions = opts.additionalOptions.replace(">"," ")
			opts.additionalOptions = opts.additionalOptions.replace("<"," ")
	if opts.verbose: print opts
	run()

def trawlHadd():
	list_of_dirs=set()
	for root, dirs, files in os.walk(opts.hadd):
		for x in files:
			if 'higgsCombine' in x and '.root' in x: 
				list_of_dirs.add(root)

	for dir in list_of_dirs:
		for root, dirs, files in os.walk(dir):
			list_of_files=''
			for file in fnmatch.filter(files,'higgsCombine*Job*.root'):
				list_of_files += ' '+os.path.join(root,'%s'%file)
			print root, ' -- ', len(list_of_files.split())
			system('mkdir -p tmp_r')

			print list_of_files 
			for fi in list_of_files.split():
			  print fi
			  fif = ROOT.TFile.Open(fi)
			  fin = ROOT.TFile("tmp_r/tmp_%s"%(fi.split('/')[-1]),"RECREATE")
			  tr = fif.Get("limit")
			  fin.WriteTObject(tr)
			  fin.Close(); fif.Close();
			outname = dir.replace('/','_')
			exec_line = 'hadd -f %s/%s.root tmp_r/*'%(dir,outname)
			if opts.verbose: print exec_line
			system(exec_line)
			system('rm -rf tmp_r')

if opts.hadd:
	trawlHadd()

elif opts.datfile:
	datfile = open(opts.datfile)
	for line in datfile.readlines():
		line=line.strip('\n')
		if line.startswith('#') or len(line)==0: 
			continue
		if line.startswith('files'):
			opts.files = line.split('=')[1]
                        defaults.files = opts.files
			continue
		configure(line)

else:
	# default setup here
	print 'Not yet implemented'
        
if opts.parallel:
    for i in range(parallel.njobs):
	print parallel.returned.get()
        
