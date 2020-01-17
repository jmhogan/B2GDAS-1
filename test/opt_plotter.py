import numpy as np
import matplotlib.pyplot as plt
import sys
import array as array
from optparse import OptionParser

def opt_plotter(argv) : 
    parser = OptionParser()

    parser.add_option('--signal', type='string', action='store',
                      dest='sig',
                      help='signal file')

    parser.add_option('--background', type='string', action='store',
                      dest='bg',
                      help='background file')

    parser.add_option('--param', type='string', action='store',
                      dest='param',
                      help='Which parameter to plot')

    (options, args) = parser.parse_args(argv)
    argv = []

    print '===== Command line options ====='
    print options
    print '================================'

    sig_in = np.load(options.sig)
    bg_in = np.load(options.bg)

    if np.shape(sig_in) != np.shape(bg_in):
        print("Shapes don't match")

    binlist = sig_in[0][  bg_in[1] > 10 ]
    sig = sig_in[1][  bg_in[1] > 10 ]
    bg  = bg_in[1][ bg_in[1] > 10 ]

    signif = sig / (bg)**.5


    print(np.shape(signif))

    print(sig)
    print(bg)
    print(signif)

    plt.plot(binlist, signif)
    #plt.bar(binlist, signif)
    #plt.figure()
    #plt.plot(sig_in[0],sig_in[1])
    plt.title("%s Optimization" % options.param)
    plt.ylabel("Relative Signifiance")
    plt.xlabel("%s" % options.param)

    #plt.figure()
    #plt.plot(bg_in[0], bg_in[1])

    plt.show()            

if __name__ == "__main__" :
    opt_plotter(sys.argv)
