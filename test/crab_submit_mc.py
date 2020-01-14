from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'B2GDAS_NAME'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'

config.Data.inputDataset = 'DATASET'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.publication = False
config.Data.outLFNDirBase = '/store/user/jmhogan/B2GTTbarUpdate2017/'

config.Site.storageSite = 'T3_US_FNALLPC'

config.JobType.scriptExe = 'execute_for_crab.sh'
config.JobType.outputFiles = ['output.root']
config.JobType.sendExternalFolder = True
config.JobType.inputFiles = ['FrameworkJobReport.xml', 'execute_for_crab.py', 'b2gdas_fwlite.py', 'JECs', 'purw2017.root', 'egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root', 'gammaEffi.txt_EGM2D_runBCDEF_passingMVA94Xwp80noiso.root', 'Muon_RunBCDEF_SF_ID.root']


