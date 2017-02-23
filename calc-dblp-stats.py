#!/usr/bin/env python3

import argparse
import sys

from collections import defaultdict
from lxml import etree


def main(args):
    stats = defaultdict(int)
    with open(args.infile, 'rb') as f:
        print("loading %s ..." % args.infile, file=sys.stderr)
        xmldoc = etree.iterparse(f, load_dtd=True, events=('start', 'end'))
        _, root = next(xmldoc)

        count = 0
        current_tag = None
        for event, elem in xmldoc:
            if event == 'end' and elem.tag == current_tag:
                #print(elem.findtext('title'))
                current_tag = None
                elem.clear()
            if event == 'start' and current_tag is None:
                current_tag = elem.tag
                stats[elem.tag] += 1
                count += 1

                print(count, file=sys.stderr, end='\r')
                sys.stderr.flush()

    print(stats)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Calculate the statistics of DBLP dataset.')
    parser.add_argument('-i', '--infile', required=True, help='DBLP XML file')

    args = parser.parse_args()
    main(args)
