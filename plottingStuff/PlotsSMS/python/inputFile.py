import sys
import ROOT as rt
#AR-180509:Imported by makeSMSplots.py.
# It is returning 2D histogram for MassScan(t.limit_exp* float(dictXsec.get(mGo[m]))) and contours corresponding to expected and observed limit(t.limit_exp,t.limit_p1s,t.limit_p2s) and equivalent contours for observed limits)

class inputFile():
#__init__ is a special method in Python classes, it is the constructor method for a class. In the following example you can see how to use it. __init__ is called when ever an object of the class is constructed.The __init__ method is roughly what represents a constructor in Python.Python creates an object for you "self", and passes it as the first parameter to the __init__ method. 

#when run python python/makeSMSplots.py config/SUS12024/T1tttt_SUS12024.cfg T1ttttRA2b, input file name is config/SUS12024/T1tttt_SUS12024.cfg
    def __init__(self, fileName):
        self.HISTOGRAM = self.findHISTOGRAM(fileName)
        self.EXPECTED = self.findEXPECTED(fileName)
        self.OBSERVED = self.findOBSERVED(fileName)
        self.LUMI = self.findATTRIBUTE(fileName, "LUMI")
        self.ENERGY = self.findATTRIBUTE(fileName, "ENERGY")
        print self.ENERGY
        self.PRELIMINARY = self.findATTRIBUTE(fileName, "PRELIMINARY")

    def findATTRIBUTE(self, fileName, attribute): # reads value of attributes like lumi, cm energy from config/SUS12024/T1tttt_SUS12024.cfg
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != attribute: continue
            fileIN.close()
            return tmpLINE[1]

    def findHISTOGRAM(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:#runs for every line in the file
#[:-1]: It gets all the elements from the list (or characters from a string) but the last element.
            tmpLINE =  line[:-1].split(" ")
            print "tmpLINE ", tmpLINE
#            print "tmpLINE[0] ",tmpLINE[0]
            if tmpLINE[0] != "HISTOGRAM": continue # goes to next line if fist word in line is not "HISTOGRAM"
            fileIN.close()   #closes config/SUS12024/T1tttt_SUS12024.cfg once a line with HISTOGRAM is found.
            print "tmpLINE[1] ",tmpLINE[1]
            print "tmpLINE[2] ",tmpLINE[2] 

            rootFileIn = rt.TFile.Open(tmpLINE[1]) # opens config/SUS12024/MassScanT1tttt.root which is output of plottingStuff/PlotMassContoursSmooth.py. 
            x = rootFileIn.Get(tmpLINE[2]) # gets 2D histogram MassScan2D from above file, it has ExpULXSec= t.limit_exp* float(dictXsec.get(mGo[m])) saved in it
            x.SetDirectory(0) # if if I don't want a histogram to be added to any directory
            return {'histogram': x}
            
    def findEXPECTED(self, fileName): #returns 3 contours for expected limits
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "EXPECTED": continue
            # looks for line starting with EXPECTED in config/SUS12024/T1tttt_SUS12024.cfg and closes that file
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1]) #opens config/SUS12024/MassScanT1tttt.root
            return {'nominal': rootFileIn.Get(tmpLINE[2]), # gets 2D graph, ExpLim, which has t.limit_exp(contour)
                    'plus': rootFileIn.Get(tmpLINE[3]), # gets 2D graph, ExpLimSup, which has t.limit_p1s for every mass point(contour)
                    'minus': rootFileIn.Get(tmpLINE[4]), # gets 2D graph, ExpLimSdn, which has t.limit_m1s for every mass point(contour)
                    'colorLine': tmpLINE[5], #kRed
                    'colorArea': tmpLINE[6]} #kOrange

    def findOBSERVED(self, fileName): #returns 3 contours for observed limits 
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "OBSERVED": continue
            # looks for line starting with Observed in config/SUS12024/T1tttt_SUS12024.cfg and closes that file
            fileIN.close() 
            rootFileIn = rt.TFile.Open(tmpLINE[1]) #opens config/SUS12024/MassScanT1tttt.root
            return {'nominal': rootFileIn.Get(tmpLINE[2]), # gets 2D graph, ObsLim, which has t.limit_obs(contour)
                    'plus': rootFileIn.Get(tmpLINE[3]), #gets 2D graph, ObsLimSup, which has t.limit_obs*1.0/(1-(float(dictXsecUnc.get(mGo[m]))/100.))(contour)
                    'minus': rootFileIn.Get(tmpLINE[4]), #gets 2D graph, ObsLimSdn, which has t.limit_obs*1.0/(1+(float(dictXsecUnc.get(mGo[m]))/100.))(contour)
                    'colorLine': tmpLINE[5], #kBlack
                    'colorArea': tmpLINE[6]} #kGray

