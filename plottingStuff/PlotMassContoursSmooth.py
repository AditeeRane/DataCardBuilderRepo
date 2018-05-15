from ROOT import *
#import numpy as np
import mmap
import time
import sys
import os

from optparse import OptionParser
parser = OptionParser()
parser.add_option("--model", dest="model", default = "T1bbbb",help="SMS model", metavar="model")
(options, args) = parser.parse_args()
#flist=open("listofFiles%s.txt" %sys.argv[1], 'r')
#fgluxsec=open("LatestXsecGluGlu.txt", 'r')
dictXsec={}
dictXsecUnc={}
with open('LatestXsecGluGlu.txt', 'r') as input:
        for line in input: #for ex. |225|2021.29|13.8804|
                elements = line.rstrip().split("|")
                dictXsec[int(elements[1])]=elements[2]
                dictXsecUnc[int(elements[1])]=elements[3]
                print elements
mGo=[]
mLsp=[]
MissMgo=[]
MissMLsp=[]
limit=[]

#fileOut=TFile("MassScan%s.root" %sys.argv[1], "RECREATE")
fileOut=TFile("MassScan%s.root" %options.model, "RECREATE")

names = next(os.walk("/eos/uscms/store/user/pedrok/SUSY2015/Analysis/Datacards/Run2ProductionV12/"))[2]

for n in names:
	print "nList ",n
	parse=n.split('_')
	if not "proc" in parse[1]:continue
	if options.model==parse[2]:
		print " Files with proc", parse
		mGo.append(float(parse[3]))
		mLsp.append(float(parse[4]))
		
		
'''		
for line in flilt:
        fname=line.split('_')
        mGo.append(float(fname[2]))
        end=fname[3].split('.')
        mLsp.append(float(end[0]))
'''
print len(mLsp)
SignifScan=TGraph2D()
SignifScan.SetName("SignifScan")

MuScan=TGraph2D()
MuScan.SetName("MuScan")
MuScanSup=TGraph2D()
MuScanSup.SetName("MuScanSup")
MuScanSdn=TGraph2D()
MuScanSdn.SetName("MuScanSdn")

MuScanObs=TGraph2D()
MuScanObs.SetName("MuScanObs")
MuScanObsSup=TGraph2D()
MuScanObsSup.SetName("MuScanObsSup")
MuScanObsSdn=TGraph2D()
MuScanObsSdn.SetName("MuScanObsSdn")

MuScanXsec=TGraph2D()
MuScanXsec.SetName("MuScanXsec")
MuScanExpXsec=TGraph2D()
MuScanExpXsec.SetName("MuScanExpXsec")

histoMuObs=TH2D("histoMuObs", "U.L. Obs on #mu ", 100, 0, 2500, 64,0,1600)
histoMuExp=TH2D("histoMuExp", "U.L. Obs on #mu ", 100, 0, 2500, 64,0,1600)
histoSignifScan=TH2D("histoSignifScan", "Signif. Scan (#sigma) ", 100, 0, 2500, 64,0,1600)
'''
MuScan=TGraph2D(len(mLsp))
MuScan.SetName("MuScan")
MuScanXsec=TGraph2D(len(mLsp))
MuScanXsec.SetName("MuScanXsec")
MuScanSup=TGraph2D(len(mLsp))
MuScanSup.SetName("MuScanSup")
MuScanSdn=TGraph2D(len(mLsp))
MuScanSdn.SetName("MuScanSdn")
MuScanObs=TGraph2D(len(mLsp))
MuScanObs.SetName("MuScanObs")
MuScanObsSup=TGraph2D(len(mLsp))
MuScanObsSup.SetName("MuScanObsSup")
MuScanObsSdn=TGraph2D(len(mLsp))
MuScanObsSdn.SetName("MuScanObsSdn")
'''
#idir = "/eos/uscms/store/user/rgp230/SUSY/statInterp/scanOutput/Moriond/BugFix/forrishilpcT1tttt/";
idir = "/eos/uscms/store/user/arane/Limits_T1tttt/";
for m in range(len(mGo)):
#	if(mGo[m]==1300 and mLsp[m]==200):
		#print "Check if this file is really empty before execution"
#		continue;
    	#if sys.argv[1]=="T1qqqq" and mGo[m]<400: continue
	filein=TFile(idir+"results_%s_%d_%d_mu0.0.root" %(options.model,int(mGo[m]), int(mLsp[m])))
	t = filein.Get("results")
	if not t:
		MissMgo.append(mGo[m])
		MissMLsp.append(mLsp[m]) 
		continue
	t.GetEntry(0)
	ExpUL= t.limit_exp #* float(dictXsec.get(mGo[m]))
	ExpULSigmaUp=t.limit_p1s #*float(dictXsec.get(mGo[m]))
    	ExpULSigmaDn=t.limit_m1s #*float(dictXsec.get(mGo[m]))


	ExpULXSec= t.limit_exp* float(dictXsec.get(mGo[m]))
	ObsULXSec= t.limit_obs * float(dictXsec.get(mGo[m]))

	ObsUL=t.limit_obs#*float(dictXsec.get(mGo[m]))
	shiftUp=1.0/(1-(float(dictXsecUnc.get(mGo[m]))/100.));
	shiftDn=1.0/(1+(float(dictXsecUnc.get(mGo[m]))/100.));
	ObsULDn=shiftDn*ObsUL
	ObsULUp=shiftUp*ObsUL

	histoMuObs.Fill(mGo[m], mLsp[m],t.limit_exp)
	histoMuExp.Fill(mGo[m], mLsp[m],t.limit_obs)

	if mGo[m]>500 and mGo[m]<555 and mLsp[m]>400:
		print mGo[m], mLsp[m], ObsUL, dictXsecUnc.get(mGo[m])

