import ROOT
import sys
#from https://root-forum.cern.ch/t/loop-over-all-objects-in-a-root-file/10807/3
def getall(d, basepath="/"):
    "Generator function to recurse into a ROOT file/dir and yield (path, obj) pairs"
    for key in d.GetListOfKeys():
        kname = key.GetName()
        if key.IsFolder():
            # TODO: -> "yield from" in Py3
            for i in getall(d.Get(kname), basepath+kname+"/"):
                yield i
        else:
            yield basepath+kname, d.Get(kname)


# Demo
ROOT.gROOT.SetBatch(True)
print "give .root file to process as argument"
assert(len(sys.argv)==2)
outputDir = sys.argv[1]
f = ROOT.TFile(sys.argv[1])
out = ROOT.TFile(sys.argv[1].replace(".root","_Rebinned.root"),"RECREATE")
for k, o in getall(f):
    print o.ClassName(), k
    o.Rebin(10) #feel free to change
    o.Write()
