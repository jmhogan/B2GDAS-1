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
#from samples import *

ROOT.gROOT.SetBatch()
DEBUG = False

def plotEffPlot(argv) : 
    parser = OptionParser()

    parser.add_option('--file_in', type='string', action='store',
                      dest='file_in',
                      help='Input file')

    parser.add_option('--OutDir', type='string', action='store',
                      dest='OutDir',
                      help='Output Directory')

    #parser.add_option('--Discrim', type='string', action='store',
    #                  dest='discrim', default = "mttbar",
    #                  help='Discriminator.')

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

    fin = ROOT.TFile.Open(options.file_in)
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
    CMS_lumi.cmsTextSize   = 0.55
    CMS_lumi.lumiTextSize     = 0.4
    FillColor = [ROOT.kRed, ROOT.kCyan, ROOT.kGreen+2, ROOT.kMagenta+1, ROOT.kOrange+7]

    canvas.cd()
    padup = ROOT.TPad("padup", "padup", 0.01,0.01,0.99,0.99);
    padup.SetBottomMargin(0.1)
    padup.SetTopMargin(0.1)
    padup.SetRightMargin(0.1)
    padup.SetLeftMargin(0.15)
    padup.SetFillStyle(0)
    #padup.SetGridx() 
    padup.SetBorderMode(0)
    padup.SetFrameFillStyle(0)
    padup.SetFrameBorderMode(0)
    padup.SetTickx(0)
    padup.SetTicky(0)
    padup.Draw()
    #padup.cd()
    
    #paddown = ROOT.TPad("paddown", "paddown", 0.01,0.01,0.99,0.32);
    #paddown.SetTopMargin(0.01)
    #paddown.SetBottomMargin(0.3)
    #paddown.SetRightMargin(0.1)
    ##paddown.SetGridx()
    #paddown.Draw()

    #Legend = ROOT.TLegend(0.6, 0.6, 0.8, 0.8)
    #Legend.SetBorderSize(0)
    #Legend.SetTextSize(0.04)
    #Legend.SetNColumns(1)
    #Legend.SetFillColor(ROOT.kWhite)
    KeyNames = []
    AllHists = []
    #StackedHist = ROOT.THStack("StackedHsit","");
    for key in ListOfKeys:
        if(DEBUG) : print key.GetName(),  key.GetClassName()
        if "TH1" not in key.GetClassName() and "TH2" not in key.GetClassName() and "TCanvas" not in key.GetClassName():
            continue
        KeyNames.append(key.GetName())
        if ("TCanvas" not in key.GetClassName()):
            hist = fin.Get(KeyNames[-1])
            hist.SetDirectory(0)
        else:
            canvas = fin.Get(KeyNames[-1])
            hist = canvas.Get("") 
        AllHists.append(hist)
        #AllHists[-1].Draw("e")
        #Legend.AddEntry(DataHist, "Data","pe")
        if 'ratio' in KeyNames[-1] : AllHists[-1].GetYaxis().SetTitle("Efficiency")
        if 'SF' in KeyNames[-1]: AllHists[-1].GetYaxis().SetTitle("Efficiency in Data / Efficiency in MC")
        AllHists[-1].GetYaxis().SetTitleSize(0.04)
        AllHists[-1].GetYaxis().SetTitleOffset(1.0)
        AllHists[-1].GetXaxis().SetTitleSize(0.04)
        #AllHists[-1].GetXaxis().SetLabelSize(0.03)
        #xTitle = AllHists[-1].GetXaxis().GetTitle()
        #ratioHist.SetTitle(";"+xTitle+";"+yTitle2);
        padup.cd()
        AllHists[-1].Draw("e")
        canvas.cd()
        CMS_lumi.CMS_lumi(padup, iPeriod, iPos)
        padup.cd()
	#Legend.Draw()
        padup.Update()
        padup.RedrawAxis()
        frame = padup.GetFrame()
        frame.Draw()
        canvas.cd()
        frame = canvas.GetFrame()
        frame.Draw()

        canvas.SaveAs(options.OutDir+"/"+KeyNames[-1]+".pdf")

if __name__ == "__main__" :
    plotEffPlot(sys.argv)


