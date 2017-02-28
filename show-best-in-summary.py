#!/usr/bin/env python3

import argparse
import csv
import sys


def main(args):
    result = []
    with open(args.infile) as f:
        csvreader = csv.reader(f)
        fieldnames = next(csvreader)
        fnmap = {}
        for i, fn in enumerate(fieldnames):
            fnmap[fn] = i

        for row in csvreader:
            if row[fnmap['Measure']] != args.measure:
                continue

            result.append(row)
            result = sorted(result, reverse=True, key=lambda x: x[fnmap[args.target]])[:args.n]

    if args.outfile:
        outf = open(args.outfile, 'w')
    else:
        outf = sys.stdout

    csvwriter = csv.writer(outf)
    csvwriter.writerow(fieldnames)
    for row in result:
        csvwriter.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Output rows with best scores in summary CSV')
    parser.add_argument('-i', '--infile', required=True, help='input CSV file of summary')
    parser.add_argument('-o', '--outfile', help='output CSV file')
    parser.add_argument('-m', '--measure', required=True, help='type of Measure')
    parser.add_argument('-t', '--target', required=True, help='target field')
    parser.add_argument('-n', type=int, help='number of best results')

    args = parser.parse_args()
    main(args)
