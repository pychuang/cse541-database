#!/usr/bin/env python3

import argparse
import csv
import sys


def process_file(fname, tjc_threshold, not_null_threshold, field, threshold):
    true_pos = 0
    false_pos = 0
    false_neg = 0

    with open(fname) as f:
        csvreader = csv.reader(f)
        fieldnames = next(csvreader)
        fnmap = {}
        for i, fn in enumerate(fieldnames):
            fnmap[fn] = i

        for row in csvreader:
            if row[fnmap['Truth']] == '#####':
                wos_paper_id = row[fnmap['ID']]
                not_null_citations = int(row[fnmap['#NotNull']])
                continue

            cg_cluster_id = row[fnmap['ID']]

            if row[fnmap['Truth']] == '1':
                truth = True
            elif row[fnmap['Truth']] == '0':
                truth = False
            else:
                exit("%s: cluster %s for %s not labeled" % (fname, cg_cluster_id, wos_paper_id))

            if float(row[fnmap['tjc']]) >= tjc_threshold:
                positive = True
            elif not_null_citations < not_null_threshold:
                positive = False
            elif not row[fnmap[field]]:
                positive = False
            else:
                value = float(row[fnmap[field]])
                if value >= threshold:
                    positive = True
                else:
                    positive = False

            if positive and truth:
                true_pos += 1
            elif positive and not truth:
                false_pos += 1
            elif not positive and truth:
                false_neg += 1

    return true_pos, false_pos, false_neg


def calculate(infiles, tjc_threshold, not_null_threshold, field, threshold):
    true_pos = 0
    false_pos = 0
    false_neg = 0

    for infile in infiles:
        tp, fp, fn = process_file(infile, tjc_threshold, not_null_threshold, field, threshold)
        true_pos += tp
        false_pos += fp
        false_neg += fn

    recall = true_pos / (true_pos + false_neg)
    if true_pos + false_pos == 0:
        print("threshold %.1f: precision =  N/A, recall = %.2f, F1 =   N/A (TP = %4d, FP = %4d, FN = %4d)" % (threshold, recall, true_pos, false_pos, false_neg))
        return
    precision = true_pos / (true_pos + false_pos)
    f1 = 2 * precision * recall / (precision + recall)
    print("threshold %.1f: precision = %.2f, recall = %.2f, F1 = %.3f (TP = %4d, FP = %4d, FN = %4d)" % (threshold, precision, recall, f1, true_pos, false_pos, false_neg))


def main(args):
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    # citation matching
    print("Citation Matching with not NULL threshold = %d" % args.not_null_threshold)
    fields = ['cjc0.6nnr', 'cjc0.7nnr', 'cjc0.8nnr', 'cjc0.9nnr', 'cjc0.6r', 'cjc0.7r', 'cjc0.8r', 'cjc0.9r', 'cjc0.6jc', 'cjc0.7jc', 'cjc0.8jc', 'cjc0.9jc']
    for field in fields:
        print("[%s]" % field)
        for threshold in thresholds:
            calculate(args.infiles, args.tjc_threshold, args.not_null_threshold, field, threshold)
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the precision, recall and F1 for title matching ORed citation matching.')
    parser.add_argument('-t', '--tjc-threshold', type=float, default=0.7, help='Threshold for title matching')
    parser.add_argument('-n', '--not-null-threshold', type=int, default=4, help='Threshold for number of citations with non-NULL title')
    parser.add_argument('infiles', nargs='+', metavar='INFILE', help='input CSV file of result')

    args = parser.parse_args()
    main(args)
