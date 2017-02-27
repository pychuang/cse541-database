#!/usr/bin/env python3

import argparse
import csv
import itertools
import os
import subprocess


def main(args):
    with open(args.summary_file_name) as f:
        csvreader = csv.reader(f)
        fieldnames = next(csvreader)
        target_fields = []
        for fieldname in fieldnames:
            if fieldname == 'Measure':
                continue
            if fieldname in ['Precision', 'Recall', 'F1']:
                break
            target_fields.append(fieldname)

        fnmap = {}
        for i, fn in enumerate(fieldnames):
            fnmap[fn] = i


    dirpath = os.path.join(args.output_basedir, args.prefix)
    print("MKDIR: %s" % dirpath)
    os.makedirs(dirpath, exist_ok=True)

    title_template = "%s of %s"
    measure_full = {'jaccard': 'jaccard', 'nnmr': 'non-NULL matched ratio', 'mr': 'matched ratio'}
    measure = measure_full[args.measure]
    ys = ['Precision', 'Recall', 'F1']
    field_abbrev = {'Threshold': 't', 'Title Jaccard': 'T', 'Citation Title Jaccard': 'j', 'non-NULL': 'n', 'non-NULL ratio': 'r'}

    for y in ys:
        for x, c in itertools.permutations(target_fields, 2):
            title = title_template % (y, args.title_description)
            filename = "%s-%s-%s-%s.png" % (args.prefix, y.lower(), field_abbrev[x], field_abbrev[c])
            outpath = os.path.join(dirpath, filename)

            cmd = ['./plot-summary.py', '-i', args.summary_file_name, '-m', measure, '-t', title, '-o', outpath, '-x', x, '-c', c, '-y', y, '--no-show']
            print('RUN:',  ' '.join(cmd))
            subprocess.call(cmd)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot plots about citations.')
    parser.add_argument('-s', '--summary-file-name', required=True, help='input CSV file of summary')
    parser.add_argument('-t', '--title-description', required=True, help='second part of title')
    parser.add_argument('-b', '--output-basedir', required=True, help='output base directory')
    parser.add_argument('-p', '--prefix', required=True, help='prefix for output directory and file name')
    parser.add_argument('-m', '--measure', required=True, help='measure abbrev')

    args = parser.parse_args()
    main(args)
