B2GDAS
======


CMS Data Analysis School (CMSDAS) exercise for the
Beyond Two Generations Physics Analysis Group (B2G PAG)

To run :

`export SCRAM_ARCH=slc(6,7)_amd64_gcc700` *if using BASH*, pick slc6 or slc7

`setenv SCRAM_ARCH slc(7,6)_amd64_gcc700` *if using TCSH*, pick slc6 or slc7

`cmsrel CMSSW_10_2_16`

`cd CMSSW_10_2_16/src`

`git clone https://github.com/cmsb2g/B2GDAS.git Analysis/B2GDAS`

`cd Analysis/B2GDAS`

`scram b -j 10`

`cd test`

`voms-proxy-init`

`python b2gdas_fwlite.py --input=inputfiles/RSGluonToTTM2000.txt --output=rsgluon_ttbar_2TeV.root --maxevents 10000`
