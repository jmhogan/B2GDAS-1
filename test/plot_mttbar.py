#! /usr/bin/env python


## _________                _____.__                            __  .__               
## \_   ___ \  ____   _____/ ____\__| ____  __ ______________ _/  |_|__| ____   ____  
## /    \  \/ /  _ \ /    \   __\|  |/ ___\|  |  \_  __ \__  \\   __\  |/  _ \ /    \ 
## \     \___(  <_> )   |  \  |  |  / /_/  >  |  /|  | \// __ \|  | |  (  <_> )   |  \
##  \______  /\____/|___|  /__|  |__\___  /|____/ |__|  (____  /__| |__|\____/|___|  /
##         \/            \/        /_____/                   \/                    \/ 
import sys
import array as array
from optparse import OptionParser
from tqdm import tqdm

def plot_mttbar(argv) : 
    parser = OptionParser()

    parser.add_option('--file_in', type='string', action='store',
                      dest='file_in',
                      help='Input file')

    parser.add_option('--file_out', type='string', action='store',
                      dest='file_out',
                      help='Output file')

    # Not necessary because LeptonType is a reco quantity
    #parser.add_option('--isData', action='store_true',
    #                  dest='isData',
    #                  default = False,
    #                  help='Is this Data?')
        
    (options, args) = parser.parse_args(argv)
    argv = []

    print '===== Command line options ====='
    print options
    print '================================'

    import ROOT

    from leptonic_nu_z_component import solve_nu_tmass, solve_nu

    fout= ROOT.TFile(options.file_out, "RECREATE")
    h_mttbar = ROOT.TH1F("h_mttbar", ";m_{t#bar{t}} (GeV);Number", 100, 0, 5000)
    h_mtopHad = ROOT.TH1F("h_mtopHad", ";m_{jet} (GeV);Number", 100, 0, 400)
    h_mtopHadGroomed = ROOT.TH1F("h_mtopHadGroomed", ";Groomed m_{jet} (GeV);Number", 100, 0, 400)
    h_mttbar.Sumw2()
    h_mtopHad.Sumw2()
    h_mtopHadGroomed.Sumw2()

    h_passElHT = ROOT.TH1F("h_passElHT",";pt_{el} (Gev) ; Number", 50, 20, 1020)
    h_passHT = ROOT.TH1F("h_passHT",";pt_{el} (Gev) ; Number", 50, 20, 1020)
    h_passMuHT = ROOT.TH1F("h_passMuHT",";pt_{mu} (Gev) ; Number", 50, 20, 1020)
    h_passElHT.Sumw2()
    h_passMuHT.Sumw2()
    h_passHT.Sumw2()

    fin = ROOT.TFile.Open(options.file_in)


    trees = [ fin.Get("TreeSemiLept") ]

    isData = False
    if "SingleElectron" in options.file_in or "SingleMuon" in options.file_in:
        isData = True
    
    for itree,t in enumerate(trees) :

        #if options.isData : 
        SemiLeptTrig        =  ROOT.vector('int')()
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


        entries = t.GetEntriesFast()
        print 'Processing tree ' + str(itree)
        #disc_l = [0.1522, 0.4941, 0.8001]

        eventsToRun = entries

        #eventsToRun = 100000
        count = 0
        for jentry in xrange( eventsToRun ):
            if jentry % 100000 == 0 :
                print 'processing ' + str(jentry)
                # get the next tree in the chain and verify
            ientry = t.GetEntry( jentry )
            if ientry < 0:
                break
    
                # Muons only for now
            if LeptonType[0] != 13 :
                continue
    
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
                        h_passHt.Fill(LeptonPt[0])
                    # Electrons
                    if LeptonType[0] == 11:
                        if not (SemiLeptTrig[1] == 1 or SemiLeptTrig[2] == 1):
                            continue
                        else if (SemiLeptTrig[3]):
                            h_passElHT.Fill(LeptonPt)
                    # Muons
                    if LeptonType[0] == 13:
                        if not SemiLeptTrig[0]:
                            continue
                        else if SemiLeptTrig[3]:
                            h_passMuHT.Fill(LeptonPt)
                    
            hadTopCandP4 = ROOT.TLorentzVector()
            hadTopCandP4.SetPtEtaPhiM( FatJetPt[0], FatJetEta[0], FatJetPhi[0], FatJetMass[0])
            bJetCandP4 = ROOT.TLorentzVector()
            bJetCandP4.SetPtEtaPhiM( NearestAK4JetPt[0], NearestAK4JetEta[0], NearestAK4JetPhi[0], NearestAK4JetMass[0])
            nuCandP4 = ROOT.TLorentzVector( )
            nuCandP4.SetPtEtaPhiM( SemiLepMETpt[0], 0, SemiLepMETphi[0], SemiLepMETpt[0] )
            theLepton = ROOT.TLorentzVector()
            theLepton.SetPtEtaPhiE( LeptonPt[0], LeptonEta[0], LeptonPhi[0], LeptonEnergy[0] ) # Assume massless
            
                
            tau32 = FatJetTau32[0]
            mass_sd = FatJetMassSoftDrop[0]
            bdisc = NearestAK4JetBDisc[0]
            
            bsjet_disc = FatJetSDBDiscB[0]
            wsjet_disc = FatJetSDBDiscW[0]
    
            passKin = hadTopCandP4.Perp() > 200.
            passTopTag = tau32 < 0.7 and mass_sd > 60. 
            passFatJet = wsjet_disc > .8001 or bsjet_disc > .8001
            pass2DCut = LeptonPtRel[0] > 20. or LeptonDRMin[0] > 0.4
            passBtag = bdisc > .8001
            
            if not passKin or not pass2DCut or not passBtag or not passTopTag or not passFatJet:
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

            h_mttbar.Fill( mttbar, SemiLeptWeight[0] )
            h_mtopHadGroomed.Fill( mass_sd, SemiLeptWeight[0] )
            h_mtopHad.Fill( hadTopCandP4.M(), SemiLeptWeight[0] )
        print(count)

        # Original hists have fine binning, change the bins below
        # Eff = PassHt&&PassEL(Mu)/PassHt
        h_effElHt = h_passElHT.Clone("ElectronTriggerEfficiency")
        h_effElHt.Divide(h_passHT,1,1,B)
        h_effMuHt = h_passMuHT.Clone("MuonTriggerEfficiency")
        h_effMuHt.Divide(h_passHT,1,1,B)
        

    fout.cd()
    fout.Write()
    fout.Close()
    
    

if __name__ == "__main__" :
    plot_mttbar(sys.argv)


