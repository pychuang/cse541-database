#!/usr/bin/env python3

import argparse
import csv
import sys


def process_file(fname):
    print("processing %s..." % fname)
    n_wos_papers = 0
    wos_papers_with_matches = set()

    with open(fname) as f:
        csvreader = csv.reader(f)
        fieldnames = next(csvreader)
        fnmap = {}
        for i, fn in enumerate(fieldnames):
            fnmap[fn] = i

        for row in csvreader:
            if row[fnmap['Truth']] == '#####':
                wos_paper_id = row[fnmap['ID']]
                n_wos_papers += 1
                continue

            cg_cluster_id = row[fnmap['ID']]
    
            if row[fnmap['Truth']] == '1':
                wos_papers_with_matches.add(wos_paper_id)
            elif row[fnmap['Truth']] == '0':
                pass
            else:
                exit("cluster %s for %s not labeled" % (cg_cluster_id, wos_paper_id))

    return (n_wos_papers, wos_papers_with_matches)

def main(args):
    n_wos_papers = 0
    wos_papers_with_matches = set()
    for infile in args.infiles:
        n, pset = process_file(infile)
        n_wos_papers += n
        wos_papers_with_matches.update(pset)

    n_wos_papers_with_matches = len(wos_papers_with_matches)
    overlap_ratio = n_wos_papers_with_matches / n_wos_papers
    print("In %d WoS papers, %d of them have matched clusters (%.2f%%)" % (n_wos_papers, n_wos_papers_with_matches, overlap_ratio * 100))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the ratio that WoS papers can find corresponding cluster in CiteSeerX citegraph.')
    parser.add_argument('infiles', nargs='+', metavar='INFILE', help='input CSV file of result')

    args = parser.parse_args()
    main(args)