#	if ExpUL<0.000001:continue
	#GetN(): returns number of points in dataset
	SignifScan.SetPoint(SignifScan.GetN(),mGo[m], mLsp[m],t.significance)
	histoSignifScan.Fill(mGo[m], mLsp[m],t.significance)
	MuScan.SetPoint(MuScan.GetN(), mGo[m], mLsp[m], ExpUL)
	MuScanSup.SetPoint(MuScanSup.GetN(), mGo[m], mLsp[m], ExpULSigmaUp)
    	MuScanSdn.SetPoint(MuScanSdn.GetN(), mGo[m], mLsp[m], ExpULSigmaDn)
	MuScanObs.SetPoint( MuScanObs.GetN(), mGo[m], mLsp[m], ObsUL)
	MuScanObsSup.SetPoint( MuScanObsSup.GetN(), mGo[m], mLsp[m], ObsULUp)
    	MuScanObsSdn.SetPoint( MuScanObsSdn.GetN(), mGo[m], mLsp[m], ObsULDn)
	MuScanXsec.SetPoint(MuScanXsec.GetN(), mGo[m], mLsp[m],ObsULXSec)
	MuScanExpXsec.SetPoint(MuScanExpXsec.GetN(), mGo[m], mLsp[m], ExpULXSec)
	
	'''
	MuScan.SetPoint(m+1, mGo[m], mLsp[m], ExpUL)
	MuScanSup.SetPoint(m+1, mGo[m], mLsp[m], ExpULSigmaUp)
    	MuScanSdn.SetPoint(m+1, mGo[m], mLsp[m], ExpULSigmaDn)
	MuScanObs.SetPoint( m+1, mGo[m], mLsp[m], ObsUL)
	MuScanObsSup.SetPoint(m+1, mGo[m], mLsp[m], ObsULUp)
    	MuScanObsSdn.SetPoint(m+1, mGo[m], mLsp[m], ObsULDn)
	MuScanXsec.SetPoint(m+1, mGo[m], mLsp[m],ExpULXSec)
	'''
MuScan.SetName("MuScan")
MuScan.SetNpx(128)
MuScan.SetNpy(160)
MuScanSup.SetNpx(128)
MuScanSup.SetNpx(160)
MuScanSdn.SetNpx(128)
MuScanSdn.SetNpx(160)
MuScanObs.SetNpx(128)
MuScanObs.SetNpy(160)
MuScanObsSup.SetNpx(128)
MuScanObsSup.SetNpy(160)
MuScanObsSdn.SetNpx(128)
MuScanObsSdn.SetNpy(160)
MuScanXsec.SetNpx(128)
MuScanXsec.SetNpy(160)
MuScanExpXsec.SetNpx(128)
MuScanExpXsec.SetNpy(160)

#GetHistogram():By default returns a pointer to the Delaunay histogram. If fHistogram doesn't exist, books the 2D histogram fHistogram with a margin around the hull. Calls TGraphDelaunay::Interpolate at each bin centre to build up an interpolated 2D histogram. 
#Note that h* histograms are not used in the code as such anywhere.
hSignif=SignifScan.GetHistogram()
hExplim=MuScan.GetHistogram()
hExplimSup=MuScanSup.GetHistogram()
hExplimSdn=MuScanSdn.GetHistogram()
hObslim=MuScanObs.GetHistogram()
hObslimSup=MuScanObsSup.GetHistogram()
hObslimSdn=MuScanObsSdn.GetHistogram()
MassScan2D=MuScanXsec.GetHistogram()
MassScan2DExp=MuScanExpXsec.GetHistogram()
c=TCanvas("c","",800,800);
MuScan.Draw("colz")
MuScanSup.Draw("colz")
MuScanSdn.Draw("colz")
MuScanObs.Draw("colz")
MuScanObsSup.Draw("colz")
MuScanObsSdn.Draw("colz")
ExpLim=TGraph()
ExpLim.SetName("ExpLim")

#GetContourList: Returns the X and Y graphs building a contour at 1.
ExpLim= MuScan.GetContourList(1.0);
ExpLimSup= MuScanSup.GetContourList(1.0);
ExpLimSdn= MuScanSdn.GetContourList(1.0);
ObsLim= MuScanObs.GetContourList(1.0);
ObsLimSup= MuScanObsSup.GetContourList(1.0);
ObsLimSdn= MuScanObsSdn.GetContourList(1.0);

MuScan.Draw("colz")

fileOut.cd()
ExpLim.Write("ExpLim")
ExpLimSup.Write("ExpLimSup")
ExpLimSdn.Write("ExpLimSdn")
ObsLim.Write("ObsLim")
ObsLimSup.Write("ObsLimSup")
ObsLimSdn.Write("ObsLimSdn")
MassScan2D.Write("MassScan2D")
#histoMuExp.Write("histoMuExp");
#histoMuObs.Write("histoMuObs");
MassScan2DExp.Write("MassScan2DExp")
hSignif.Write("MassScanSignif")
histoSignifScan.Write("histoSignif")

#fileOut.Write()
#c.Print("test_MassContoursSmooth.pdf")
fileOut.Close()
#if hlim is None: print "NONE"
#time.sleep(60)
