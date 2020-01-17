#! /usr/bin/env python


## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 
import sys
import array as array
import math
from optparse import OptionParser
from tqdm import tqdm

#Global Trigger Efficiency Vars
edgesEl = [45, 50, 55, 60, 70, 80, 90, 100, 120, 140, 160, 200, 250, 300, 400, 500, 600, 800, 1000]
NBinsEl = 18#len(edgesEl)
triggerEfficienciesEl = [0.026661361, 0.43208829, 0.77876109, 0.82022744, 0.83862364, 0.84485871, 0.85109389, 0.85565388, 0.86430746, 0.87895018, 0.87826085, 0.88820976, 0.89754951, 0.89563191, 0.90026498, 0.90593588, 0.90593588, 0.90593588, 0.90593588]
edgesMu = [45, 50, 55, 60, 70, 80, 90, 100, 120, 140, 160, 200, 250, 300, 400, 500, 600, 800, 1000]
NBinsMu = 18#len(edgesMu)
triggerEfficienciesMu = [0.21379612, 0.95265096, 0.97956568, 0.98561150, 0.98043269, 0.97914445, 0.97634792, 0.95485681, 0.95453513, 0.94702542, 0.94127947, 0.93261105, 0.91108406, 0.91419727, 0.88470322, 0.89171273, 0.89171273, 0.89171273, 0.89171273]
#Low edge: Eff, Uncert
electronTriggerEfficiencyDict = {}
for lowEdge in edgesEl:
    electronTriggerEfficiencyDict[lowEdge] = 0.
muonTriggerEfficiencyDict = {}
for lowEdge in edgesEl:
    electronTriggerEfficiencyDict[lowEdge] = 0.
print "Finished setting up global variables"

def getTriggerEfficiency(recoLeptonType, userLeptonType, leptonPt):
    # Note the i will be 1 greater than the lower edge index, ROOT bin numbering starts at 1
    if userLeptonType.lower()=="electron" and recoLeptonType[0]!=11:
        return 0.
    if userLeptonType.lower()=="muon" and recoLeptonType[0]!=13:
        return 0.
    if userLeptonType.lower()=="electron":
        i = 0
        for lowEdge in edgesEl:
            if leptonPt < lowEdge:
                break
            else:
                i+=1
        return triggerEfficienciesEl[min(i,NBinsEl-1)]
    elif userLeptonType.lower()=="muon":
        i = 0
        for lowEdge in edgesMu:
            if leptonPt < lowEdge:
                break
            else:
                i+=1
        return triggerEfficienciesMu[min(i,NBinsMu-1)]
    
    print "Fails bad"
    return 0.
        


