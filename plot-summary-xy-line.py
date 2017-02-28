#!/usr/bin/env python3

import argparse
import csv
import matplotlib.cm as cm
import matplotlib.colors as pc
import matplotlib.patches as pp
import matplotlib.pyplot as plt
import sys


def main(args):
    x = []
    y = []
    with open(args.infile) as f:
        csvreader = csv.reader(f)
        fieldnames = next(csvreader)
        fnmap = {}
        for i, fn in enumerate(fieldnames):
            fnmap[fn] = i

        i_x = fnmap[args.x]
        i_y = fnmap[args.y]

        for row in csvreader:
            if row[i_x] == '' or row[i_y] == '':
                continue

            x.append(row[i_x])
            y.append(row[i_y])

    norm = pc.Normalize(0, 1)
    scm = cm.ScalarMappable(norm)

    plt.plot(x, y, marker='.')

    if args.title:
        plt.title(args.title)
    plt.gca().set_xlim([0, 1])
    plt.gca().set_ylim([0, 1])
    plt.xlabel(fieldnames[i_x])
    plt.ylabel(fieldnames[i_y])
    plt.tight_layout()
    if args.outfile:
        print("save as %s" % args.outfile)
        plt.savefig(args.outfile)
    if not args.no_show:
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot summary.')
    parser.add_argument('-i', '--infile', required=True, help='input CSV file of summary')
    parser.add_argument('-o', '--outfile', help='output PNG file')
    parser.add_argument('-x', required=True, help='Column name for X axis')
    parser.add_argument('-y', required=True, help='Column name for Y axis')
    parser.add_argument('-n', '--no-show', action='store_true', help='do not show the plot')
    parser.add_argument('-t', '--title', help='Title for the diagram')

    args = parser.parse_args()
    main(args)
