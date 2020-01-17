#! /usr/bin/env python


## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 
import sys
import array as array
from plot_mttbar import plot_mttbar
import os

tTag = False
bTag = True
lepton = 'electron'


path = 'root://cmseos.fnal.gov//store/user/cmsdas/2020/long_exercises/B2GTTbar/update2017data/'
ext = '.root'

if lepton == 'electron':lep = 'El'
else: lep = 'Mu'

dirName = 'plots_' + lep + '_T' + str(int(tTag)) + 'B' + str(int(bTag))

if not os.path.isdir(dirName):
    os.mkdir(dirName)

mc = ['RSG_1000','TT_0lep','TT_1lep','TT_2lep','ST_s_tbar','ST_s_tbar','ST_s_top','ST_tW_tbar','ST_tW_top','ST_t_tbar','ST_t_top','WJets_100to250','WJets_250to400','WJets_400to600','WJets_50to100','WJets_600toInf','QCD_1000to1500','QCD_1500to2000','QCD_2000toInf','QCD_200to300','QCD_300to500','QCD_500to700','QCD_700to1000']

mcStr = []
for name in mc:
    fileIn = path + name + ext
    fileOut = dirName + '/' + name + '_plots.root'
    inputTags = ["--file_in", fileIn, "--file_out", fileOut , "--leptonType", lepton]
    if tTag: inputTags.append('--topTag')
    if bTag: inputTags.append('--bTag')

    mcStr.append(inputTags)

for tag in mcStr:
    plot_mttbar( tag )



