#! /usr/bin/env python


if __name__ == "__main__" :

    import ROOT
    ROOT.gStyle.SetOptStat(0)
    c1 = ROOT.TCanvas()
    c1.cd()

    eosPath = "root://cmseos.fnal.gov//store/user/cmsdas/2020/long_exercises/B2GTTbar/update2017data/"
    signalSamples = ["RSG_500.root", "RSG_1000.root", "RSG_2000.root", "RSG_2500.root", "RSG_3000.root", "RSG_3500.root", "RSG_4000.root", "RSG_4500.root", "RSG_5000.root"]
    tFiles = [ROOT.TFile.Open(eosPath+mySignalFile) for mySignalFile in signalSamples]
    myHists = [myTF.Get("h_mttbar_true") for myTF in tFiles]
    myLegend = ROOT.TLegend(0.3,0.4,0.8,0.8)
    myLegend.SetNColumns(2)

    myHists[0].SetLineColor(ROOT.kBlack)
    myHists[0].SetLineWidth(2)
    myHists[0].DrawNormalized("hist")
    myHists[0].GetYaxis().SetTitle("Normalized Number of Events");
    myLegend.AddEntry(myHists[0],"RSG 500 GeV","l")

    otherColors = [ROOT.kBlack, ROOT.kRed, ROOT.kGreen-1, ROOT.kBlue-2, ROOT.kOrange, ROOT.kMagenta, ROOT.kCyan, ROOT.kMagenta+2, ROOT.kViolet+1]
    for i in range(1,len(myHists)):
        myHists[i].SetLineColor(otherColors[i])
        myHists[i].SetLineWidth(2)
        myHists[i].DrawNormalized("histsame")
        #myHists[i].GetYaxis().SetTitle("Normalized Number of Events");
        myLegend.AddEntry(myHists[i],"RSG "+signalSamples[i].split("_")[1].split(".")[0]+" GeV","l")

    myLegend.Draw("same")
    c1.SaveAs("testMasses.pdf")
        
    
