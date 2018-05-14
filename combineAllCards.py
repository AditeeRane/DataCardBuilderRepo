from ROOT import *
import os
import math
import sys

from optparse import OptionParser
parser = OptionParser()
parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('--run', action='store_true', dest='run', default=False, help='no X11 windows')
parser.add_option("--dir", dest="dir", default = 'testCards-DrellYan2',help="mass of LSP", metavar="dir")

(options, args) = parser.parse_args()


#########################################################################################################
#########################################################################################################
if __name__ == '__main__':

	cdir = options.dir

	allcardnames = os.listdir(cdir);
	command = 'combineCards.py ';
	for cn in allcardnames:
		if 'card_' in cn: command += " " + cdir+'/'+cn;
	command += " > "+cdir+'/allcards.txt'
	os.system(command);

	if options.run:
		#combine_cmmd = "combine -M ProfileLikelihood --signif -t -1 --expectSignal=1 --toysFreq %s/allcards.txt" % (cdir);
		#combine_cmmd = "combine -M ProfileLikelihood --signif %s/allcards.txt" % (cdir);
		combine_cmmd = "text2workspace.py %s/allcards.txt -o %s/allcards.root" % (cdir,cdir);
		os.system(combine_cmmd);
		
		#combine_cmmd = "combine -M ProfileLikelihood --signif %s/allcards.root -n %s" % (cdir,cdir);
		#os.system(combine_cmmd);
		combine_cmmd = "combine -M MaxLikelihoodFit %s/allcards.root -n %s " % (cdir,cdir);
		os.system(combine_cmmd);
		#combine_cmmd = "combine -M Asymptotic %s/allcards.root -n %s" % (cdir,cdir);
		#os.system(combine_cmmd);
