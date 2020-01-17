#! /usr/bin/env python

## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 
import sys, os
import array as array
import math
from optparse import OptionParser
import ROOT
import CMS_lumi, tdrstyle
from samples import *

ROOT.gROOT.SetBatch()
DEBUG = False
PrintYield = True

#JEC_unc = 0.05
#JER_unc = 0.05
#LepWeight = 0.0

def plotHisto(argv) : 
    parser = OptionParser()

    parser.add_option('--inDir', type='string', action='store',
                      dest='inDir',
                      help='Input file')

    parser.add_option('--OutDir', type='string', action='store',
                      dest='OutDir',
                      help='Output Directory')

    parser.add_option('--Discrim', type='string', action='store',
                      dest='discrim', default = "mttbar",
                      help='Discriminator.')

    (options, args) = parser.parse_args(argv)
    argv = []

    print '===== Command line options ====='
    print options
    print '================================'
    try:
        os.stat(options.OutDir)
    except:
        os.mkdir(options.OutDir)   

    if(DEBUG) : print bkgsamples
    inDir = options.inDir

    fin = ROOT.TFile.Open(inDir+"/"+bkgsamples[bkgsamples.keys()[0]][0])
    ListOfKeys = fin.GetListOfKeys()

    # set canvas style
    tdrstyle.setTDRStyle()
    canvas = ROOT.TCanvas("c","c",50,50,800,600)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetTickx(0)
    canvas.SetTicky(0)
    iPeriod = 4
    iPos = 11
    FillColor = [ROOT.kRed, ROOT.kCyan, ROOT.kGreen+2, ROOT.kMagenta+1, ROOT.kOrange+7]

#    canvas.cd()
    padup = ROOT.TPad("padup", "padup", 0.01,0.33,0.99,0.99);
    padup.SetBottomMargin(0.01)
    padup.SetTopMargin(0.1)
    padup.SetRightMargin(0.1)
    padup.SetFillStyle(0)
    #padup.SetGridx() 
    padup.SetBorderMode(0)
    padup.SetFrameFillStyle(0)
    padup.SetFrameBorderMode(0)
    padup.SetTickx(0)
    padup.SetTicky(0)
