#!/usr/bin/env python

import argparse
import ConfigParser
import csv


def main(args, config):
    with open(args.input, 'rb') as f:
        csvreader = csv.reader(f)
        count = 0
        empty_paperid = 0
        empty_author = 0
        empty_title = 0
        empty_venue = 0
        empty_year = 0
        empty_volume = 0
        empty_doi = 0
        empty_citedby = 0
        
        for row in csvreader:
            count += 1
            paperid, author, title, venue, year, volume, doi, citedby_paperid = row
            if not paperid:
                empty_paperid += 1
            if not author:
                empty_author += 1
            if not title:
                empty_title += 1
            if not venue:
                empty_venue += 1
            if not year:
                empty_year += 1
            if not volume:
                empty_volume += 1
            if not doi:
                empty_doi += 1
            if not citedby_paperid:
                empty_citedby += 1
            if count % 100 == 0:
                print "\r%d rows read" % count,
        print "\r",

        print "totally %d rows" % count
        print "%d empty paperid (%f)" % (empty_paperid, empty_paperid / float(count))
        print "%d empty author (%f)" % (empty_author, empty_author / float(count))
        print "%d empty title (%f)" % (empty_title, empty_title / float(count))
        print "%d empty venue (%f)" % (empty_venue, empty_venue / float(count))
        print "%d empty year (%f)" % (empty_year, empty_year / float(count))
        print "%d empty volume (%f)" % (empty_volume, empty_volume / float(count))
        print "%d empty doi (%f)" % (empty_doi, empty_doi / float(count))
        print "%d empty citedby (%f)" % (empty_citedby, empty_citedby / float(count))


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Process CSV of citations in Web of Science.')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')

    args = parser.parse_args()
    main(args, config)
