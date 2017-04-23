#!/usr/bin/env python3

import argparse
import csv
import matplotlib.pyplot as plt
import operator
import sys

from collections import defaultdict


def main(args):
    stats = defaultdict(int)
    with open(args.infile) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            doctype, count = row
            stats[doctype] = int(count)

    if args.types:
        n = args.types
    else:
        n = len(stats)

    sorted_stats = sorted(stats.items(), reverse=True, key=operator.itemgetter(1))
    sorted_stats = sorted_stats[:n]
    print(sorted_stats)
    print(len(sorted_stats))

    left_x = range(n)
    heights = []
    bar_labels = []

    for k, v in sorted_stats:
        heights.append(v)
        bar_labels.append(k)

    plt.title('Documents in WoS')
    plt.bar(left_x, heights, align='center')
    plt.xticks(left_x, bar_labels, rotation=60)
    plt.xlim(-1, n)
    plt.xlabel('types')
    plt.ylabel('count')
    plt.tight_layout()
    plt.savefig('wos-doctypes.png')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot doctypes of WoS dataset.')
    parser.add_argument('-i', '--infile', required=True, help='input CSV file')
    parser.add_argument('-n', '--types', type=int, help='plot only top N types')

    args = parser.parse_args()
    main(args)
