#!/usr/bin/env python3

import argparse
import csv
import sys


def main(args):
    data = []
    with open(args.infile) as f:
        csvreader = csv.reader(f)
        fieldnames = next(csvreader)
        fnmap = {}
        for i, fn in enumerate(fieldnames):
            fnmap[fn] = i

        for row in csvreader:
            if row[fnmap['Measure']] != args.measure:
                continue

            precision = row[fnmap['Precision']]
            recall = row[fnmap['Recall']]

            if precision == '' or recall == '':
                continue

            # round down to the second decimal place
            precision = int(float(precision) * 100) / 100
            recall = int(float(recall) * 100) / 100

            data.append((precision, recall))

    data.sort(reverse=True)

    if args.outfile:
        outf = open(args.outfile, 'w')
    else:
        outf = sys.stdout

    csvwriter = csv.writer(outf)
    csvwriter.writerow(['Precision', 'Recall'])

    prev = None
    for precision, recall in data:
        if prev != precision:
            prev = precision
            csvwriter.writerow([precision, recall])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Summarize best recall')
    parser.add_argument('-i', '--infile', required=True, help='input CSV file of summary')
    parser.add_argument('-o', '--outfile', help='output CSV file of results')
    parser.add_argument('-m', '--measure', required=True, help='type of Measure')

    args = parser.parse_args()
    main(args)
