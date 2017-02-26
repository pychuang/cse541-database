#!/usr/bin/env python3

import argparse
import csv
import matplotlib.cm as cm
import matplotlib.colors as pc
import matplotlib.patches as pp
import matplotlib.pyplot as plt
import sys


def main(args):
    i_x, i_c, i_y = args.columns

    data = []
    print("processing %s" % args.infile)
    with open(args.infile) as f:
        csvreader = csv.reader(f)
        fieldnames = next(csvreader)

        measures = {}
        for row in csvreader:
            m = row[0]
            if m not in measures:
                measures[m] = len(measures)
                if measures[m] == args.measure:
                    print("Measure: %s" % m)
            if measures[m] != args.measure:
                continue

            if row[i_y] == '':
                continue

            d = [row[i] for i in args.columns]
            data.append(d)

    print("X: %s" % fieldnames[i_x])
    print("Color: %s" % fieldnames[i_c])

    vmin = min(d[1] for d in data)
    vmax = max(d[1] for d in data)
    norm = pc.Normalize(vmin, vmax)
    scm = cm.ScalarMappable(norm)

    for x, c, y in data:
        color = scm.to_rgba(c)
        plt.plot([x], [y], color=color, marker='+', markeredgecolor=color, markeredgewidth=1)

    cfield = fieldnames[i_c]
    cvalues = sorted(set(c for x, c, y in data))
    patches = [pp.Patch(color=scm.to_rgba(c), label="%s = %s" % (cfield, c)) for c in cvalues]
    plt.legend(handles=patches, loc='best')

    if args.title:
        plt.title(args.title)
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
    parser.add_argument('-n', '--no-show', action='store_true', help='do not show the plot')
    parser.add_argument('-m', '--measure', type=int, required=True, help='type of Measure: 0, 1, 2...')
    parser.add_argument('-t', '--title', help='Title for the diagram')
    parser.add_argument('columns', nargs=3, metavar='COLUMN', type=int, help='list of columns to be used: X, C, Y')

    args = parser.parse_args()
    main(args)
