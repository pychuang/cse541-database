#!/usr/bin/env python3

import argparse
import csv
import matplotlib.pyplot as plt
import sys


def process_file(fname, citation_counts, not_null, missing, not_null_ratio):
    with open(fname) as f:
        csvreader = csv.reader(f)
        fieldnames = next(csvreader)
        fnmap = {}
        for i, fn in enumerate(fieldnames):
            fnmap[fn] = i

        for row in csvreader:
            if row[fnmap['Truth']] == '#####':
                wos_paper_id = row[fnmap['ID']]
                wos_citations = int(row[fnmap['#Citation']])
                wos_not_null_citations = int(row[fnmap['#NotNull']])

                citation_counts.append(wos_citations)
                if wos_citations > 0:
                    not_null.append(wos_not_null_citations)

                    m =  wos_citations - wos_not_null_citations
                    missing.append(m)

                    r = wos_not_null_citations / wos_citations
                    not_null_ratio.append(r)

def main(args):
    citation_counts = []
    not_null = []
    missing = []
    not_null_ratio = []

    for infile in args.infiles:
        process_file(infile, citation_counts, not_null, missing, not_null_ratio)

    plt.title('Distribution of number of citations')
    plt.hist(citation_counts, max(citation_counts) + 1, histtype='stepfilled')
    plt.xlabel('#citations')
    plt.ylabel('#papers')
    plt.tight_layout()
    plt.savefig('sampled-papers-citations.png')
    plt.show()

    plt.title('Distribution of ratios of citations with non-NULL titles')
    plt.hist(not_null_ratio, 100)
    plt.xlabel('ratio of citations with non-NULL titles')
    plt.ylabel('#papers')
    plt.tight_layout()
    plt.savefig('sampled-papers-citations-not-null-ratio.png')
    plt.show()

    plt.title('Distribution of ratios of citations with non-NULL titles')
    plt.hist(not_null_ratio, 100, cumulative=-1, normed=True, histtype='step', label='cumulative percentage')
    plt.hist(not_null_ratio, 100, cumulative=True, normed=True, histtype='step', label='reversed cumulative percentage')
    plt.xlabel('ratio of citations with non-NULL titles')
    plt.ylabel('percentage of papers')
    plt.legend()
    plt.tight_layout()
    plt.savefig('sampled-papers-citations-not-null-ratio-cumulative.png')
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Plot plots about citations.')
    parser.add_argument('infiles', nargs='+', metavar='INFILE', help='input CSV file of result')

    args = parser.parse_args()
    main(args)
