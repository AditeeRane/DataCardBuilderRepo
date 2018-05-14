#! /usr/bin/env python
import os
import glob
import math
from array import array
import sys
import time

#import ROOT
from ROOT import *
############################################
#            Job steering                  #
############################################
from optparse import OptionParser
parser = OptionParser()
parser.add_option('--fastsim', action='store_true', dest='fastsim', default=False, help='use fastsim signal (default = %default)')
parser.add_option('--keeptar', action='store_true', dest='keeptar', default=False, help='keep old tarball for condor jobs (default = %default)')
parser.add_option("--model", dest="model", default = "T1bbbb",help="SMS model", metavar="model")
parser.add_option("--outDir", dest="outDir", default = "/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond/BugFix",help="EOS output directory  (default = %default)", metavar="outDir")
parser.add_option('--lpc', action='store_true', dest='lpc', default=True, help='running on lpc condor  (default = %default)')

(options, args) = parser.parse_args()

# -----------------------------------------------------------------
#Create CACHEDIR.TAG files on the fly to exclude output directories from condor tarball
# -----------------------------------------------------------------
#AR-At call of this function, we are at /uscms_data/d3/arane/work/RA2bInterpretation/CMSSW_7_4_7/src/SCRA2BLE/DatacardBuilder 
# this function is called only at the beginning
def cachedir(DIR):
    print "len(cacheDIR) " ,len(DIR)
    if len(DIR)==0: #false
        return
        #tagfile is created under tmp directory
    tagfile = DIR+"/CACHEDIR.TAG"
    print "tagfile " , tagfile
    print "tagfile exists " , os.path.isfile(tagfile) #false
    if not os.path.isfile(tagfile): #true
        print "Now write tag file"
        tag = open(tagfile,'w')
        tag.write("Signature: 8a477f597d28d172789f06886806bc55\n")
        tag.write("# This file is a cache directory tag.\n")
        tag.write("# For information about cache directory tags, see:\n")
        tag.write("#       http://www.brynosaurus.com/cachedir/")
        tag.close()
        print "tag file is written inside tmp directory: we are still at SCRA2BLE/DatacardBuilder"

def condorize(command,tag,odir,CMSSWVER):

    print "--------------------"
    print "Launching phase space point:",tag

    #change to a tmp dir
    os.chdir("tmp");
    startdir = os.getcwd(); #not used anywhere
    f1n = "tmp_%s.sh" %(tag);
    f1=open(f1n, 'w')
    f1.write("#!/bin/sh \n");

    # setup environment
    if options.lpc:

        f1.write("export SUBMIT_DIR=`pwd -P` \n" );
        f1.write("cd ${_CONDOR_SCRATCH_DIR} \n" );
    	f1.write("source /cvmfs/cms.cern.ch/cmsset_default.sh \n");
        f1.write("export SCRAM_ARCH=slc6_amd64_gcc491 \n");
        f1.write("eval `scramv1 project CMSSW CMSSW_7_4_7` \n");
        f1.write("cd CMSSW_7_4_7/src/ \n");
        f1.write("eval `scramv1 runtime -sh` \n");
	f1.write("tar -xzf $SUBMIT_DIR/SCRA2BLE.tar.gz \n" );
        f1.write("tar -xzf $SUBMIT_DIR/HiggsAnalysis.tar.gz \n" );
        f1.write("cd $SUBMIT_DIR/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit \n" );
        f1.write("scram b clean \n");
        f1.write("scram b -j4 \n");
#        f1.write("cd bin \n" );
 #       f1.write("make all \n");
        f1.write("cd $SUBMIT_DIR/CMSSW_7_4_7/src/SCRA2BLE/DatacardBuilder/ \n");

#    	f1.write("set SCRAM_ARCH=slc6_amd64_gcc481\n")
 #   	f1.write("cd %s \n" %(CMSSWVER));
  #  	f1.write("cd src/SCRA2BLE/DatacardBuilder/ \n");
   # 	f1.write("eval `scramv1 runtime -sh`\n")
    	f1.write(command+" \n")
    	mu=0.0
    	f1.write("xrdcp -f results_%s_mu%1.1f.root root://cmseos.fnal.gov/%s/results_%s_mu%1.1f.root 2>&1 \n" % (tag,float(mu),odir,tag,float(mu)));
