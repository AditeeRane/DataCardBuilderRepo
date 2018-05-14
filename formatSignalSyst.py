from ROOT import *

def formatFile(dname,fname):
	print "%s/%s" %(dname,fname)	
	f = TFile.Open("%s/%s" %(dname,fname));
	fsbins=TFile.Open("%s/RA2bin_signal.root" %dname)
	fnameout=fname.rstrip(".root")+"Format.root"
	fout=TFile.Open("%s/%s" %(dname,fnameout), "RECREATE")
	names = [k.GetName() for k in f.GetListOfKeys()]
	for n in names:
		h=f.Get(n)
		h2=h.Clone(n)
		searchbins=fsbins.Get(n)
		fout.cd()
		hformat=formatHistogram(fname,h2,searchbins)
		#for i in range(1,hformat.GetNbinsX()+1):print hformat.GetXaxis().GetBinLabel(i)
		hformat.Write(n)
	f.Close();	
	fout.Close()
def formatHistogram(fname,hname, searchbins):
	parse=fname.split('_')[2].rstrip('.root')
	binlabel=parse
	if "Up" in parse: binlabel=parse.rstrip("Up");
	if "Down" in parse: binlabel=parse.rstrip("Down");
	for i in range(1,hname.GetNbinsX()+1):
		hname.GetXaxis().SetBinLabel(i,binlabel)
		fracUnc=1.0
		if ("Up" in fname or "up" in fname) and hname.GetBinContent(i)>0.0:fracUnc=searchbins.GetBinContent(i)/hname.GetBinContent(i)
		if ("Down" in fname or "down" in fname ) and searchbins.GetBinContent(i)>0.0:fracUnc=hname.GetBinContent(i)/searchbins.GetBinContent(i)
		if fracUnc>3.0:fracUnc=3.0
		if fracUnc<0.01:fracUnc=0.01
		hname.SetBinContent(i, fracUnc)
	return hname
def MCStatErr(dname):
	fsbins=TFile.Open("%s/RA2bin_signal.root" %dname)
	fout=TFile.Open("%s/RA2bin_signal_MCStatErr.root" %dname,"RECREATE")
	names = [k.GetName() for k in fsbins.GetListOfKeys()]
	for n in names:
		hsig=fsbins.Get(n)
		hmcstat=hsig.Clone(n)
		for i in range(1,hsig.GetNbinsX()+1):
			searchlabel=hsig.GetXaxis().GetBinLabel(i);
			hmcstat.GetXaxis().SetBinLabel(i,"MCStatErr_%s" %searchlabel)
			if(hsig.GetBinContent(i)>0.0):hmcstat.SetBinContent(i, 1.0+hsig.GetBinError(i)/hsig.GetBinContent(i))
			else:hmcstat.SetBinContent(i, 1.0+hsig.GetBinError(i))
		fout.cd()
		hmcstat.Write(n)
	fout.Close()
if __name__ == '__main__':
	DirectoryLists=["fastsimSignalT1tttt", "fastsimSignalT1bbbb","fastsimSignalT1qqqq", "fastsimSignalT5qqqqVV", "fastsimSignalT2tt","fastsimSignalT2bb", "fastsimSignalT2qq"]
	DirectoryLists=["fastsimSignalT1tttt"]
	listofFiles=["RA2bin_signal_btagCFuncUp.root", "RA2bin_signal_btagCFuncDown.root","RA2bin_signal_ctagCFuncUp.root","RA2bin_signal_ctagCFuncDown.root","RA2bin_signal_mistagCFuncUp.root","RA2bin_signal_mistagCFuncDown.root","RA2bin_signal_btagSFuncUp.root", "RA2bin_signal_btagSFuncDown.root", "RA2bin_signal_mistagSFuncUp.root", "RA2bin_signal_mistagSFuncDown.root", "RA2bin_signal_trigSystUncUp.root", "RA2bin_signal_trigSystUncDown.root","RA2bin_signal_trigStatUncUp.root","RA2bin_signal_trigStatUncDown.root","RA2bin_signal_JERup.root", "RA2bin_signal_JERdown.root", "RA2bin_signal_JECup.root", "RA2bin_signal_JECdown.root","RA2bin_signal_scaleuncUp.root","RA2bin_signal_scaleuncDown.root", "RA2bin_signal_isruncUp.root", "RA2bin_signal_isruncDown.root"]
	for dname in DirectoryLists:
		signaldirtag="inputHistograms/%s" %dname
		for fname in listofFiles:
			formatFile(signaldirtag,fname)
			#break;
		print signaldirtag
		MCStatErr(signaldirtag)
