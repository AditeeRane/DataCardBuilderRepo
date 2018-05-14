from ROOT import *
def LeptonCorr(signaldirtag,model,lumi, mGo, mLSP): #Here you can also add the genMHT hist
	signalContamLL_file=TFile("inputHistograms/SignalContamin/LLContamination_%s.root" %model)
	signalContamTau_file=TFile("inputHistograms/SignalContamin/Signal%sHtauContamin.root" %model)
	signalContamGenLL_file=TFile("inputHistograms/SignalContamin/LLContamination_genMHT_%s.root" %model)
	signalContamGenTau_file=TFile("inputHistograms/SignalContamin/Signal%sHtauContamin_genMHT.root" %model)
	
	LLHist=TH1D()
	LLGenHist=TH1D()
	TauHist=TH1D()
	TauGenHist=TH1D()
	if "T2" in model:
		LLGenHist=signalContamGenLL_file.Get("SignalContamination/mStop_%d_mLSP_%d" %(mGo, mLSP))
		TauGenHist=signalContamGenTau_file.Get("SignalContamination/mStop_%d_mLSP_%d" %(mGo, mLSP))
		LLHist=signalContamLL_file.Get("SignalContamination/mStop_%d_mLSP_%d" %(mGo, mLSP))
		TauHist=signalContamTau_file.Get("SignalContamination/mStop_%d_mLSP_%d" %(mGo, mLSP))
	else:
                LLGenHist=signalContamGenLL_file.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                TauGenHist=signalContamGenTau_file.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                LLHist=signalContamLL_file.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                TauHist=signalContamTau_file.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
	#if mixed models need to grab all the mixed models files and then add them weighted
	if "T1tbtb" in model or "T1tbtbT1tbttT1tttt" in model or "T1tbtbT1tbbbT1bbbb" in model or "T1ttbb" in model:
		signalContamLL_T1tbtb=TFile("inputHistograms/SignalContamin/LLContamination_T1tbtb.root")
		signalContamLL_T1tbbb=TFile("inputHistograms/SignalContamin/LLContamination_T1tbbb.root")
		signalContamLL_T1tbtt=TFile("inputHistograms/SignalContamin/LLContamination_T1tbtt.root")
		signalContamLL_T1bbtt=TFile("inputHistograms/SignalContamin/LLContamination_T1bbtt.root")
		signalContamLL_T1tttt=TFile("inputHistograms/SignalContamin/LLContamination_T1tttt.root")

		signalContamGenLL_T1tbtb=TFile("inputHistograms/SignalContamin/LLContamination_genMHT_T1tbtb.root")
		signalContamGenLL_T1tbbb=TFile("inputHistograms/SignalContamin/LLContamination_genMHT_T1tbbb.root")
		signalContamGenLL_T1tbtt=TFile("inputHistograms/SignalContamin/LLContamination_genMHT_T1tbtt.root")
		signalContamGenLL_T1bbtt=TFile("inputHistograms/SignalContamin/LLContamination_genMHT_T1bbtt.root")
		signalContamGenLL_T1tttt=TFile("inputHistograms/SignalContamin/LLContamination_genMHT_T1tttt.root")

		signalContamTau_T1tbtb=TFile("inputHistograms/SignalContamin/SignalT1tbtbHtauContamin.root")
		signalContamTau_T1tbbb=TFile("inputHistograms/SignalContamin/SignalT1tbbbHtauContamin.root")
		signalContamTau_T1tbtt=TFile("inputHistograms/SignalContamin/SignalT1tbttHtauContamin.root")
		signalContamTau_T1bbtt=TFile("inputHistograms/SignalContamin/SignalT1bbttHtauContamin.root")
		signalContamTau_T1tttt=TFile("inputHistograms/SignalContamin/SignalT1ttttHtauContamin.root")

		signalContamGenTau_T1tbtb=TFile("inputHistograms/SignalContamin/SignalT1tbtbHtauContamin_genMHT.root")
		signalContamGenTau_T1tbbb=TFile("inputHistograms/SignalContamin/SignalT1tbbbHtauContamin_genMHT.root")
		signalContamGenTau_T1tbtt=TFile("inputHistograms/SignalContamin/SignalT1tbttHtauContamin_genMHT.root")
		signalContamGenTau_T1bbtt=TFile("inputHistograms/SignalContamin/SignalT1bbttHtauContamin_genMHT.root")
		signalContamGenTau_T1tttt=TFile("inputHistograms/SignalContamin/SignalT1ttttHtauContamin_genMHT.root")
		
		if "T1tbtb" in model:
                	LLGenHist=signalContamGenLL_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauGenHist=signalContamGenTau_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	LLHist=signalContamLL_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauHist=signalContamTau_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))	
		if "T1tbtbT1tbttT1tttt" in model:
                	LLGenHistT1tbtb=signalContamGenLL_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauGenHistT1tbtb=signalContamGenTau_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	LLHistT1tbtb=signalContamLL_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauHistT1tbtb=signalContamTau_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))	
                	LLGenHistT1tbtt=signalContamGenLL_T1tbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauGenHistT1tbtt=signalContamGenTau_T1tbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	LLHistT1tbtt=signalContamLL_T1tbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauHistT1tbtt=signalContamTau_T1tbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))	
                	LLGenHistT1tttt=signalContamGenLL_T1tttt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauGenHistT1tttt=signalContamGenTau_T1tttt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	LLHistT1tttt=signalContamLL_T1tttt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauHistT1tttt=signalContamTau_T1tttt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))	
			w1=0.25
			w2=0.5
			w3=0.25
			LLGenHist=LLGenHistT1tbtb.Clone("LLGenHist")			
			LLHist=LLHistT1tbtb.Clone("LLHist")			
			TauGenHist=TauGenHistT1tbtb.Clone("TauGenHist")			
			TauHist=TauHistT1tbtb.Clone("TauHist")			
			for i in range(1, LLGenHist.GetNbinsX()+1):
				LLYield=w1*LLHistT1tbtb.GetBinContent(i)+w2*LLHistT1tbtt.GetBinContent(i)+w3*LLHistT1tttt.GetBinContent(i)
				LLGenYield=w1*LLGenHistT1tbtb.GetBinContent(i)+w2*LLGenHistT1tbtt.GetBinContent(i)+w3*LLGenHistT1tttt.GetBinContent(i)
				LLGenHist.SetBinContent(i,LLGenYield)
				LLHist.SetBinContent(i,LLYield)
				TauYield=w1*TauHistT1tbtb.GetBinContent(i)+w2*TauHistT1tbtt.GetBinContent(i)+w3*TauHistT1tttt.GetBinContent(i)
				TauGenYield=w1*TauGenHistT1tbtb.GetBinContent(i)+w2*TauGenHistT1tbtt.GetBinContent(i)+w3*TauGenHistT1tttt.GetBinContent(i)
				TauGenHist.SetBinContent(i,TauGenYield)
				TauHist.SetBinContent(i,TauYield)	
		if "T1tbtbT1tbbbT1bbbb" in model:
                	LLGenHistT1tbtb=signalContamGenLL_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauGenHistT1tbtb=signalContamGenTau_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	LLHistT1tbtb=signalContamLL_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauHistT1tbtb=signalContamTau_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))	
                	LLGenHistT1tbbb=signalContamGenLL_T1tbbb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauGenHistT1tbbb=signalContamGenTau_T1tbbb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	LLHistT1tbbb=signalContamLL_T1tbbb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauHistT1tbbb=signalContamTau_T1tbbb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))	
			w1=0.25
			w2=0.5
			w3=0.25 #(dont' need this no T1bbbb lepton contamin)
			LLGenHist=LLGenHistT1tbtb.Clone("LLGenHist")			
			LLHist=LLHistT1tbtb.Clone("LLHist")			
			TauGenHist=TauGenHistT1tbtb.Clone("TauGenHist")			
			TauHist=TauGenHistT1tbtb.Clone("TauHist")			
			for i in range(1, LLGenHist.GetNbinsX()+1):
				LLYield=w1*LLHistT1tbtb.GetBinContent(i)+w2*LLHistT1tbbb.GetBinContent(i)
				LLGenYield=w1*LLGenHistT1tbtb.GetBinContent(i)+w2*LLGenHistT1tbbb.GetBinContent(i)
				LLGenHist.SetBinContent(i,LLGenYield)
				LLHist.SetBinContent(i,LLYield)
				TauYield=w1*TauHistT1tbtb.GetBinContent(i)+w2*TauHistT1tbbb.GetBinContent(i)
				TauGenYield=w1*TauGenHistT1tbtb.GetBinContent(i)+w2*TauGenHistT1tbbb.GetBinContent(i)
				TauGenHist.SetBinContent(i,TauGenYield)
				TauHist.SetBinContent(i,TauYield)	
		if "T1ttbb" in model:
                	LLGenHistT1bbtt=signalContamGenLL_T1bbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauGenHistT1bbtt=signalContamGenTau_T1bbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	LLHistT1bbtt=signalContamLL_T1bbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauHistT1bbtt=signalContamTau_T1bbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))	
                	LLGenHistT1tbtb=signalContamGenLL_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauGenHistT1tbtb=signalContamGenTau_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	LLHistT1tbtb=signalContamLL_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauHistT1tbtb=signalContamTau_T1tbtb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))	
                	LLGenHistT1tbbb=signalContamGenLL_T1tbbb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauGenHistT1tbbb=signalContamGenTau_T1tbbb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	LLHistT1tbbb=signalContamLL_T1tbbb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauHistT1tbbb=signalContamTau_T1tbbb.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))	
                	LLGenHistT1tbtt=signalContamGenLL_T1tbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauGenHistT1tbtt=signalContamGenTau_T1tbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	LLHistT1tbtt=signalContamLL_T1tbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauHistT1tbtt=signalContamTau_T1tbtt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))	
                	LLGenHistT1tttt=signalContamGenLL_T1tttt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauGenHistT1tttt=signalContamGenTau_T1tttt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	LLHistT1tttt=signalContamLL_T1tttt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))
                	TauHistT1tttt=signalContamTau_T1tttt.Get("SignalContamination/mGluino_%d_mLSP_%d" %(mGo, mLSP))	
			w1=0.25
			w2=0.25
			w3=0.25
			w4=0.125
			w5=0.0625
			w6=0.0625 #(don't use this one no T1bbbb Lep contamination)
			LLGenHist=LLGenHistT1tbtb.Clone("LLGenHist")			
			LLHist=LLHistT1tbtb.Clone("LLHist")			
			TauGenHist=TauGenHistT1tbtb.Clone("TauGenHist")			
			TauHist=TauGenHistT1tbtb.Clone("TauHist")			
			for i in range(1, LLGenHist.GetNbinsX()+1):
				LLYield=w1*LLHistT1tbtb.GetBinContent(i)+w2*LLHistT1tbbb.GetBinContent(i)+w3*LLHistT1tbtt.GetBinContent(i)+w4*LLHistT1bbtt.GetBinContent(i)+w5*LLHistT1tttt.GetBinContent(i)
				LLGenYield=w1*LLGenHistT1tbtb.GetBinContent(i)+w2*LLGenHistT1tbbb.GetBinContent(i)+w3*LLGenHistT1tbtt.GetBinContent(i)+w4*LLGenHistT1bbtt.GetBinContent(i)+w5*LLGenHistT1tttt.GetBinContent(i)
				LLGenHist.SetBinContent(i,LLGenYield)
				LLHist.SetBinContent(i,LLYield)
				TauYield=w1*TauHistT1tbtb.GetBinContent(i)+w2*TauHistT1tbbb.GetBinContent(i)+w3*TauHistT1tbtt.GetBinContent(i)+w4*TauHistT1bbtt.GetBinContent(i)+w5*TauHistT1tttt.GetBinContent(i)
				TauGenYield=w1*TauGenHistT1tbtb.GetBinContent(i)+w2*TauGenHistT1tbbb.GetBinContent(i)+w3*TauGenHistT1tbtt.GetBinContent(i)+w4*TauGenHistT1bbtt.GetBinContent(i)+w5*TauGenHistT1tttt.GetBinContent(i)
				TauGenHist.SetBinContent(i,TauGenYield)
				TauHist.SetBinContent(i,TauYield)	
	LLGenHist.Scale(1000*lumi)
	TauGenHist.Scale(1000*lumi)
	LLHist.Scale(1000*lumi)
	TauHist.Scale(1000*lumi)
	sms=model+'_%d_%d_fast' %(mGo,mLSP)
	signal_file=TFile.Open(signaldirtag+"/RA2bin_proc_%s.root" %sms);
        #signal_file =TFile(signaldirtag+"/RA2bin_proc_%s.root" %sms);
	signaltag="RA2bin_"+sms;
	print signaltag
        signalRegion_sigHist = signal_file.Get(signaltag+"_nominalOrig");
        signalRegion_genHist = signal_file.Get(signaltag+"_genMHT");
	signalRegion_sigHist.Scale(1000*lumi)
	signalRegion_genHist.Scale(1000*lumi)
	signalHistContam=signalRegion_sigHist.Clone("signalHistContam")
	for i in range(1,signalHistContam.GetNbinsX()+1):
		YieldGen=signalRegion_genHist.GetBinContent(i)
		#if signalHistContam.GetBinContent(i)>0.0:
		print signalRegion_sigHist.GetBinContent(i),(TauHist.GetBinContent(i)+LLHist.GetBinContent(i))
		YieldGen=signalRegion_genHist.GetBinContent(i)-((TauGenHist.GetBinContent(i)+LLGenHist.GetBinContent(i))) #CORRECT THIS TO BE THE CONTAMINATION RUN OVER GEN
		Yield=signalHistContam.GetBinContent(i)-TauHist.GetBinContent(i)-LLHist.GetBinContent(i)
		Yield=(YieldGen+Yield)/2.0
		if Yield<0: Yield=0;
		signalHistContam.SetBinContent(i, Yield);
	signalHistContam.SetDirectory(0)
	return signalHistContam
	
