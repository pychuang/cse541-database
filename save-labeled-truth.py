#!/usr/bin/env python3

import argparse
import csv
import sys


def convert(s):
    if not s:
        return False
    return bool(int(s))


def main(args):
    if args.infile:
        inf = open(args.infile)
    else:
        inf = sys.stdin

    posfile = open(args.posfile, 'w')
    negfile = open(args.negfile, 'w')
    poscsvwriter = csv.writer(posfile)
    negcsvwriter = csv.writer(negfile)

    csvreader = csv.DictReader(inf)
    for row in csvreader:
        if row['Truth'] == '#####':
            wos_paper_id = row['ID']
            continue

        truth = convert(row['Truth'])
        cluster_id = row['ID']

        if truth:
            poscsvwriter.writerow([wos_paper_id, cluster_id])
        else:
            negcsvwriter.writerow([wos_paper_id, cluster_id])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process labeled result CSV and save labeled truth in simpler format.')
    parser.add_argument('-i', '--infile', help='input CSV file of labeled result')
    parser.add_argument('-p', '--posfile', required=True, help='output CSV file of positive labels')
    parser.add_argument('-n', '--negfile', required=True, help='output CSV file of negative labels')

    args = parser.parse_args()
    main(args)
