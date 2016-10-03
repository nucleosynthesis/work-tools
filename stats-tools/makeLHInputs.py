#!/usr/bin/env python
import ROOT as r 
r.gROOT.SetBatch(True)
import os, sys
import optparse
import fnmatch
import pickle
from array import array

def parse_args():

    usage = ('usage: %prog getCorrelationMatrix.py [options]\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)

    parser.add_option('-i', '--inFile',      help='Input mlfit.root file')
    parser.add_option('-o', '--outFileName',default = "mlfit.root",      help='Output file')
    parser.add_option('-w', '--whichFits',default = "fit_b,prefit,fit_s",  help='Which fit(s) to use')
    parser.add_option('--filterStrings',default = "*",help='Take only bins with this in name (can give comma separated list)')
    parser.add_option('--threshold',default = 1.E-5, type=float,help='Only take bins with yield higher than threshold')

    options,args = parser.parse_args()
    return options 
def main(filterStrings,inFile,outFileName,whichFits,threshold):
    filters = ["*"+i.strip()+"*" for i in filterStrings.split(",")] if filterStrings else ["*"]
    whichFitList = [i.strip() for i in whichFits.split(",")] 
    outFile = r.TFile(outFileName,"RECREATE")
    outFile.cd()
    for whichFit in whichFitList:
        # get inputs
        iFile = r.TFile(inFile)
        covarianceInput = iFile.Get("shapes_{0}/overall_total_covar".format(whichFit))
        totalBackground = iFile.Get("shapes_{0}/total_background".format(whichFit))
        totalSignal = iFile.Get("shapes_{0}/total_signal".format(whichFit))
        total = iFile.Get("shapes_{0}/total_overall".format(whichFit))

        #make restricted set of bins based on filters + thresh
        binLabels = [covarianceInput.GetXaxis().GetBinLabel(iBin) for iBin in range(1,covarianceInput.GetNbinsX()+1)]
        binLabelsFiltered = []
        binDict = {}
        for iBinMinusOne,binLabel in enumerate(binLabels):
            #check filters
            if all([fnmatch.fnmatch(binLabel,filterString) for filterString in filters]):
                #check threshold
                if totalBackground.GetBinContent(iBinMinusOne+1) > threshold:
                    binLabelsFiltered.append(binLabel)
            binDict[binLabel] = iBinMinusOne+1
        
        #define outputs
        outBackground = r.TH1D("total_background","total_background",len(binLabelsFiltered),0,len(binLabelsFiltered))
        outSignal = r.TH1D("total_signal","total_signal",len(binLabelsFiltered),0,len(binLabelsFiltered))
        outTotal = r.TH1D("total","total",len(binLabelsFiltered),0,len(binLabelsFiltered))
        outCovar = r.TH2D("total_covar","total_covar",len(binLabelsFiltered),0,len(binLabelsFiltered),\
                len(binLabelsFiltered),0,len(binLabelsFiltered))

        #set output contents/errors + labels
        for iBinMinusOne,binLabel in enumerate(binLabelsFiltered):
            outTotal.SetBinError(iBinMinusOne+1,total.GetBinError(binDict[binLabel]))
            outTotal.SetBinContent(iBinMinusOne+1,total.GetBinContent(binDict[binLabel]))
            outBackground.SetBinContent(iBinMinusOne+1,totalBackground.GetBinContent(binDict[binLabel]))
            outBackground.SetBinError(iBinMinusOne+1,totalBackground.GetBinError(binDict[binLabel]))
            outSignal.SetBinError(iBinMinusOne+1,totalSignal.GetBinError(binDict[binLabel]))
            outSignal.SetBinContent(iBinMinusOne+1,totalSignal.GetBinContent(binDict[binLabel]))

            outBackground.GetXaxis().SetBinLabel(iBinMinusOne+1,binLabel)
            outSignal.GetXaxis().SetBinLabel(iBinMinusOne+1,binLabel)
            outTotal.GetXaxis().SetBinLabel(iBinMinusOne+1,binLabel)
            outCovar.GetXaxis().SetBinLabel(iBinMinusOne+1,binLabel)
            outCovar.GetYaxis().SetBinLabel(iBinMinusOne+1,binLabel)
            for jBinMinusOne,binLabel2 in enumerate(binLabelsFiltered):
                outCovar.SetBinContent(iBinMinusOne+1,jBinMinusOne+1,covarianceInput.GetBinContent(binDict[binLabel],binDict[binLabel2]))

        #write it!
        outDir = outFile.mkdir("shapes_{0}".format(whichFit))
        outDir.cd()
        outTotal.Write()
        outBackground.Write()
        outSignal.Write()
        outCovar.Write()
    outFile.Close()



if __name__ == "__main__":
    main(**vars(parse_args()))

