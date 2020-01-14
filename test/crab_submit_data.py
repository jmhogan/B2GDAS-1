from CRABClient.UserUtilities import config
config = config()

config.General.requestName = 'B2GDAS_NAME'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'

config.Data.inputDataset = 'DATASET'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 200
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/Final/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt'
config.Data.publication = False
config.Data.outLFNDirBase = '/store/user/jmhogan/B2GTTbarUpdate2017/'

config.Site.storageSite = 'T3_US_FNALLPC'

config.JobType.scriptExe = 'execute_for_crab_data.sh'

config.JobType.outputFiles = ['output.root']
config.JobType.inputFiles = ['FrameworkJobReport.xml', 'execute_for_crab_data.py', 'b2gdas_fwlite.py', 'JECs' ]
