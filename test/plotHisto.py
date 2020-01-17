#! /usr/bin/env python

## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 
import sys, os
import array as array
from optparse import OptionParser
import ROOT
import CMS_lumi, tdrstyle
from samples import *

ROOT.gROOT.SetBatch()
DEBUG = False

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

    canvas.cd()
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
    padup.Draw()
    
    paddown = ROOT.TPad("paddown", "paddown", 0.01,0.01,0.99,0.32);
    paddown.SetTopMargin(0.01)
    paddown.SetBottomMargin(0.3)
    paddown.SetRightMargin(0.1)
    #paddown.SetGridx()
    paddown.Draw()

    Legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
    Legend.SetBorderSize(0)
    Legend.SetTextSize(0.04)
    Legend.SetNColumns(1)
    Legend.SetFillColor(ROOT.kWhite)
    KeyNames = []
    AllHists = []
    StackedHist = ROOT.THStack("StackedHsit","");
    for key in ListOfKeys:
        if(DEBUG) : print key.GetName(),  key.GetClassName()
        if "TH1" not in key.GetClassName() and "TH2" not in key.GetClassName():
            continue
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
                bkghist.Add(hist,weight[f.split("_plots")[0]])
            Hists.append(bkghist)
            if(DEBUG) : print Hists
            Hists[-1].SetFillColor(FillColor[j])
            Hists[-1].SetName(KeyNames[-1]+"_"+cat)
            Legend.AddEntry(Hists[-1], cat,"f") 
	    StackedBkgHist.Add(Hists[-1])
            AllBkgHist.Add(Hists[-1])
        BkgErr = ROOT.TGraphErrors()
        errRate = 0.1
        for i in range(1,AllBkgHist.GetNbinsX()+1):
            BkgErr.SetPoint(i-1, AllBkgHist.GetBinCenter(i), AllBkgHist.GetBinContent(i))
            BkgErr.SetPointError(i-1, (AllBkgHist.GetXaxis().GetBinCenter(i)-AllBkgHist.GetXaxis().GetBinLowEdge(i)), AllBkgHist.GetBinContent(i)*(errRate))
        BkgErr.SetFillStyle(3004)
        BkgErr.SetFillColor(12)
        BkgErr.SetLineColor(12)
        DataHist = ROOT.TH1D()
        for i,f in enumerate(data):
            ifile = ROOT.TFile.Open(inDir+"/"+f)
            hist = ifile.Get(KeyNames[-1])
            hist.SetDirectory(0)
            Hists.append(hist)
            DataHist.Add(Hists[-1])
        DataHist.SetName(KeyNames[-1]+"_data")
        Legend.AddEntry(DataHist, "Data","pe")

        SigHists = []
        for i,f in enumerate(signal):
            ifile = ROOT.TFile.Open(inDir+"/"+f)
            hist = ifile.Get(KeyNames[-1])
            hist.SetDirectory(0)
            hist.Scale(weight[f])
            SigHists.append(hist)
            SigHists[-1].SetLineColor(1)  
            SigHists[-1].SetLineWidth(3)
            SigHists[-1].SetLineStyle(i+1)          
            SigHists[-1].SetName(KeyNames[-1]+"_"+f.split('.')[0])
            Legend.AddEntry(SigHists[-1], f.split('_')[0]+" "+f.split('_')[1]+" GeV","l")
	AllHists.append(Hists)
        padup.cd()
        StackedBkgHist.SetMinimum(0.0)
        DataHist.SetMinimum(0.0)
        DataHist.SetMaximum(max(StackedBkgHist.GetMaximum(), DataHist.GetMaximum())*1.3)
        DataHist.GetYaxis().SetTitle("Events/bin")
        DataHist.GetYaxis().SetTitleSize(0.06)
        DataHist.GetYaxis().SetTitleOffset(0.98)
        DataHist.Draw("e")
        StackedBkgHist.Draw("histsame")
        BkgErr.Draw("same E2") 
        SigHists[0].Draw("histsame")
        DataHist.Draw("esame")
        paddown.cd()
        ratioHist = DataHist.Clone("ratioHist")
        ratioHist.SetMinimum(0.0)
        ratioHist.SetMaximum(1.6)
        ratioHist.GetXaxis().SetTitleSize(0.12)
        ratioHist.GetXaxis().SetLabelSize(0.11)
        ratioHist.GetYaxis().SetLabelSize(0.11)
        ratioHist.GetYaxis().SetTitleSize(0.12)
        ratioHist.GetYaxis().SetTitleOffset(0.35)
        #ratioHist.GetXaxis().SetTitleOffset(0.48)
        xTitle = SigHists[0].GetXaxis().GetTitle()
        if(DEBUG) : print xTitle
        if options.discrim.lower() in KeyNames[-1].lower():
            ratioHist.Add(AllBkgHist, -1)
            for i in range(1,ratioHist.GetNbinsX()+1):
                if not BkgErr.GetErrorY(i-1) == 0.0:
                    ratioHist.SetBinContent(i,ratioHist.GetBinContent(i)/BkgErr.GetErrorY(i-1))
            yTitle2 = "(Data-MC)/Unc." 
            ratioHist.SetFillColor(12)
            ratioHist.Draw("hist")
        else:
            ratioHist.Divide(AllBkgHist)
            yTitle2 = "Data/MC"
            ratioHist.Draw("e")
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


