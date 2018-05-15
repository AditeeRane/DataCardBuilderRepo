import sys
from inputFile import *
from smsPlotXSEC import *
from smsPlotCONT import *
from smsPlotBrazil import *

#AR-180510--Run this script as:
# python python/makeSMSplots.py config/SUS12024/T1tttt_SUS12024.cfg T1ttttRA2b
if __name__ == '__main__':
    # read input arguments
    filename = sys.argv[1] #config/SUS12024/T1tttt_SUS12024.cfg
    print "filename ", filename 
#The [-1] then indexes that list at position -1. Doing so will return the last item
    modelname = sys.argv[1].split("/")[-1].split("_")[0]
    print "modelname ", modelname #T1tttt
    analysisLabel = sys.argv[1].split("/")[-1].split("_")[1]
    print "analysisLabel ", analysisLabel #SUS12024.cfg
    outputname = sys.argv[2]
    print "outputname ",outputname #T1ttttRA2b
    # read the config file
    fileIN = inputFile(filename) #creates an object "fileIN" for this class
    
    # classic temperature histogra
#modelname:T1tttt
#fileIN.HISTOGRAM:2D histogram MassScan2D(t.limit_exp* float(dictXsec.get(mGo[m])))
#fileIN.OBSERVED:3 contours corresponding to observed limit(t.limit_obs), and it's 1sigma band
#fileIN.EXPECTED:3 contours corresponding to expected limit(t.limit_exp), and it's 1sigma band
#fileIN.ENERGY:13
#fileIN.LUMI:2.1
#fileIN.PRELIMINARY:Preliminary
    xsecPlot = smsPlotXSEC(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
    xsecPlot.Draw()
    xsecPlot.Save("%sXSEC" %outputname)
    '''
    # only lines
    contPlot = smsPlotCONT(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
    contPlot.Draw()
    contPlot.Save("%sCONT" %outputname)
    
    # brazilian flag (show only 1 sigma)
    brazilPlot = smsPlotBrazil(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, "")
    brazilPlot.Draw()
    brazilPlot.Save("%sBAND" %outputname)
    '''
    
