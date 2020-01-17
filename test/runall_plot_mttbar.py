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

TT_0lep_Str = ["--file_in", "root://cmseos.fnal.gov//store/user/cmsdas/2020/long_exercises/B2GTTbar/update2017data/TT_0lep.root", "--file_out", "TT_1lep_plots_elec_T1B1.root", "--leptonType", " electron", "--bTag", "--TopTag" ]
TT_1lep_Str = ["--file_in", "root://cmseos.fnal.gov//store/user/cmsdas/2020/long_exercises/B2GTTbar/update2017data/TT_1lep.root", "--file_out", "TT_1lep_plots_elec_T1B1.root", "--leptonType", " electron", "--bTag", "TopTag" ]
TT_2lep_Str = ["--file_in", "root://cmseos.fnal.gov//store/user/cmsdas/2020/long_exercises/B2GTTbar/update2017data/TT_2lep.root", "--file_out", "TT_1lep_plots_elec_T1B1.root", "--leptonType", " electron", "--bTag", "--TopTag" ]

#----------------------------------------------------------------------------------------------------------------------#

QCD_1000to1500_Str = ["--file_in", "root://cmseos.fnal.gov//store/user/cmsdas/2020/long_exercises/B2GTTbar/update2017data/QCD_1000to1500.root", "--file_out", "TT_1lep_plots.root", "--leptonType", " electron", "--bTag", "--TopTag" ]
QCD_1000to1500_Str = ["--file_in", "root://cmseos.fnal.gov//store/user/cmsdas/2020/long_exercises/B2GTTbar/update2017data/QCD_1000to1500.root", "--file_out", "TT_1lep_plots.root", "--leptonType", " electron", "--bTag", "--TopTag" ]
QCD_1500to2000_Str = ["--file_in", "root://cmseos.fnal.gov//store/user/cmsdas/2020/long_exercises/B2GTTbar/update2017data/QCD_1500to2000.root", "--file_out", "TT_1lep_plots.root", "--leptonType", " electron", "--bTag", "--TopTag" ]
QCD_1500to2000_Str = ["--file_in", "root://cmseos.fnal.gov//store/user/cmsdas/2020/long_exercises/B2GTTbar/update2017data/QCD_2000to2000.root", "--file_out", "TT_1lep_plots.root", "--leptonType", " electron", "--bTag", "--TopTag" ]



plot_mttbar( ttjetsStr )
plot_mttbar( rsgluon3TeVStr )
plot_mttbar( singlemuStr )


