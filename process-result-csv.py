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

    union_tp = 0
    union_fp = 0
    union_fn = 0

    intersect_tp = 0
    intersect_fp = 0
    intersect_fn = 0

    wos_papers_that_found_candidates = set()

    if args.infile:
        inf = open(args.infile)
    else:
        inf = sys.stdin

    csvreader = csv.DictReader(inf)
    for row in csvreader:
        if row['Truth'] == '#####':
            wos_paper_id = row['ID']
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

        if cornelia or ours:
            wos_papers_that_found_candidates.add(wos_paper_id)

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

        union = cornelia or ours

        if union and truth:
            union_tp += 1
        elif union and not truth:
            union_fp += 1
        elif not union and truth:
            union_fn += 1

        intersect = cornelia and ours

        if intersect and truth:
            intersect_tp += 1
        elif intersect and not truth:
            intersect_fp += 1
        elif not intersect and truth:
            intersect_fn += 1

    print("%d WoS papers have candidate matches" % len(wos_papers_that_found_candidates))

    cornelia_precision = cornelia_tp / (cornelia_tp + cornelia_fp)
    cornelia_recall = cornelia_tp / (cornelia_tp + cornelia_fn)
    print("[Cornelia]\tprecision=%f, recall=%f" % (cornelia_precision, cornelia_recall))
    ours_precision = ours_tp / (ours_tp + ours_fp)
    ours_recall = ours_tp / (ours_tp + ours_fn)
    print("[Ours]\tprecision=%f, recall=%f" % (ours_precision, ours_recall))
    union_precision = union_tp / (union_tp + union_fp)
    union_recall = union_tp / (union_tp + union_fn)
    print("[Union]\tprecision=%f, recall=%f" % (union_precision, union_recall))
    intersect_precision = intersect_tp / (intersect_tp + intersect_fp)
    intersect_recall = intersect_tp / (intersect_tp + intersect_fn)
    print("[Intersect]\tprecision=%f, recall=%f" % (intersect_precision, intersect_recall))


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Process labeled result CSV.')
    parser.add_argument('-i', '--infile', help='input CSV file of labeled result')

    args = parser.parse_args()
    main(args, config)
