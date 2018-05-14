import os

from ROOT import *
import numpy as np
import tdrstyle
tdrstyle.setTDRStyle()

from optparse import OptionParser
parser = OptionParser()

parser.add_option("--model", dest="model", default = "T1bbbb",help="SMS model", metavar="model")


(options, args) = parser.parse_args()


if __name__ == '__main__':
# flist=open("listofFiles.txt", 'r')
# mGo=[]
# mLsp=[]
# limit=[]
# for line in flist:
# 	fname=line.split('_')
# 	mGo.append(float(fname[2]))
# 	end=fname[3].split('.')
# 	mLsp.append(float(end[0]))

#ROOT.gStyle.SetPadLeftMargin(0.16);
#ROOT.gStyle.SetPadRightMargin(0.20);
#ROOT.gStyle.SetPadTopMargin(0.10);
#ROOT.gStyle.SetPalette(1);
#AR-180508:Files under inputHistograms/fastsimSignalT1bbbb/ and /eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV12/RA2bin_proc_T1bbbb_* have similar names.

#f = TFile("/eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV12/RA2bin_proc_T1bbbb_*");
#print "f.GetListOfKeys() ", f.GetListOfKeys()
#names = [k.GetName() for k in f.GetListOfKeys()]
	names = next(os.walk("/eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV12/"))[2]

#indx =ls /uscms_data/d3/arane/work/RA2bInterpretation/CMSSW_7_4_7/src/SCRA2BLE/DatacardBuilder/inputHistograms/fastsimSignalT1bbbb/RA2bin_proc_*
#for i in indx
 #    f = TFile("inputHistograms/fastsimSignalT1bbbb/%s" %i);

#names = [k.GetName() for k in f.GetListOfKeys()]

	mGo=[]
	mLsp=[]
	limit=[]
	for n in names:
		print "nList ",n
		parse=n.split('_')
		if not "proc" in parse[1]:continue
		if options.model==parse[2]:
			print " Files with proc", parse

	#tmpm = float(parse[2])---not used anywhere else in script
	#if tmpm == 1075 or tmpm == 1025 or tmpm == 625 or tmpm == 675 or tmpm == 725 or tmpm == 775 or tmpm == 825 or tmpm == 875 or tmpm == 925 or tmpm == 975 or tmpm == 1125 or tmpm == 1175: continue;
			mGo.append(float(parse[3]))
			mLsp.append(float(parse[4]))


#unique values
	mGoRange=mGo[:]
	mGoRangeSet=set(mGoRange)
	mGoRange=list(mGoRangeSet) #this only has the unique values
	print mGoRange
	mGoRange.sort()
	mGoRangeArray=np.asarray(mGoRange)
	print "mGoRangeArray ", len(mGoRangeArray)

	mLspRange=mLsp[:]
	mLspRangeSet=set(mLspRange)
	mLspRange=list(mLspRangeSet)
	print mLspRange
	mLspRange.sort()
	mLspRangeArray=np.asarray(mLspRange)
	print " mLspRangeArray ",len(mLspRangeArray)

	h2_MassScan=TH2F("h2_MassScan", "Mass Scan",    len(mGoRangeArray)-1, mGoRangeArray, len(mLspRangeArray)-1, mLspRangeArray)
	h2_MassScanMu=TH2F("h2_MassScanMu", "Mass Scan", len(mGoRangeArray)-1, mGoRangeArray, len(mLspRangeArray)-1, mLspRangeArray)
#print len(mGoRangeArray)-1, mGoRangeArray
#print len(mLspRangeArray)-1, mLspRangeArray

#	idir = "/eos/uscms/store/user/ntran/SUSY/statInterp/scanOutput/";
	idir = "/eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond/";
	for m in range(len(mGo)):
#AR: this is just to not include results_%s_%d_%d_mu0.0.root which for some reason seems to be empty. 
		if(mGo[m]==1300 and mLsp[m]==200):
			print "Check if this file is really empty before execution"
			continue;
		filein=TFile(idir+"results_%s_%d_%d_mu0.0.root" %(options.model, int(mGo[m]), int(mLsp[m])))
	#print "results_T1bbbb_%d_%d.root" %(int(mGo[m]), int(mLsp[m]))
		t = filein.Get("results")
		t.GetEntry(0)
		h2_MassScan.Fill(mGo[m],mLsp[m],t.limit_obs)
		h2_MassScanMu.Fill(mGo[m],mLsp[m],t.fittedMu)
		print "mG, mLSP, limit_obs",  mGo[m], mLsp[m],t.limit_obs

	c1=TCanvas("c1", "", 1000,1000)
	h2_MassScan.GetXaxis().SetTitle(" M_{g} ")
	h2_MassScan.GetYaxis().SetTitle(" m_{ #chi } ")
	h2_MassScan.SetMaximum(20);
	fout=TFile("test.root", 'recreate')
	h2_MassScan.Write()
	h2_MassScanMu.Write()
	h2_MassScan.Smooth();
	h2_MassScan.Draw("colz")
	c1.Print("testMassScan.pdf")
