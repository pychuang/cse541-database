#!/usr/bin/env python3

import argparse

from collections import defaultdict
from lxml import etree


def main(args):
    with open(args.infile) as f:
        print("loading %s ..." % args.infile)
        parser = etree.XMLParser(load_dtd=True)
        tree = etree.parse(f, parser)

    root = tree.getroot()

    stats = defaultdict(int)
    for child in root:
        stats[child.tag] += 1

    print(stats)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the statistics of DBLP dataset.')
    parser.add_argument('-i', '--infile', required=True, help='DBLP XML file')

    args = parser.parse_args()
    main(args)
