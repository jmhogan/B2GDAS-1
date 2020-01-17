#! /usr/bin/env python
Lumi = 40000

bkgsamples = {
    "QCD": [   
        "QCD_1000to1500_plots.root",
        "QCD_1500to2000_plots.root",
        "QCD_2000toInf_plots.root",
        "QCD_200to300_plots.root",
        "QCD_300to500_plots.root",
        "QCD_500to700_plots.root",
        "QCD_700to1000_plots.root",
    ],
    "WJets": [
        "WJets_100to250_plots.root",
        "WJets_250to400_plots.root",
        "WJets_400to600_plots.root",
        "WJets_50to100_plots.root",
        "WJets_600toInf_plots.root",
    ],
    "ST" :[
        "ST_s_tbar_plots.root",
        "ST_s_top_plots.root",
        "ST_tW_tbar_plots.root",
        "ST_tW_top_plots.root",
        "ST_t_tbar_plots.root",
        "ST_t_top_plots.root",
    ],
    "TT" :[
        "TT_0lep_plots.root",
        "TT_1lep_plots.root",
        "TT_2lep_plots.root",
    ]
}

data = [
    "SingleElectron_ALL_plots.root",
    "SingleMuon_ALL_plots.root",
]

signal = [
    "RSG_1000_plots.root",
    #"RSG_2000_plots.root",
    #"RSG_2500_plots.root",
    #"RSG_3000_plots.root",
    #"RSG_3500_plots.root",
    #"RSG_4000_plots.root",
    #"RSG_4500_plots.root",
    #"RSG_500_plots.root",
    #"RSG_5000_plots.root",
]

weight = {}
weightFile = open('weights.txt','r')
lines = weightFile.readlines()
for l in lines:
    if '#' in l: continue
    line = (l.split('\n')[0]).split(',')
    sampleName = (line[0].split('.'))[0]
    NEff = float(line[1])
    Xsec = float(line[2])
    weight[sampleName] = Lumi*Xsec/NEff
