import os,sys

samplelist = {

'WJetsToLNuPt100To250':'/WJetsToLNu_Pt-100To250_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'WJetsToLNuPt250To400':'/WJetsToLNu_Pt-250To400_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'WJetsToLNuPt400To600':'/WJetsToLNu_Pt-400To600_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'WJetsToLNuPt600ToInf':'/WJetsToLNu_Pt-600ToInf_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'WJetsToLNuPt50To100':'/WJetsToLNu_Pt-50To100_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
                                  
'STtWantitop':'/ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',
'STtWtop':'/ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'STtchannelantitop':'/ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'STtchanneltop':'/ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'STschanneltop':'/ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'STschannelantitop':'/ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
                                  
'QCDHT700to1000':'/QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM',
'QCDHT500to700':'/QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',
'QCDHT300to500':'/QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'QCDHT200to300':'/QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM',
'QCDHT2000toInf':'/QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',
'QCDHT1500to2000':'/QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',
'QCDHT1000to1500':'/QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',
                                  
'TTToHadronic':'/TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'TTToSemiLeptonic':'/TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v2/MINIAODSIM',
'TTTo2L2Nu':'/TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_new_pmx_94X_mc2017_realistic_v14-v2/MINIAODSIM',
'TTMtt700to1000':'/TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'TTMtt1000toInf':'/TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
                                  
'RSGluonToTTM500':'/RSGluonToTT_M-500_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'RSGluonToTTM750':'/RSGluonToTT_M-750_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'RSGluonToTTM1000':'/RSGluonToTT_M-1000_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'RSGluonToTTM1250':'/RSGluonToTT_M-1250_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'RSGluonToTTM1500':'/RSGluonToTT_M-1500_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'RSGluonToTTM2000':'/RSGluonToTT_M-2000_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'RSGluonToTTM2500':'/RSGluonToTT_M-2500_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'RSGluonToTTM3000':'/RSGluonToTT_M-3000_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'RSGluonToTTM3500':'/RSGluonToTT_M-3500_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'RSGluonToTTM4000':'/RSGluonToTT_M-4000_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'RSGluonToTTM4500':'/RSGluonToTT_M-4500_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',
'RSGluonToTTM5000':'/RSGluonToTT_M-5000_TuneCP5_13TeV-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM',

}

datalist2017 = {
    'ElecRun2017B':'/SingleElectron/Run2017B-31Mar2018-v1/MINIAOD',
    'ElecRun2017C':'/SingleElectron/Run2017C-31Mar2018-v1/MINIAOD',
    'ElecRun2017D':'/SingleElectron/Run2017D-31Mar2018-v1/MINIAOD',
    'ElecRun2017E':'/SingleElectron/Run2017E-31Mar2018-v1/MINIAOD',
    'ElecRun2017F':'/SingleElectron/Run2017F-31Mar2018-v1/MINIAOD',
    'MuonRun2017B':'/SingleMuon/Run2017B-31Mar2018-v1/MINIAOD',
    'MuonRun2017C':'/SingleMuon/Run2017C-31Mar2018-v1/MINIAOD',
    'MuonRun2017D':'/SingleMuon/Run2017D-31Mar2018-v1/MINIAOD',
    'MuonRun2017E':'/SingleMuon/Run2017E-31Mar2018-v1/MINIAOD',
    'MuonRun2017F':'/SingleMuon/Run2017F-31Mar2018-v1/MINIAOD',
    }

for sample in samplelist.keys():
    print 'listing files in',samplelist[sample]
    os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query=\"file dataset = '+samplelist[sample]+'\" >& inputfiles/'+sample+'.txt')
    
    #print 'creating crab file for',sample
    #os.system('cp crab_submit_mc.py crab_submit_mc_'+sample+'.py')
    #os.system('sed -i "s|DATASET|'+samplelist[sample]+'|" crab_submit_mc_'+sample+'.py')
    #os.system('sed -i "s|NAME|'+sample+'|" crab_submit_mc_'+sample+'.py')

i = 0
for sample in datalist2017.keys():
    print 'listing files in',datalist2017[sample]
    os.system('/cvmfs/cms.cern.ch/common/dasgoclient --limit=0 --query="file dataset = '+datalist2017[sample]+'" >& inputfiles/'+sample+'.txt')

    #print 'creating crab file for',sample
    #os.system('cp crab_submit_data.py crab_submit_data_'+sample+'.py')
    #os.system('sed -i "s|DATASET|'+datalist2017[sample]+'|" crab_submit_data_'+sample+'.py')
    #os.system('sed -i "s|NAME|'+sample+'|" crab_submit_data_'+sample+'.py')
    #i += 1