def plot_mttbar(argv) : 
    parser = OptionParser()

    parser.add_option('--file_in', type='string', action='store',
                      dest='file_in',
                      help='Input file')

    parser.add_option('--file_out', type='string', action='store',
                      dest='file_out',
                      help='Output file')

    parser.add_option('--leptonType', type='string', action='store',
                      dest='lepton_type', default = "electron",
                                    help='Lepton Type')

    parser.add_option('--topTag', action='store_true',
                      dest='topTag',
                      help='Require top tag. Defaults to true')

    parser.add_option('--bTag', action='store_true',
                      dest='bTag',
                      help='Require b tag. Defaults to true')

    # Not necessary because LeptonType is a reco quantity
    #parser.add_option('--isData', action='store_true',
    #                  dest='isData',
    #                  default = False,
    #                  help='Is this Data?')
        
    (options, args) = parser.parse_args(argv)
    print "Top tag", options.topTag
    print "B tag", options.bTag
    argv = []

    print '===== Command line options ====='
    print options
    print '================================'

    import ROOT

    from leptonic_nu_z_component import solve_nu_tmass, solve_nu

    fout= ROOT.TFile(options.file_out, "RECREATE")

    h_mttbar = ROOT.TH1F("h_mttbar", ";m_{t#bar{t}} (GeV);Number", 50, 0, 5000)

    h_mttbar_lwu = ROOT.TH1F("h_mttbar_lwu", ";m_{t#bar{t}} (GeV);Number", 50, 0, 4000)
    h_mttbar_lwd = ROOT.TH1F("h_mttbar_lwd", ";m_{t#bar{t}} (GeV);Number", 50, 0, 4000)

    h_mttbar_jec_up = ROOT.TH1F("h_mttbar_jec_up", ";m_{t#bar{t}} (GeV);Number", 50, 0, 4000) 
    h_mttbar_jec_down = ROOT.TH1F("h_mttbar_jec_down", ";m_{t#bar{t}} (GeV);Number", 50, 0, 4000)
    h_mttbar_jer_up = ROOT.TH1F("h_mttbar_jer_up", ";m_{t#bar{t}} (GeV);Number", 50, 0, 4000) 
    h_mttbar_jer_down = ROOT.TH1F("h_mttbar_jer_down", ";m_{t#bar{t}} (GeV);Number", 50, 0, 4000)

    h_mtopHad = ROOT.TH1F("h_mtopHad", ";m_{jet} (GeV);Number", 50, 100, 350)
    h_mtopHadGroomed = ROOT.TH1F("h_mtopHadGroomed", ";Groomed m_{jet} (GeV);Number", 50, 100, 250)

    h_lepton_pt = ROOT.TH1F("h_lepton_pt", ";p_{t} (GeV);Number", 50, 45, 500)
    h_MET  = ROOT.TH1F("h_MET", ";E_T Missing (GeV);Number", 50, 0, 500)
    h_lepton_eta = ROOT.TH1F("h_lepton_eta", "eta;Number", 50, -3, 3) 
    h_LepTopCandP4_pt = ROOT.TH1F("h_LepTopCanP4_pt", ";p_T Leptonic Top (GeV);Number", 50, 0, 1500)
    h_LepTopCandP4_m = ROOT.TH1F("h_LepTopCanP4_m", ";m_t (GeV);Number", 50, 0, 1500) 
    h_Compare = ROOT.TH2D("h_Compare", "FatJet p_T (GeV);Lepton DR Min", 50, 0, 2000, 50, 0, 6 ) # Figure out syntax later...

    h_FatJetPt = ROOT.TH1F("h_FatJetPt",";pt_{jet} (GeV) ; Number", 50, 400, 1000)
    h_FatJetEta = ROOT.TH1F("h_FatJetEta",";#Eta ; Number", 50, -3, 3)
    h_NearestAK4JetPt = ROOT.TH1F("h_NearestAK4JetPt",";pt_{jet} (GeV) ; Number", 50, 25 , 500)
    h_NearestAK4JetEta = ROOT.TH1F("h_NearestAK4JetEta","; #Eta ; Number", 50, -3, 3)
    h_NearestAK4JetBDisc = ROOT.TH1F("h_NearestAK4JetBDisc",";BDisc ; Number", 50, 0.1, 1)

    h_FatJetPt.Sumw2()
    h_FatJetEta.Sumw2()
    h_NearestAK4JetPt.Sumw2()
    h_NearestAK4JetEta.Sumw2()
    h_NearestAK4JetBDisc.Sumw2()

    
    h_mttbar.Sumw2()
    
    h_mttbar_lwu.Sumw2()
    h_mttbar_lwd.Sumw2()

    h_mttbar_jec_up.Sumw2()
    h_mttbar_jec_down.Sumw2()
    h_mttbar_jer_up.Sumw2()
    h_mttbar_jer_down.Sumw2()

    h_mtopHad.Sumw2()
    h_mtopHadGroomed.Sumw2()

    h_lepton_pt.Sumw2()
    h_MET.Sumw2()
    h_lepton_eta.Sumw2()
    h_LepTopCandP4_pt.Sumw2()
    h_LepTopCandP4_m.Sumw2()
    h_Compare.Sumw2()

    h_passElHT = ROOT.TH1F("h_passElHT",";pt_{el} (Gev) ; Number", NBinsEl, array.array('f',edgesEl))
    h_passHTelBin = ROOT.TH1F("h_passHTelBin",";pt_{el} (Gev) ; Number", NBinsEl, array.array('f',edgesEl))
    h_passHTmuBin = ROOT.TH1F("h_passHTmuBin",";pt_{el} (Gev) ; Number", NBinsMu, array.array('f',edgesMu))
    h_passMuHT = ROOT.TH1F("h_passMuHT",";pt_{mu} (Gev) ; Number", NBinsMu, array.array('f',edgesMu))
    h_passElHT.Sumw2()
    h_passMuHT.Sumw2()
    h_passHTmuBin.Sumw2()
    h_passHTelBin.Sumw2()
    
    h_effEl = ROOT.TH1F("h_effEl",";pt_{el} (Gev) ; Number", NBinsEl, array.array('f',edgesEl))
    h_effMu = ROOT.TH1F("h_effMu",";pt_{mu} (Gev) ; Number", NBinsMu, array.array('f',edgesMu))

    fin = ROOT.TFile.Open(options.file_in)


    trees = [ fin.Get("TreeSemiLept") ]

    isData = False
    if "SingleElectron" in options.file_in or "SingleMuon" in options.file_in:
        isData = True
        print "Is Data"
    
    for itree,t in enumerate(trees) :

        #if options.isData : 
        SemiLeptTrig        =  ROOT.vector('int')()
        LeptonIDWeight      =  array.array('f', [0.] )
        LeptonIDWeightUnc   =  array.array('f', [0.] )
        EleRecoWeight       =  array.array('f', [0.] )
        EleRecoWeightUnc    =  array.array('f', [0.] )
        SemiLeptWeight      = array.array('f', [0.] )
        PUWeight            = array.array('f', [0.] )
        GenWeight           = array.array('f', [0.] )
        FatJetPt            = array.array('f', [-1.])
        FatJetEta           = array.array('f', [-1.])
        FatJetPhi           = array.array('f', [-1.])
        FatJetRap           = array.array('f', [-1.])
        FatJetEnergy        = array.array('f', [-1.])
        FatJetBDisc         = array.array('f', [-1.])
        FatJetMass          = array.array('f', [-1.])
        FatJetMassSoftDrop  = array.array('f', [-1.])
        FatJetTau32         = array.array('f', [-1.])
        FatJetTau21         = array.array('f', [-1.]) 
        FatJetSDBDiscW      = array.array('f', [-1.])
        FatJetSDBDiscB      = array.array('f', [-1.])
        FatJetSDsubjetWpt   = array.array('f', [-1.])
        FatJetSDsubjetWmass = array.array('f', [-1.])
        FatJetSDsubjetBpt   = array.array('f', [-1.])
        FatJetSDsubjetBmass = array.array('f', [-1.])
        FatJetJECUpSys      = array.array('f', [-1.])
        FatJetJECDnSys      = array.array('f', [-1.])
        FatJetJERUpSys      = array.array('f', [-1.])
        FatJetJERDnSys      = array.array('f', [-1.])
        LeptonType          = array.array('i', [-1])
        LeptonPt            = array.array('f', [-1.])
        LeptonEta           = array.array('f', [-1.])
        LeptonPhi           = array.array('f', [-1.])
        LeptonEnergy        = array.array('f', [-1.])
        LeptonIso           = array.array('f', [-1.])
        LeptonPtRel         = array.array('f', [-1.])
        LeptonDRMin         = array.array('f', [-1.])
        SemiLepMETpt        = array.array('f', [-1.])
        SemiLepMETphi       = array.array('f', [-1.])
        SemiLepNvtx         = array.array('f', [-1.])
        FatJetDeltaPhiLep      = array.array('f', [-1.]) 
        NearestAK4JetBDisc            = array.array('f', [-1.])
        NearestAK4JetPt     = array.array('f', [-1.])
        NearestAK4JetEta    = array.array('f', [-1.])
        NearestAK4JetPhi    = array.array('f', [-1.])
        NearestAK4JetMass   = array.array('f', [-1.])
        NearestAK4JetJECUpSys = array.array('f', [-1.])
        NearestAK4JetJECDnSys = array.array('f', [-1.])
        NearestAK4JetJERUpSys = array.array('f', [-1.])
        NearestAK4JetJERDnSys = array.array('f', [-1.])
        SemiLeptRunNum        = array.array('f', [-1.])   
        SemiLeptLumiNum     = array.array('f', [-1.])   
        SemiLeptEventNum      = array.array('f', [-1.])   


        #if options.isData : 
        t.SetBranchAddress('SemiLeptTrig'        , SemiLeptTrig )
        t.SetBranchAddress('SemiLeptWeight'      , SemiLeptWeight      ) #Combined weight of all scale factors (lepton, PU, generator) relevant for the smeileptonic event selection
        t.SetBranchAddress('LeptonIDWeight', LeptonIDWeight)
        t.SetBranchAddress('LeptonIDWeightUnc', LeptonIDWeightUnc)
        t.SetBranchAddress('EleRecoWeight', EleRecoWeight)
        t.SetBranchAddress('EleRecoWeightUnc', EleRecoWeightUnc)
        t.SetBranchAddress('PUWeight'            , PUWeight            )
        t.SetBranchAddress('GenWeight'           , GenWeight               )
        t.SetBranchAddress('FatJetPt'            , FatJetPt            )
        t.SetBranchAddress('FatJetEta'           , FatJetEta           )
        t.SetBranchAddress('FatJetPhi'           , FatJetPhi           )
        t.SetBranchAddress('FatJetRap'           , FatJetRap           )
        t.SetBranchAddress('FatJetEnergy'        , FatJetEnergy        )
        t.SetBranchAddress('FatJetBDisc'         , FatJetBDisc         )
        t.SetBranchAddress('FatJetMass'          , FatJetMass           )
        t.SetBranchAddress('FatJetMassSoftDrop'  , FatJetMassSoftDrop  )
        t.SetBranchAddress('FatJetTau32'         , FatJetTau32         )
        t.SetBranchAddress('FatJetTau21'         , FatJetTau21         )
        t.SetBranchAddress('FatJetSDBDiscW'      , FatJetSDBDiscW      )
        t.SetBranchAddress('FatJetSDBDiscB'      , FatJetSDBDiscB              )
        t.SetBranchAddress('FatJetSDsubjetWpt'   , FatJetSDsubjetWpt   )
        t.SetBranchAddress('FatJetSDsubjetWmass' , FatJetSDsubjetWmass )
        t.SetBranchAddress('FatJetSDsubjetBpt'   , FatJetSDsubjetBpt   )
        t.SetBranchAddress('FatJetSDsubjetBmass' , FatJetSDsubjetBmass )
        t.SetBranchAddress('FatJetJECUpSys'      , FatJetJECUpSys      )
        t.SetBranchAddress('FatJetJECDnSys'      , FatJetJECDnSys      )
        t.SetBranchAddress('FatJetJERUpSys'      , FatJetJERUpSys      )
        t.SetBranchAddress('FatJetJERDnSys'      , FatJetJERDnSys      )
        t.SetBranchAddress('LeptonType'          , LeptonType          )
        t.SetBranchAddress('LeptonPt'            , LeptonPt            )
        t.SetBranchAddress('LeptonEta'           , LeptonEta           )
        t.SetBranchAddress('LeptonPhi'           , LeptonPhi           )
        t.SetBranchAddress('LeptonEnergy'        , LeptonEnergy        )
        t.SetBranchAddress('LeptonIso'           , LeptonIso           )
        t.SetBranchAddress('LeptonPtRel'         , LeptonPtRel         )
        t.SetBranchAddress('LeptonDRMin'         , LeptonDRMin         )
        t.SetBranchAddress('SemiLepMETpt'        , SemiLepMETpt        )
        t.SetBranchAddress('SemiLepMETphi'       , SemiLepMETphi       )
        t.SetBranchAddress('SemiLepNvtx'         , SemiLepNvtx         )
        t.SetBranchAddress('FatJetDeltaPhiLep'      , FatJetDeltaPhiLep      )
        t.SetBranchAddress('NearestAK4JetBDisc'            ,NearestAK4JetBDisc             )
        t.SetBranchAddress('NearestAK4JetPt'     ,NearestAK4JetPt      )
        t.SetBranchAddress('NearestAK4JetEta'    ,NearestAK4JetEta     )
        t.SetBranchAddress('NearestAK4JetPhi'    ,NearestAK4JetPhi     )
        t.SetBranchAddress('NearestAK4JetMass'   ,NearestAK4JetMass    )
        t.SetBranchAddress('NearestAK4JetJECUpSys'      , NearestAK4JetJECUpSys)
        t.SetBranchAddress('NearestAK4JetJECDnSys'      , NearestAK4JetJECDnSys)
        t.SetBranchAddress('NearestAK4JetJERUpSys'      , NearestAK4JetJERUpSys)
        t.SetBranchAddress('NearestAK4JetJERDnSys'      , NearestAK4JetJERDnSys)
        t.SetBranchAddress('SemiLeptRunNum'         ,  SemiLeptRunNum       )
        t.SetBranchAddress('SemiLeptLumiNum'      ,  SemiLeptLumiNum    )
        t.SetBranchAddress('SemiLeptEventNum'       ,  SemiLeptEventNum     )


        t.SetBranchStatus ('*', 0)
        t.SetBranchStatus ('FatJetSDBDiscB', 1)
        t.SetBranchStatus ('LeptonIDWeight', 1)
        t.SetBranchStatus ('LeptonIDWeightUnc', 1)
        t.SetBranchStatus ('EleRecoWeight', 1)
        t.SetBranchStatus ('EleRecoWeightUnc', 1)
        t.SetBranchStatus ('FatJetSDBDiscW', 1)
        t.SetBranchStatus ('SemiLeptWeight', 1)
        t.SetBranchStatus ('PUWeight', 1)
        t.SetBranchStatus ('GenWeight', 1)
        t.SetBranchStatus ('FatJetPt', 1)
        t.SetBranchStatus ('FatJetEta', 1)
        t.SetBranchStatus ('FatJetPhi', 1)
        t.SetBranchStatus ('FatJetMass', 1)
        t.SetBranchStatus ('FatJetMassSoftDrop', 1)
        t.SetBranchStatus ('FatJetTau32', 1)
        t.SetBranchStatus ('SemiLeptTrig', 1)
        t.SetBranchStatus ('NearestAK4JetBDisc', 1)
        t.SetBranchStatus ('NearestAK4JetPt'   ,1 )
        t.SetBranchStatus ('NearestAK4JetEta'  ,1 )
        t.SetBranchStatus ('NearestAK4JetPhi'  ,1 )
        t.SetBranchStatus ('NearestAK4JetMass' ,1 )
        t.SetBranchStatus ('SemiLepMETpt' , 1 )
        t.SetBranchStatus ('SemiLepMETphi' , 1 )
        t.SetBranchStatus ('LeptonType'          , 1 )
        t.SetBranchStatus ('LeptonPt'            , 1)
        t.SetBranchStatus ('LeptonEta'           , 1)
        t.SetBranchStatus ('LeptonPhi'           , 1)
        t.SetBranchStatus ('LeptonEnergy'        , 1)
        t.SetBranchStatus ('LeptonIso'           , 1)
        t.SetBranchStatus ('LeptonPtRel'         , 1)
        t.SetBranchStatus ('LeptonDRMin'         , 1)
        t.SetBranchStatus('FatJetJECUpSys'      , 1)
        t.SetBranchStatus('FatJetJECDnSys'      , 1)
        t.SetBranchStatus('FatJetJERUpSys'      , 1)
        t.SetBranchStatus('FatJetJERDnSys'      , 1)
        t.SetBranchStatus('NearestAK4JetJECUpSys'      , 1)
        t.SetBranchStatus('NearestAK4JetJECDnSys'      , 1)
        t.SetBranchStatus('NearestAK4JetJERUpSys'      , 1)
        t.SetBranchStatus('NearestAK4JetJERDnSys'      , 1)        


        entries = t.GetEntriesFast()
        print 'Processing tree ' + str(itree)
        #disc_l = [0.1522, 0.4941, 0.8001]

        eventsToRun = entries

        #eventsToRun = 100000
        count = 0
        for jentry in xrange( eventsToRun ):
            triggerEfficiency = 1.
            if jentry % 100000 == 0 :
                print 'processing ' + str(jentry)
                # get the next tree in the chain and verify
            ientry = t.GetEntry( jentry )
            if ientry < 0:
                break

            # Triggering: Data -- Fills histograms to calculate trigger efficiencies for electrons and muons against HT. MC -- just prints the efficiency for now.
            # Muon triggers only for now 
            # 0   "HLT_Mu50",
            # 1   "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165",
            # 2   "HLT_Ele115_CaloIdVT_GsfTrkIdT",
            # 3   "HLT_PFHT1050"    
            if isData:
                if not (SemiLeptTrig[0] or SemiLeptTrig[1] or SemiLeptTrig[2] or SemiLeptTrig[3]):
                    continue
                # Check if HTPass for both electron and muon channels
                if SemiLeptTrig[3]:
                    h_passHTelBin.Fill(LeptonPt[0])
                    h_passHTmuBin.Fill(LeptonPt[0])
                # Electrons
                if (options.lepton_type == "electron" and LeptonType[0] == 11):
                    if not (SemiLeptTrig[1] == 1 or SemiLeptTrig[2] == 1):
                        continue
                    elif (SemiLeptTrig[3]):
                        h_passElHT.Fill(LeptonPt[0])
                # Muons
                elif (options.lepton_type == "muon" and LeptonType[0] == 13):
                    if not SemiLeptTrig[0]:
                        continue
                    elif SemiLeptTrig[3]:
                        h_passMuHT.Fill(LeptonPt[0])
                else:
                    continue
            else:
                if (options.lepton_type == "electron" and LeptonType[0] == 11):
                    triggerEfficiency = getTriggerEfficiency(LeptonType, options.lepton_type, LeptonPt[0])
                elif (options.lepton_type == "muon" and LeptonType[0] == 13):
                    triggerEfficiency = getTriggerEfficiency(LeptonType, options.lepton_type, LeptonPt[0])
                else:
                    continue
                        
                        
            jec_up = FatJetJECUpSys[0]
            jec_down = FatJetJECDnSys[0]
            jer_up = FatJetJERUpSys[0]
            jer_down = FatJetJERDnSys[0]
        
            hadTopCandP4 = ROOT.TLorentzVector()
        
            hadTopCandP4.SetPtEtaPhiM( FatJetPt[0], FatJetEta[0], FatJetPhi[0], FatJetMass[0])
            bJetCandP4 = ROOT.TLorentzVector()
            bJetCandP4.SetPtEtaPhiM( NearestAK4JetPt[0], NearestAK4JetEta[0], NearestAK4JetPhi[0], NearestAK4JetMass[0])
            nuCandP4 = ROOT.TLorentzVector( )
            nuCandP4.SetPtEtaPhiM( SemiLepMETpt[0], 0, SemiLepMETphi[0], 0 )
            theLepton = ROOT.TLorentzVector()
            theLepton.SetPtEtaPhiE( LeptonPt[0], LeptonEta[0], LeptonPhi[0], LeptonEnergy[0] ) # Assume massless

            # ------------ Jet Energy Corrections+Resolution ----------------#
            hadTopCandP4_jec_up = hadTopCandP4*jec_up
            hadTopCandP4_jec_down = hadTopCandP4*jec_down
            hadTopCandP4_jer_up = hadTopCandP4*jer_up
            hadTopCandP4_jer_down = hadTopCandP4*jer_down

            bJetCandP4_jec_up = bJetCandP4*jec_up
            bJetCandP4_jec_down = bJetCandP4*jec_down
            bJetCandP4_jer_up = bJetCandP4*jer_up
            bJetCandP4_jer_down = bJetCandP4*jer_down
 
            theLeptonWeight = LeptonIDWeight[0]
            theLepton_WeightUp = theLeptonWeight + LeptonIDWeightUnc[0]
            theLepton_WeightDown = theLeptonWeight - LeptonIDWeightUnc[0]
            if LeptonType[0] != 13 : # If not a muon...
                theLeptonWeight = LeptonIDWeight[0]*EleRecoWeight[0]
                theLepton_WeightUp = theLeptonWeight + math.sqrt(LeptonIDWeightUnc[0]**2+EleRecoWeightUnc[0]**2)
                theLepton_WeightDown = theLeptonWeight - math.sqrt(LeptonIDWeightUnc[0]**2+EleRecoWeightUnc[0]**2)
            # -------------------------------------------------------------- #


            tau32 = FatJetTau32[0]
            mass_sd = FatJetMassSoftDrop[0]
            bdisc = NearestAK4JetBDisc[0]
            
            bsjet_disc = FatJetSDBDiscB[0]
            wsjet_disc = FatJetSDBDiscW[0]

            
            # CUTS
            passLepPt = LeptonPt[0] > 55
            passLepEta = (LeptonType[0]==11 and abs(LeptonEta[0]) < 2.5) or (LeptonType[0]==13 and abs(LeptonEta[0] < 2.4))
            passMET = SemiLepMETpt > 50
            passKin = hadTopCandP4.Perp() > 400.
            passTopTag = passKin and tau32 < 0.7 and mass_sd > 110. and mass_sd < 230 and ( wsjet_disc > .1522 or bsjet_disc > .1522) 
            passBtag = bdisc > .1522

            if not passLepPt or not passLepEta or not passMET:
                continue
            if options.bTag and not passBtag:
                continue
            if not options.bTag and passBtag:
                continue
            if options.topTag and not passTopTag:
                continue
            if not options.topTag and passTopTag:
                continue
            
                            
            count+=1
    

                ##  ____  __.__                              __  .__         __________                     
                ## |    |/ _|__| ____   ____   _____ _____ _/  |_|__| ____   \______   \ ____   ____  ____  
                ## |      < |  |/    \_/ __ \ /     \\__  \\   __\  |/ ___\   |       _// __ \_/ ___\/  _ \ 
                ## |    |  \|  |   |  \  ___/|  Y Y  \/ __ \|  | |  \  \___   |    |   \  ___/\  \__(  <_> )
                ## |____|__ \__|___|  /\___  >__|_|  (____  /__| |__|\___  >  |____|_  /\___  >\___  >____/ 
                ##         \/       \/     \/      \/     \/             \/          \/     \/     \/       
                
                # Now we do our kinematic calculation based on the categories of the
                # number of top and bottom tags
            mttbar = -1.0 

            lepTopCandP4 = None
                # Get the z-component of the lepton from the W mass constraint
            solution, nuz1, nuz2 = solve_nu( vlep=theLepton, vnu=nuCandP4 )
                # If there is at least one real solution, pick it up
            if solution :
                nuCandP4.SetPz( nuz1 )
            else :
                nuCandP4.SetPz( nuz1.real )

            lepTopCandP4 = nuCandP4 + theLepton + bJetCandP4
            ttbarCand = hadTopCandP4 + lepTopCandP4
            mttbar = ttbarCand.M()

            # ----------- Jet Energy Corrections+Resolution ------------ #
            lepTopCandP4_jec_up = nuCandP4 + theLepton + bJetCandP4_jec_up
            ttbarCand_jec_up = hadTopCandP4_jec_up + lepTopCandP4_jec_up

            lepTopCandP4_jec_down = nuCandP4 + theLepton + bJetCandP4_jec_down
            ttbarCand_jec_down = hadTopCandP4_jec_down + lepTopCandP4_jec_down

            lepTopCandP4_jer_up = nuCandP4 + theLepton + bJetCandP4_jer_up
            ttbarCand_jer_up = hadTopCandP4_jer_up + lepTopCandP4_jer_up

            lepTopCandP4_jer_down = nuCandP4 + theLepton + bJetCandP4_jer_down
            ttbarCand_jer_down = hadTopCandP4_jer_down + lepTopCandP4_jer_down

            mttbar_jec_up = ttbarCand_jec_up.M()
            mttbar_jec_down = ttbarCand_jec_down.M()
            mttbar_jer_up = ttbarCand_jer_up.M()
            mttbar_jer_down = ttbarCand_jec_down.M()
            # ---------------------------------------------------------- #

            SemiLeptWeight[0] *= triggerEfficiency

            h_mttbar.Fill( mttbar, SemiLeptWeight[0] )

            h_mttbar_jec_up.Fill( mttbar_jec_up, SemiLeptWeight[0] )
            h_mttbar_jec_down.Fill( mttbar_jec_down, SemiLeptWeight[0] )
            h_mttbar_jer_up.Fill( mttbar_jer_up, SemiLeptWeight[0] )
            h_mttbar_jer_down.Fill( mttbar_jer_down, SemiLeptWeight[0] ) 

            h_mtopHadGroomed.Fill( mass_sd, SemiLeptWeight[0] ) 
            h_mtopHad.Fill( hadTopCandP4.M(), SemiLeptWeight[0] ) 
            
            h_lepton_pt.Fill( theLepton.Pt(), SemiLeptWeight[0] )
            h_lepton_eta.Fill( theLepton.Eta(), SemiLeptWeight[0] )
            h_MET.Fill( SemiLepMETpt[0], SemiLeptWeight[0] )
            h_LepTopCandP4_pt.Fill( lepTopCandP4.Pt(), SemiLeptWeight[0] )
            h_LepTopCandP4_m.Fill( lepTopCandP4.M(), SemiLeptWeight[0] )
            h_Compare.Fill( FatJetPt[0], LeptonDRMin[0], SemiLeptWeight[0] )

            h_FatJetPt.Fill( FatJetPt[0], SemiLeptWeight[0] )
            h_FatJetEta.Fill( FatJetEta[0], SemiLeptWeight[0] )
            h_NearestAK4JetPt.Fill( NearestAK4JetPt[0], SemiLeptWeight[0])
            h_NearestAK4JetEta.Fill( NearestAK4JetEta[0], SemiLeptWeight[0])
            h_NearestAK4JetBDisc.Fill( NearestAK4JetBDisc[0], SemiLeptWeight[0])

            # -------- Avoid Division By Zero ---------- #

            if theLeptonWeight != 0:
                LWU = theLepton_WeightUp/theLeptonWeight
                LWD = theLepton_WeightDown/theLeptonWeight
            else:
                continue
                
            h_mttbar_lwu.Fill( mttbar, SemiLeptWeight[0]*LWU ) 
            h_mttbar_lwd.Fill( mttbar, SemiLeptWeight[0]*LWD )
            
        print(count)

        # Original hists have fine binning, change the bins below
        # Eff = PassHt&&PassEL(Mu)/PassHt
        h_effEl.Divide(h_passElHT,h_passHTelBin,1,1,"B")
        h_effMu.Divide(h_passMuHT,h_passHTmuBin,1,1,"B")

        # Loop over histogram bins and finds appropriate efficiency to apply
        #applyTriggerEfficiency(h_mttbar, )

    fout.cd()
    fout.Write()
    fout.Close()
    
    

if __name__ == "__main__" :
    
    plot_mttbar(sys.argv) # what is this?


