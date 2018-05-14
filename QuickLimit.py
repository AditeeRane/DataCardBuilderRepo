from ROOT import *
models=['SMSbbbb1500','SMSbbbb1000', 'SMStttt1500','SMStttt1200','SMSqqqq1400','SMSqqqq1000']
for model in models:
	tf = TFile("higgsCombinetestCards-allBkgs-%s-1.3-mu0.0.Asymptotic.mH120.root" %model)
	tt = tf.Get("limit")
	tt.GetEntry(0)
	TwoSPlus=tt.limit
	tt.GetEntry(1);
	OneSPlus=tt.limit
	ExpLim=tt.GetEntry(2);
	ExpLim=tt.limit
	tt.GetEntry(3);
	OneSMinus=tt.limit
	tt.GetEntry(4)
	TwoSMinus=tt.limit	
	print model,TwoSPlus,OneSPlus,ExpLim,OneSMinus,TwoSMinus
