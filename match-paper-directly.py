#!/usr/bin/env python3

import argparse
import collections
import configparser
import csv
import MySQLdb
import sys

import dataclean.wos as wos
import dataclean.citeseerx as csx


wos_cursor = None
csx_cursor = None
solr_url = None


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def match(wos_paperid, n):
    wos_paper = wos.WosPaper.get_paper_by_id(wos_cursor, wos_paperid)
    print("WOS: %s" % wos_paper)

    csx_clusters = csx.CsxCluster.find_clusters_by_title(solr_url, wos_paper.title)
    print("CSX: %d clusters" % len(csx_clusters))
    for csx_cluster in csx_clusters:
        print("\tCSX: %s" % csx_cluster)


def main(args, config):
    global wos_cursor
    global csx_cursor
    global solr_url

    solr_url = config.get('solr', 'url')

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
            print()
            wos_paperid = row[0]
            csx_clusterid = match(wos_paperid, int(args.n))
    finally:
        if wosdb:
            wosdb.close()
        if csxdb:
            csxdb.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Match papers of Web of Science and clusters of citegraph of CiteSeerX.')
    parser.add_argument('-i', '--infile', help='Input CSV file of paper IDs of Web of Science')
    parser.add_argument('-n', default=3, help='Max number of results')

    args = parser.parse_args()
    main(args, config)
