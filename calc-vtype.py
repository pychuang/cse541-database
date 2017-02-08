#!/usr/bin/env python3

import argparse
import csv
import sys

from collections import defaultdict

def process_file(fname, stats):
    with open(fname) as f:
        csvreader = csv.reader(f)
        fieldnames = next(csvreader)
        fnmap = {}
        for i, fn in enumerate(fieldnames):
            fnmap[fn] = i

        for row in csvreader:
            if row[fnmap['Truth']] == '#####':
                wos_paper_id = row[fnmap['ID']]
                continue

            cg_cluster_id = row[fnmap['ID']]
            vtype = row[fnmap['VType']]
    
            if row[fnmap['Truth']] == '1':
                stats[vtype] += 1
            elif row[fnmap['Truth']] == '0':
                pass
            else:
                exit("cluster %s for %s not labeled" % (cg_cluster_id, wos_paper_id))


def main(args):
    stats = defaultdict(int)

    for infile in args.infiles:
        process_file(infile, stats)

    print(stats)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the distribution of venue types of matched clusters.')
    parser.add_argument('infiles', nargs='+', metavar='INFILE', help='input CSV file of result')

    args = parser.parse_args()
    main(args)
