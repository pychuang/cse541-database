#!/usr/bin/env python3

import argparse
import csv
import sys


def convert(s):
    if not s:
        return False
    return bool(int(s))


def main(args):
    known_truth = {}

    with open(args.posfile) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            wos_paper_id, cg_cluster_id = row
            known_truth[(wos_paper_id, cg_cluster_id)] = True

    with open(args.negfile) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            wos_paper_id, cg_cluster_id = row
            known_truth[(wos_paper_id, cg_cluster_id)] = False

    if args.infile:
        inf = open(args.infile)
    else:
        inf = sys.stdin

    if args.outfile:
        outf = open(args.outfile, 'w')
    else:
        outf = sys.stdout

    csvreader = csv.reader(inf)
    fieldnames = next(csvreader)
    fnmap = {}
    for i, fn in enumerate(fieldnames):
        fnmap[fn] = i
    csvwriter = csv.writer(outf)
    csvwriter.writerow(fieldnames)
    for row in csvreader:
        if row[fnmap['Truth']] == '#####':
            wos_paper_id = row[fnmap['ID']]
            csvwriter.writerow(row)
            continue

        cg_cluster_id = row[fnmap['ID']]
        id_pair = (wos_paper_id, cg_cluster_id)
        if id_pair in known_truth:
            if known_truth[id_pair]:
                row[fnmap['Truth']] = 1
            else:
                row[fnmap['Truth']] = 0
        csvwriter.writerow(row)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Apply truth labels to result CSV.')
    parser.add_argument('-i', '--infile', help='input CSV file of result')
    parser.add_argument('-o', '--outfile', help='output CSV file of results')
    parser.add_argument('-p', '--posfile', required=True, help='output CSV file of positive labels')
    parser.add_argument('-n', '--negfile', required=True, help='output CSV file of negative labels')

    args = parser.parse_args()
    main(args)
