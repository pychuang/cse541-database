#!/usr/bin/env python

import argparse
import ConfigParser
import csv
import MySQLdb
import sys

from dataclean import wos

wos_cursor = None
csx_cursor = None


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def match(wos_paperid):
    wos_paper = wos.get_wos_paper_by_id(wos_cursor, wos_paperid)
    print wos_paper
#    wos_paper = wos.get_wos_paper_by_id(wos_cursor, wos_paperid)
#    print wos_paper

    wos_citations = wos.get_citations(wos_cursor, wos_paper)
    print wos_citations
#    wos_citations = wos.get_citations(wos_cursor, wos_paper)
#    print wos_citations

def main(args, config):
    global wos_cursor
    global csx_cursor

    if args.infile:
        inf = open(args.infile, 'rb')
    else:
        inf = sys.stdin

    try:
        wosdb = None
        csxdb = None
        wosdb = connect_db(config, 'wos')
        csxdb = connect_db(config, 'citegraph')
        wos_cursor = wosdb.cursor()
        csx_cursor = csxdb.cursor()

        csvreader = csv.reader(inf)
        for row in csvreader:
            print
            wos_paperid = row[0]
            csx_clusterid = match(wos_paperid)
    finally:
        if wosdb:
            wosdb.close()
        if csxdb:
            csxdb.close()


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Match papers of Web of Science and clusters of citegraph of CiteSeerX.')
    parser.add_argument('-i', '--infile', help='Input CSV file of paper IDs of Web of Science')

    args = parser.parse_args()
    main(args, config)
