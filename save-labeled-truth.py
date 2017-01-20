#!/usr/bin/env python3

import argparse
import csv


def process_file(fname, poscsvwriter, negcsvwriter):
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

            cluster_id = row[fnmap['ID']]

            if row[fnmap['Truth']] == '1':
                poscsvwriter.writerow([wos_paper_id, cluster_id])
            elif row[fnmap['Truth']] == '0':
                negcsvwriter.writerow([wos_paper_id, cluster_id])
            else:
                exit("parse error in %s" % fname)


def main(args):
    posfile = open(args.posfile, 'w')
    negfile = open(args.negfile, 'w')
    poscsvwriter = csv.writer(posfile)
    negcsvwriter = csv.writer(negfile)

    for infile in args.infiles:
        process_file(infile, poscsvwriter, negcsvwriter)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process labeled result CSV and save labeled truth in simpler format.')
    parser.add_argument('-p', '--posfile', required=True, help='output CSV file of positive labels')
    parser.add_argument('-n', '--negfile', required=True, help='output CSV file of negative labels')
    parser.add_argument('infiles', nargs='+', metavar='INFILE', help='input CSV file of labeled result')

    args = parser.parse_args()
    main(args)
