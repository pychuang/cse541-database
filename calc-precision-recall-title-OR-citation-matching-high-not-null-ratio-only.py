#!/usr/bin/env python3

import argparse
import csv
import os


def process_file(fname, tjc_threshold, not_null_threshold, not_null_ratio_threshold, field, threshold):
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
                all_citations = int(row[fnmap['#Citation']])
                not_null_citations = int(row[fnmap['#NotNull']])
                if all_citations:
                    not_null_ratio = not_null_citations / all_citations
                else:
                    not_null_ratio = 0
                continue

            cg_cluster_id = row[fnmap['ID']]

            if row[fnmap['Truth']] == '1':
                truth = True
            elif row[fnmap['Truth']] == '0':
                truth = False
            else:
                exit("%s: cluster %s for %s not labeled" % (fname, cg_cluster_id, wos_paper_id))

            # do not consider wos paper with low not_null_ratio
            if not_null_ratio < not_null_ratio_threshold:
                continue

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


def calculate(infiles, tjc_threshold, not_null_threshold, not_null_ratio_threshold, field, threshold):
    true_pos = 0
    false_pos = 0
    false_neg = 0

    for infile in infiles:
        tp, fp, fn = process_file(infile, tjc_threshold, not_null_threshold, not_null_ratio_threshold, field, threshold)
        true_pos += tp
        false_pos += fp
        false_neg += fn

    return true_pos, false_pos, false_neg


def main(args):
    if args.outfile:
        outf = open(args.outfile, 'w')
    else:
        outf = open(os.devnull, 'w')
    csvwriter = csv.writer(outf)

    measures = {'nnr': 'non-NULL matched ratio', 'r': 'matched ratio', 'jc': 'jaccard'}
    title_jaccards = [0.7, 0.8, 0.9]
    citation_title_jaccards = ['0.6', '0.7', '0.8', '0.9']
    not_null_thresholds = [4, 5, 6, 7, 8]
    not_null_ratio_thresholds = [0, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    thresholds = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]

    csvwriter.writerow(['Measure', 'Threshold', 'Title Jaccard', 'Citation Title Jaccard', 'non-NULL', 'Precision', 'Recall', 'F1', 'True Pos', 'False Pos', 'False Neg'])

    for measure, measure_name in measures.items():
        for cjc in citation_title_jaccards:
            # field: cjc0.6nnr, cjc0.6r, cjc0.6jc... etc
            field = 'cjc' + cjc + measure
            print("[%s]" % field)

            for tjc_threshold in title_jaccards:
                for not_null_threshold in not_null_thresholds:
                    print("title jaccard = %.1f, not NULL threshold = %d" % (tjc_threshold, not_null_threshold))

                    for threshold in thresholds:
                        true_pos, false_pos, false_neg = calculate(args.infiles, tjc_threshold, not_null_threshold, args.not_null_ratio_threshold, field, threshold)

                        recall = true_pos / (true_pos + false_neg)
                        if true_pos + false_pos == 0:
                            print("threshold %.1f: precision =  N/A, recall = %.2f, F1 =   N/A (TP = %4d, FP = %4d, FN = %4d)" % (threshold, recall, true_pos, false_pos, false_neg))
                            precision = None
                            f1 = None
                        else:
                            precision = true_pos / (true_pos + false_pos)
                            f1 = 2 * precision * recall / (precision + recall)
                            print("threshold %.1f: precision = %.2f, recall = %.2f, F1 = %.3f (TP = %4d, FP = %4d, FN = %4d)" % (threshold, precision, recall, f1, true_pos, false_pos, false_neg))

                        csvwriter.writerow([measure_name, threshold, tjc_threshold, cjc, not_null_threshold, precision, recall, f1, true_pos, false_pos, false_neg])
            print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the precision, recall and F1 for title matching ORed citation matching.')
    parser.add_argument('-o', '--outfile', help='output CSV file of sample results')
    parser.add_argument('-n', '--not-null-ratio-threshold', type=float, required=True, help='not NULL ratio threshold')
    parser.add_argument('infiles', nargs='+', metavar='INFILE', help='input CSV file of result')

    args = parser.parse_args()
    main(args)
