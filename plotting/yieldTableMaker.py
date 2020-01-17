#! /usr/bin/env python

import os
import argparse
#lumi = 40 ifb

def makeValidationYields(options, xSecDict):
    myOutputFile = open("validationYields.txt","w")
    myOutputFile.write("Sample && Weighted Yields && Raw Yields\n")
    myFilePaths = [options.directory+"/"+myFile for myFile in os.listdir(options.directory) if ".root" in myFile]
    for myFile in myFilePaths:
        print myFile.split(".root")[0]
        myTFile = ROOT.TFile.Open(myFile.replace("/eos/uscms/","root://cmseos.fnal.gov//"));
        myNEvtsHist = myTFile.Get("h_nEvts")
        sumWeights = myNEvtsHist.GetBinContent(3)-myNEvtsHist.GetBinContent(1)
        myTrashHist = ROOT.TH1F("myTrashHist","Leading Fat Jet Momentum;Jet p_{T}; Number of Weighted Events", 20, 0., 10000.)
        myTTree = myTFile.Get("TreeSemiLept")
        myTTree.Draw(options.branch+">>myTrashHist",options.cut)
        outputString = myFile.split("/")[-1].split(".root")[0]+" && "+str(myTrashHist.Integral())+" && "
        if not options.weight=="(1.)":
            myWeightedTrashHist = ROOT.TH1F("myWeightedTrashHist","Leading Fat Jet Momentum;Jet p_{T}; Number of Weighted Events", 20, 0., 10000.)
            myTTree.Draw(options.branch+">>myWeightedTrashHist","("+options.cut+"*"+str(xSecDict[myFile.split("//")[-1]])+"*"+options.weight+"/"+str(sumWeights)+")")
            outputString = outputString + str(myWeightedTrashHist.Integral())
        myOutputFile.write(outputString+"\n")
    myOutputFile.close()

def makeOutputYields(options, xSecDict):
    myOutputFile = open("outputYields.txt","w")
    myFilePaths = [options.directory+"/"+myFile for myFile in os.listdir(options.directory) if ".root" in myFile]
    for myFile in myFilePaths:
        print myFile.split(".root")[0]
        myTFile = ROOT.TFile.Open(myFile.replace("/eos/uscms/","root://cmseos.fnal.gov//"));
        myNEvtsHist = myTFile.Get("h_nEvts")
        sumWeights = myNEvtsHist.GetBinContent(3)-myNEvtsHist.GetBinContent(1)
        myTTree = myTFile.Get("TreeSemiLept")
        myHist = ROOT.TH1F("myHist","Leading Fat Jet Momentum;Jet p_{T}; Number of Weighted Events", 20, 0., 10000.)      
        myTTree.Draw(options.branch+">>myHist",options.cut)
        outputString = myFile.split("/")[-1]+" && "+str(myHist.Integral())+" && "
        if not options.weight=="(1.)":
            myWeightedHist = ROOT.TH1F("myWeightedHist","Leading Fat Jet Momentum;Jet p_{T}; Number of Weighted Events", 20, 0., 10000.)
            myTTree.Draw(options.branch+">>myWeightedHist","("+options.cut+"*"+str(xSecDict[myFile.split("//")[-1]])+"*"+options.weight+"/"+str(sumWeights)+")")
            #print "("+options.cut+"*"+options.weight+")"
            #print myWeightedHist.Integral()
            outputString = outputString + str(myWeightedHist.Integral())
        myOutputFile.write(outputString+"\n")
    myOutputFile.close()

def getXsecs():
    myDict = {}
    with open("../Samples_NEffective_CrossSections.txt") as f: 
        for line in f: 
            if ".root" in line:
                lineArray = line.split(",")
                myDict[lineArray[0]] = [lineArray[1],lineArray[2]] # sample.root: [xsec,nEff]
    return myDict

if __name__ == "__main__" :
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--all", help="Include all files", action="store_true")
    parser.add_argument("-d", "--directory", help="Directory pointing to original files",
default="/eos/uscms/store/user/cmsdas/2020/long_exercises/B2GTTbar/update2017data/")
    parser.add_argument("-v", "--validation", help="Directory pointing to original output files",
default="/eos/uscms/store/user/cmsdas/2020/long_exercises/B2GTTbar/update2017data/")
    parser.add_argument("-b", "--branch", help="Branch to draw", default="FatJetPt[0]")
    parser.add_argument("-c", "--cut", help="Cut string to be applied to events.", default="(1.)")
    parser.add_argument("-w", "--weight", help="Weight string to be applied to events",default="(40*GenWeight*PUWeight*EleRecoWeight*LeptonIDWeight*SemiLeptWeight)")
    options = parser.parse_args()
    import ROOT
    print "Getting xsecs"
    xSecDict = getXsecs()
    print "Making output yields"
    makeOutputYields(options, xSecDict)
    print "Making validation yields"
    makeValidationYields(options, xSecDict)
    
