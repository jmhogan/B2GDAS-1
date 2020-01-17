#! /usr/bin/env python


def makeJECJER(myPath,syst):
    tFile = ROOT.TFile.Open(myPath)
    myHistNom = tFile.Get("h_mttbar")
    if syst == "lw":
        myHistUp = tFile.Get("h_mttbar_lwu")
        myHistDown = tFile.Get("h_mttbar_lwd")
    else:
        myHistUp = tFile.Get("h_mttbar_"+syst.lower()+"_up")
        myHistDown = tFile.Get("h_mttbar_"+syst.lower()+"_down")
    myLegend = ROOT.TLegend(0.3,0.4,0.8,0.8)
    myLegend.SetNColumns(3)

    print "Nominal", myHistNom
    myHistNom.SetLineColor(ROOT.kBlack)
    myHistNom.SetLineWidth(2)
    myHistNom.DrawNormalized("histe")
    myHistNom.GetYaxis().SetTitle("Normalized Number of Events");
    myLegend.AddEntry(myHistNom,"Nominal","l")

    print "Up", myHistUp
    myHistUp.SetLineColor(ROOT.kBlue)
    myHistUp.SetLineWidth(2)
    myHistUp.DrawNormalized("histesame")
    myHistUp.GetYaxis().SetTitle("Normalized Number of Events");
    myLegend.AddEntry(myHistUp,syst+" Up","l")

    print "Down", myHistDown
    myHistDown.SetLineColor(ROOT.kRed)
    myHistDown.SetLineWidth(2)
    myHistDown.DrawNormalized("histesame")
    myHistDown.GetYaxis().SetTitle("Normalized Number of Events");
    myLegend.AddEntry(myHistDown,syst+" Down","l")

    myLegend.Draw("same")
    c1.SaveAs("mttbar_"+syst+".pdf")



if __name__ == "__main__" :

    import ROOT
    ROOT.gStyle.SetOptStat(0)
    c1 = ROOT.TCanvas()
    c1.cd()

    eosPath = "~/nobackup/samples/plots_El_T0B0/RSG_1000_plots.root"
    makeJECJER(eosPath, "JEC")
    makeJECJER(eosPath, "JER")
    makeJECJER(eosPath, "lw")
   
