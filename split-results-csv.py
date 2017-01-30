#!/usr/bin/env python3

import argparse
import csv
import os
import sys


def new_csv(out_dir, start, bound):
    outfname = "results-%d-%d.csv" % (start, bound)
    outpath = os.path.join(out_dir, outfname)
    outf = open(outpath, 'w')
    return csv.writer(outf)


def main(args):
    if args.infile:
        inf = open(args.infile)
    else:
        inf = sys.stdin

    csvreader = csv.reader(inf)
    fieldnames = next(csvreader)
    fnmap = {}
    for i, fn in enumerate(fieldnames):
        fnmap[fn] = i

    count = 0

    start = 1
    bound = args.count
    for row in csvreader:
        if row[fnmap['Truth']] == '#####':
            count += 1

        if count == start:
            csvwriter = new_csv(args.out_dir, start, bound)
            csvwriter.writerow(fieldnames)

            start += args.count
            bound += args.count

        csvwriter.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split result CSV into several CSVs.')
    parser.add_argument('-i', '--infile', help='input CSV file of result')
    parser.add_argument('-n', '--count', type=int, required=True, help='number of WoS papers per output CSV file')
    parser.add_argument('-o', '--out-dir', required=True, help='output directory')

    args = parser.parse_args()
    main(args)
