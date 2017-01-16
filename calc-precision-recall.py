#!/usr/bin/env python3

import argparse
import csv
import sys


def process_file(fname, field, threshold):
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
                continue

            if row[fnmap['Truth']] == '1':
                truth = True
            elif row[fnmap['Truth']] == '0':
                truth = False
            else:
                exit("parse error in %s" % fname)

            if not row[fnmap[field]]:
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


def calculate(infiles, field, threshold):
    true_pos = 0
    false_pos = 0
    false_neg = 0

    for infile in infiles:
        tp, fp, fn = process_file(infile, field, threshold)
        true_pos += tp
        false_pos += fp
        false_neg += fn

    recall = true_pos / (true_pos + false_neg)
    if true_pos + false_pos == 0:
        print("threshold %f: precision =  N/A, recall = %.2f, F1 =  N/A (TP = %4d, FP = %4d, FN = %4d)" % (threshold, recall, true_pos, false_pos, false_neg))
        return
    precision = true_pos / (true_pos + false_pos)
    f1 = 2 * precision * recall / (precision + recall)
    print("threshold %f: precision = %.2f, recall = %.2f, F1 = %.2f (TP = %4d, FP = %4d, FN = %4d)" % (threshold, precision, recall, f1, true_pos, false_pos, false_neg))


def main(args):
    fields = ['tjc', 'cjc0.6nnr', 'cjc0.7nnr', 'cjc0.8nnr', 'cjc0.9nnr', 'cjc0.6r', 'cjc0.7r', 'cjc0.8r', 'cjc0.9r', 'cjc0.6jc', 'cjc0.7jc', 'cjc0.8jc', 'cjc0.9jc']
    thresholds = [0.6, 0.7, 0.8, 0.9]
    for field in fields:
        print("[%s]" % field)
        for threshold in thresholds:
            calculate(args.infiles, field, threshold)
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the precision, recall and F1 for all fields.')
    parser.add_argument('infiles', nargs='+', metavar='INFILE', help='input CSV file of result')

    args = parser.parse_args()
    main(args)
