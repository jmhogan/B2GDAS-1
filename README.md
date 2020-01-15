B2GDAS
======


CMS Data Analysis School (CMSDAS) exercise for the
Beyond Two Generations Physics Analysis Group (B2G PAG)

To run :

`export SCRAM_ARCH=slc(6,7)_amd64_gcc700` *if using BASH*, pick slc6 or slc7

`setenv SCRAM_ARCH slc(7,6)_amd64_gcc700` *if using TCSH*, pick slc6 or slc7

`cmsrel CMSSW_10_2_16`

`cd CMSSW_10_2_16/src`

`git clone git@github.com:jmhogan/B2GDAS-1.git Analysis/B2GDAS`

`cd Analysis/B2GDAS`

`scram b`

`cd test`

`voms-proxy-init`

Optional: To test n-tuple production

`python b2gdas_fwlite.py --input=inputfiles/RSGluonToTTM2000.txt --output=rsgluon_ttbar_2TeV.root --maxevents 10000`
