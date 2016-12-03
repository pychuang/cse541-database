#!/usr/bin/env python3

import argparse
import collections
import configparser
import csv
import MySQLdb
import os
import random
import sys


def convert(s):
    if not s:
        return False
    return bool(int(s))


def main(args, config):
    cornelia_tp = 0
    cornelia_fp = 0
    cornelia_fn = 0

    ours_tp = 0
    ours_fp = 0
    ours_fn = 0

    combined_tp = 0
    combined_fp = 0
    combined_fn = 0

    if args.infile:
        inf = open(args.infile)
    else:
        inf = sys.stdin

    csvreader = csv.DictReader(inf)
    for row in csvreader:
        if row['Truth'] == '#####':
            wos_paper_id = row['ID']
            print(wos_paper_id)
            continue

        truth = row['Truth']
        cornelia = row['Cornelia']
        ours = row['Ours']
        cluster_id = row['ID']

        if (cornelia == '1' or ours == '1') and (truth != '1' and truth != '0'):
            print('ERROR', wos_paper_id, cluster_id)
            exit(1)

        truth = convert(truth)
        cornelia = convert(cornelia)
        ours = convert(ours)


        if cornelia and truth:
            cornelia_tp += 1
        elif cornelia and not truth:
            cornelia_fp += 1
        elif not cornelia and truth:
            cornelia_fn += 1

        if ours and truth:
            ours_tp += 1
        elif ours and not truth:
            ours_fp += 1
        elif not ours and truth:
            ours_fn += 1

        combined = cornelia or ours

        if combined and truth:
            combined_tp += 1
        elif combined and not truth:
            combined_fp += 1
        elif not combined and truth:
            combined_fn += 1



    cornelia_precision = cornelia_tp / (cornelia_tp + cornelia_fp)
    cornelia_recall = cornelia_tp / (cornelia_tp + cornelia_fn)
    print("[Cornelia]\tprecision=%f, recall=%f" % (cornelia_precision, cornelia_recall))
    ours_precision = ours_tp / (ours_tp + ours_fp)
    ours_recall = ours_tp / (ours_tp + ours_fn)
    print("[Ours]\tprecision=%f, recall=%f" % (ours_precision, ours_recall))
    combined_precision = combined_tp / (combined_tp + combined_fp)
    combined_recall = combined_tp / (combined_tp + combined_fn)
    print("[Combined]\tprecision=%f, recall=%f" % (combined_precision, combined_recall))


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Process labeled result CSV.')
    parser.add_argument('-i', '--infile', help='input CSV file of labeled result')

    args = parser.parse_args()
    main(args, config)
