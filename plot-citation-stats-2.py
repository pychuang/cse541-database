#!/usr/bin/env python3

import argparse
import csv
import matplotlib.pyplot as plt
import sys


def process_file(fname, citation_counts, not_null, null, not_null_ratio):
    wos_paper_count = 0
    with open(fname) as f:
        csvreader = csv.reader(f)
        fieldnames = next(csvreader)
        fnmap = {}
        for i, fn in enumerate(fieldnames):
            fnmap[fn] = i

        for row in csvreader:
            if row[fnmap['Truth']] == '#####':
                wos_paper_count += 1
                wos_paper_id = row[fnmap['ID']]
                wos_citations = int(row[fnmap['#Citation']])
                wos_not_null_citations = int(row[fnmap['#NotNull']])

                citation_counts.append(wos_citations)
                not_null.append(wos_not_null_citations)
                if wos_citations == 0:
                    not_null_ratio.append(0)
                else:
                    m =  wos_citations - wos_not_null_citations
                    null.append(m)

                    r = wos_not_null_citations / wos_citations
                    not_null_ratio.append(r)

        return wos_paper_count


def main(args):
    citation_counts = []
    not_null = []
    null = []
    not_null_ratio = []

    wos_paper_count = 0
    for infile in args.infiles:
        wos_paper_count += process_file(infile, citation_counts, not_null, null, not_null_ratio)

    print("%d WoS papers" % wos_paper_count)
    print("%d WoS papers have no citation" % citation_counts.count(0))
    print("%d WoS papers have no non-NULL citations" % not_null.count(0))
    print("%d WoS papers have no NULL citations" % null.count(0))

    plt.title('Distribution of number of citations')
    plt.hist(citation_counts, max(citation_counts) + 1, histtype='stepfilled')
    plt.xlabel('#citations')
    plt.ylabel('#papers')
    plt.tight_layout()
    plt.savefig('sampled-papers-citations.png')
    plt.show()

    plt.title('Distribution of of number of citations with non-NULL titles')
    plt.hist(not_null, 200, histtype='stepfilled')
    plt.xlabel('#citations with non-NULL titles')
    plt.ylabel('#papers')
    plt.tight_layout()
    plt.savefig('sampled-papers-citations-not-null.png')
    plt.show()

    plt.title('Distribution of of number of citations with NULL titles')
    plt.hist(null, 120, histtype='stepfilled')
    plt.xlabel('#citations with NULL titles')
    plt.ylabel('#papers')
    plt.tight_layout()
    plt.savefig('sampled-papers-citations-null.png')
    plt.show()

    plt.title('Distribution of ratios of citations with non-NULL titles')
    plt.hist(not_null_ratio, 100, histtype='stepfilled')
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