#    padup.Draw()
    
    paddown = ROOT.TPad("paddown", "paddown", 0.01,0.01,0.99,0.32);
    paddown.SetTopMargin(0.01)
    paddown.SetBottomMargin(0.3)
    paddown.SetRightMargin(0.1)
    #paddown.SetGridx()
    #paddown.Draw()


    Legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
    Legend.SetBorderSize(0)
    Legend.SetTextSize(0.04)
    Legend.SetNColumns(1)
    Legend.SetFillColor(ROOT.kWhite)

    KeyNames = []
    AllHists = []
    StackedHist = []
    for key in ListOfKeys:
        if(DEBUG) : print key.GetName(),  key.GetClassName()
        if "TH1" not in key.GetClassName(): # and "TH2" not in key.GetClassName():
            continue

        #canvas.Clear()
        canvas.cd()
        padup.Draw()
        paddown.Draw()
        Legend.Clear()

        KeyNames.append(key.GetName())
        Hists = []
        StackedBkgHist = ROOT.THStack(key.GetName()+"_MC",key.GetName()+"_MC") 
        AllBkgHist = ROOT.TH1D()
        for j,cat in enumerate(bkgsamples):
            bkghist = ROOT.TH1D()
            for i, f in enumerate(bkgsamples[cat]):
                ifile = ROOT.TFile.Open(inDir+"/"+f)
                hist = ifile.Get(KeyNames[-1])
                hist.SetDirectory(0)
                if(DEBUG) : print bkghist, hist, 'bkg ', f.split("_plots")[0], ' weight ', weight[f.split("_plots")[0]], ' nBins ', hist.GetNbinsX() 
                if i==0 : 
                    bkghist = hist.Clone(cat)
                    bkghist.Scale(weight[f.split("_plots")[0]])
                    if(DEBUG) : print bkghist
                else:
                    bkghist.Add(hist,weight[f.split("_plots")[0]])
                bkghist.SetDirectory(0)
                ifile.Close()
            Hists.append(bkghist)
            if(DEBUG) : print Hists, Hists[-1]
            Hists[-1].SetFillColor(FillColor[j])
            Hists[-1].SetName(KeyNames[-1]+"_"+cat)
            if(PrintYield): print cat, " Integral = ", Hists[-1].Integral(0,Hists[-1].GetNbinsX()+1)
            Legend.AddEntry(Hists[-1], cat,"f") 
	    StackedBkgHist.Add(Hists[-1])
            if(DEBUG) : print 'after stack'
            if j==0:
                AllBkgHist= Hists[-1].Clone("AllBkg")
            else:
                AllBkgHist.Add(Hists[-1])
        StackedHist.append(StackedBkgHist)
        BkgErr = ROOT.TGraphErrors()
        for i in range(1,AllBkgHist.GetNbinsX()+1):
            BkgErr.SetPoint(i-1, AllBkgHist.GetBinCenter(i), AllBkgHist.GetBinContent(i))
            BkgErr.SetPointError(i-1, (AllBkgHist.GetXaxis().GetBinCenter(i)-AllBkgHist.GetXaxis().GetBinLowEdge(i)), AllBkgHist.GetBinError(i)) #**2+JER_unc**2+JEC_unc**2+LepWeight**2))
        BkgErr.SetFillStyle(3004)
        BkgErr.SetFillColor(12)
        BkgErr.SetLineColor(12)

        DataHist = ROOT.TH1D()
        for i,f in enumerate(data):
            if not ('el' in inDir.lower() and 'el' in f.lower()) and not ('mu' in inDir.lower() and 'mu' in f.lower()): continue
            ifile = ROOT.TFile.Open(inDir+"/"+f)
            hist = ifile.Get(KeyNames[-1])
            hist.SetDirectory(0)
            Hists.append(hist)
            DataHist = hist.Clone("Data")
            DataHist.SetDirectory(0)
            ifile.Close()
        DataHist.SetName(KeyNames[-1]+"_data")
        if(PrintYield): print "data Integral = " , DataHist.Integral(0,DataHist.GetNbinsX()+1)
        Legend.AddEntry(DataHist, "Data","pe")

        SigHists = []
        for i,f in enumerate(signal):
            ifile = ROOT.TFile.Open(inDir+"/"+f)
            hist = ifile.Get(KeyNames[-1])
            hist.SetDirectory(0)
            hist.Scale(weight[f.split("_plots")[0]])
            SigHists.append(hist)
            SigHists[-1].SetLineColor(1)  
            SigHists[-1].SetLineWidth(3)
            SigHists[-1].SetLineStyle(i+1)          
            SigHists[-1].SetName(KeyNames[-1]+"_"+f.split('.')[0])
            Legend.AddEntry(SigHists[-1], f.split('_')[0]+" "+f.split('_')[1]+" GeV","l")
            ifile.Close()
	AllHists.append(Hists)
        #StackedBkgHist.SetMinimum(0.0)
        #DataHist.SetMinimum(0.0)
        #DataHist.SetMaximum((DataHist.GetMaximum())*2.0)
        DataHist.GetYaxis().SetRangeUser(0.0, (DataHist.GetMaximum())*1.7)
        DataHist.GetYaxis().SetTitle("Events/bin")
        DataHist.GetYaxis().SetTitleSize(0.06)
        DataHist.GetYaxis().SetLabelSize(0.05)
        DataHist.GetYaxis().SetTitleOffset(0.98)
        DataHist.SetMarkerStyle(8)

        padup.cd()
        DataHist.Draw("e")
        StackedBkgHist.Draw("hist same")
        BkgErr.Draw("same E2") 
        SigHists[0].Draw("histsame")
        DataHist.SetTitle("; ; Events/bin");
        DataHist.Draw("esame")

        paddown.cd()
        if(DEBUG) : print DataHist.GetNbinsX()
        ratioHist = DataHist.Clone("ratioHist")
        ratioHist.SetMinimum(0.0)
        ratioHist.SetMaximum(2.0)
        ratioHist.GetXaxis().SetTitleSize(0.12)
        ratioHist.GetXaxis().SetLabelSize(0.11)
        ratioHist.GetYaxis().SetLabelSize(0.11)
        ratioHist.GetYaxis().SetTitleSize(0.11)
        ratioHist.GetYaxis().SetTitleOffset(0.55)
        ratioHist.GetYaxis().SetNdivisions(30303)
        #ratioHist.GetXaxis().SetTitleOffset(0.48)
        xTitle = SigHists[0].GetXaxis().GetTitle()
        UnityLine = ROOT.TLine(ratioHist.GetXaxis().GetBinLowEdge(1), 1.0, ratioHist.GetXaxis().GetBinUpEdge(ratioHist.GetNbinsX()), 1.0)
        UnityLine.SetLineColor(1)
        if(DEBUG) : print xTitle
        if options.discrim.lower() in KeyNames[-1].lower():
            if(DEBUG) : print ratioHist, AllBkgHist
            ratioHist.Add(AllBkgHist, -1)
            for i in range(1,ratioHist.GetNbinsX()+1):
                if not BkgErr.GetErrorY(i-1) == 0.0:
                    ratioHist.SetBinContent(i,ratioHist.GetBinContent(i)/BkgErr.GetErrorY(i-1))
            yTitle2 = "(Data-MC)/Unc." 
            ratioHist.SetFillColor(12)
            ratioHist.SetMinimum(-5.0) #-1.1*max(ratioHist.GetMaximum(),abs(ratioHist.GetMinimum())))
            ratioHist.SetMaximum(5.0) #1.1*max(ratioHist.GetMaximum(),abs(ratioHist.GetMinimum())))
            ratioHist.Draw("hist")
        else:
            ratioHist.Divide(AllBkgHist)
            yTitle2 = "Data/MC"
            ratioHist.Draw("e")
            UnityLine.Draw("same")
        ratioHist.SetTitle(";"+xTitle+";"+yTitle2);
        CMS_lumi.CMS_lumi(padup, iPeriod, iPos)
        padup.cd()
	Legend.Draw()
        padup.Update()
        padup.RedrawAxis()
        frame = padup.GetFrame()
        frame.Draw()
        canvas.cd()
        frame = canvas.GetFrame()
        frame.Draw()

        canvas.SaveAs(options.OutDir+"/"+KeyNames[-1]+".pdf")

if __name__ == "__main__" :
    plotHisto(sys.argv)


