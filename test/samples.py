#! /usr/bin/env python
Lumi = 1

bkgsamples = {
    "QCD": [   
        "mttbar_testQCD.root",
    ],
    "WJets": [
        "mttbar_testWJets.root",
    ]
}

data = [
    "mttbar_testEle2017B.root",
]

signal = [
    "mttbar_testRSG1000.root",
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
