"""
draw a histogram of the distribution of a given column
and check for uniformity with the chisq test.
"""
import argparse
import numpy as np
from chart import chart
from _common import pairwise

def run(args):
    # get rid of N, just keep the correlation.
    col_num = args.c if args.c < 0 else (args.c - 1)
    file_iter =  (l.rstrip("\r\n").split("\t")
                  for l in open(args.file) if l[0] != "#")

    pvals = np.array([float(b[col_num]) for b in file_iter])
    kwargs = {"bins": args.n } if args.n else {}
    hist, bins = np.histogram(pvals, normed=True, **kwargs)
    xlabels = "|".join("%.2f-%.2f" % b for b in pairwise(bins))
    print "#", chart(hist, xlabels)
    hist, bins = np.histogram(pvals, normed=False, **kwargs)
    try:
        from scipy.stats import chisquare
        chisq, p = chisquare(hist)
        print "#chi-square test of uniformity. p-val: %.3g " \
              "(low value means reject null of uniformity)" % p
    except ImportError:
        pass
    print "#bin_start\tbin_end\tn"
    for bin, val in zip(pairwise(bins), hist):
        print "%.2f\t%.2f\t%i" % (bin[0], bin[1], val)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                   formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-c", dest="c", help="column number for the histogram",
                   type=int, default=-1)
    p.add_argument("-n", dest="n", help="number of bins in the histogram",
                   type=int, default=None)
    p.add_argument('file', help='bed file to correct')
    args = p.parse_args()
    return run(args)

if __name__ == "__main__":
    import doctest
    if doctest.testmod(optionflags=doctest.ELLIPSIS |\
                                   doctest.NORMALIZE_WHITESPACE).failed == 0:
        main()