#    	f1.write("rm -r *.py input* *.root *.tar.gz \n")
        f1.write("rm -r *.py input* *.root \n")
    	f1.close();
    	f2n = "tmp_%s.condor" % (tag);
    	outtag = "out_%s_$(Cluster)" % (tag)
     
    	f2=open(f2n, 'w')
    	f2.write("universe = vanilla \n");
    	f2.write("Executable = %s \n" % (f1n) );
    	f2.write("Requirements = OpSys == \"LINUX\"&& (Arch != \"DUMMY\" ) \n");
    	f2.write("request_disk = 10000000 \n");
    	f2.write("request_memory = 5000 \n");
    	f2.write("Should_Transfer_Files = YES \n");
    	f2.write("WhenToTransferOutput  = ON_EXIT \n");
    	f2.write("Transfer_Input_Files =  %s, /uscms_data/d3/arane/work/RA2bInterpretation/CMSSW_7_4_7/src/HiggsAnalysis.tar.gz, /eos/uscms/store/user/arane/SCRA2BLE.tar.gz \n" % (f1n));
    	f2.write("Output = "+outtag+".stdout \n");
    	f2.write("Error = "+outtag+".stderr \n");
    	f2.write("Log = "+outtag+".log \n");
    	f2.write("Notification    = Error \n");
    	f2.write("x509userproxy = $ENV(X509_USER_PROXY) \n")
    	f2.write("Queue 1 \n");
    	f2.close();
	
    	os.system("condor_submit %s" % (f2n));
	
 	os.chdir("../.");
    else:    
	f1.write("#SBATCH -J CombineCLT_%s\n" %(tag))
    	f1.write("#SBATCH -p background-4g\n")
    	f1.write("#SBATCH --time=07:30:00\n")
    	f1.write("#SBATCH --mem-per-cpu=8000 \n")
    	f1.write("#SBATCH -o CombineCLT_%s.out \n" %(tag))
    	f1.write("#SBATCH -e CombineCLT_%s.err \n" %(tag))
    	f1.write("cd /fdata/hepx/store/user/rish/CombineCards/Moriond/%s \n" % (CMSSWVER));
    	f1.write("cd src/SCRA2BLE/DatacardBuilder/ \n");
    	f1.write("eval `scramv1 runtime -sh`\n")
    	f1.write("ls \n");
    	f1.write(command+" \n") 
    	f1.close();
    	os.system("sbatch %s " %f1n)
 



if __name__ == '__main__':
    outDir = options.outDir # /store/user/arane/Limits_T1tttt
    eosDir = "root://cmseos.fnal.gov/"+options.outDir
    print "eosdir ", eosDir
    # get some info from the OS
    CMSSWVER = os.getenv("CMSSW_VERSION")
    CMSSWBASE = os.getenv("CMSSW_BASE")
    # tar it up for usage

    print "options.keeptar " , options.keeptar
    print "CMSSWVER " , CMSSWVER
    print "CMSSWBASE " ,CMSSWBASE
    print " tar directory " , CMSSWBASE+"/.. "+CMSSWVER
#AR-creates tmp directory at /uscms_data/d3/arane/work/RA2bInterpretation/CMSSW_7_4_7/src/SCRA2BLE/DatacardBuilder/
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
        cachedir('tmp')
    if not options.keeptar:
        print "keeptar not doing anything here"           
#os.system("tar --exclude-caches-all --exclude inputHistograms/fastsimSignalT*  -zcf tmp/"+CMSSWVER+".tar.gz -C "+CMSSWBASE+"/.. "+CMSSWVER+"/src/HiggsAnalysis")
#       os.system("tar --exclude-caches-all --exclude inputHistograms/fastsimSignalT*  -zcf tmp/SCRA2BLE.tar.gz -C /uscms_data/d3/arane/work/RA2bInterpretation/CMSSW_7_4_7/src/SCRA2BLE")
#        os.system("tar --exclude-caches-all -czf HiggsAnalysis.tar.gz HiggsAnalysis/")   
    #f = TFile.Open("inputHistograms/fastsimSignalT1tttt/RA2bin_signal.root");
#AR-Returns next item of iterator
    filenames = next(os.walk("/eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV12/"))[2]
    #filenames = next(os.walk("./inputHistograms/fastsimSignal%s/" %options.model))[2]
    #print filenames
	
    models = []
    mGos=[]
    mLSPs=[]
    for f in filenames:
        print "f " , f
	parse=f.split("_")
        print "parse " ,parse
	#print parse
	if not "proc" in parse[1]:continue
	if options.model==parse[2]:
		models.append(parse[2])	
		mGos.append(int(parse[3]))
		mLSPs.append(int(parse[4]))
    # for signal in signals:
    for m in range(len(mGos)):
        #    for mLSP in mLSPs:
        command = "python analysisBuilderCondor.py ";
        command += "--signal %s " % models[m];
        command += "--mGo %i " % mGos[m];
        command += "--mLSP %i " % mLSPs[m];
        if options.fastsim: command += " --fastsim";
        command += " --realData";
        command += " --tag allBkgs";
        #command += " --eos %s" % (eosDir);

        tag = "%s_%i_%i" % (models[m],mGos[m],mLSPs[m]);
	#os.system(command)
	print command
        condorize( command, tag, outDir, CMSSWVER );
        time.sleep(0.05);


    # else:

    #     os.system('python analysisBuilderCondor.py -b --signal T1bbbb --mGo 1500 --mLSP 100 --realData --tag allBkgs');
    #     os.system('python analysisBuilderCondor.py -b --signal T1bbbb --mGo 1000 --mLSP 100 --realData --tag allBkgs');
    #     os.system('python analysisBuilderCondor.py -b --signal T1tttt --mGo 1500 --mLSP 800 --realData --tag allBkgs');
    #     os.system('python analysisBuilderCondor.py -b --signal T1tttt --mGo 1200 --mLSP 800 --realData --tag allBkgs');
    #     os.system('python analysisBuilderCondor.py -b --signal T1qqqq --mGo 1400 --mLSP 800 --realData --tag allBkgs');
    #     os.system('python analysisBuilderCondor.py -b --signal T1qqqq --mGo 1000 --mLSP 800 --realData --tag allBkgs');





