#!/usr/bin/env python3

import argparse
import csv
import matplotlib.pyplot as plt
import sys


def convert(row, fnmap,  field):
    d = row[fnmap[field]]
    if not d:
        return 0
    return float(d)


def main(args):
    wos_ratio = []
    csx_ratio = []
    jaccard = []

    with open(args.infile) as f:
        csvreader = csv.reader(f)
        fieldnames = next(csvreader)
        fnmap = {}
        for i, fn in enumerate(fieldnames):
            fnmap[fn] = i

        for row in csvreader:
            w = convert(row, fnmap, 'matched/WoS')
            c = convert(row, fnmap, 'matched/CSX')
            j = convert(row, fnmap, 'Jaccard')

            wos_ratio.append(w)
            csx_ratio.append(c)
            jaccard.append(j)


    plt.hist(wos_ratio, 50, label='Citation matched ratio of WoS paper')
    plt.xlabel('ratio')
    plt.legend()
    plt.savefig('100-manual-label-wos-matched-ratio.png')
    plt.show()

    plt.hist(csx_ratio, 50, label='Citation matched ratio of CiteSeerX cluster')
    plt.xlabel('ratio')
    plt.legend()
    plt.savefig('100-manual-label-csx-matched-ratio.png')
    plt.show()

    plt.hist(jaccard, 50, label='Jaccard of citations between CiteSeerX and WoS')
    plt.xlabel('Jaccard similarity')
    plt.legend()
    plt.savefig('100-manual-label-jaccard.png')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot 100 manually labeled results.')
    parser.add_argument('-i', '--infile', required=True, help='input CSV file of result')

    args = parser.parse_args()
    main(args)
