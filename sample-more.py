#!/usr/bin/env python3

import argparse
import csv
import os
import random
import sys


def main(args):
    if args.outfile:
        outf = open(args.outfile, 'w')
    else:
        outf = open(os.devnull, 'w')
    csvwriter = csv.writer(outf)

    if args.include:
        inf = open(args.include)

    old_set = set()
    csvreader = csv.reader(inf)
    for row in csvreader:
        wos_paperid = row[0]
        csvwriter.writerow(row)
        old_set.add(wos_paperid)

    if args.infile:
        inf = open(args.infile)
    else:
        inf = sys.stdin

    wos_paperids = []
    csvreader = csv.reader(inf)
    for row in csvreader:
        wos_paperid = row[0]
        wos_paperids.append(wos_paperid)

    random.shuffle(wos_paperids)
    count = 0
    for wos_paperid in wos_paperids:
        if wos_paperid in old_set:
            continue

        csvwriter.writerow([wos_paperid])
        count += 1
        if count >= args.nsamples:
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Randomly sampling WoS paper IDs.')
    parser.add_argument('-i', '--infile', help='input CSV file of paper IDs for sampling')
    parser.add_argument('-I', '--include', help='input CSV file of paper IDs that should include')
    parser.add_argument('-o', '--outfile', help='output CSV file of sample results')
    parser.add_argument('-n', '--nsamples', type=int, default=1000, help='number of samples')

    args = parser.parse_args()
    main(args)
