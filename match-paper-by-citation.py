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


def match(wos_paperid):
    wos_paper = wos.get_paper_by_id(wos_cursor, wos_paperid)
    print(wos_paper)
    wos_citations = wos.get_citations(wos_cursor, wos_paper)

    '''
    csx_clusters = csx.find_clusters_by_title(csx_cursor, wos_paper.title)
    if not csx_clusters:
        return
    '''

    csx_cluster_candidates = collections.defaultdict(int)
    for wos_citation in wos_citations:
        csx_citations = csx.find_clusters_by_title(csx_cursor, wos_citation.title)
        if not csx_citations:
            continue

        for csx_citation in csx_citations:
            csx_citing_clusters = csx_citation.find_citing_clusters(solr_url)
            for csx_citing_cluster in csx_citing_clusters:
                csx_cluster_candidates[csx_citing_cluster] += 1
    sorted_candidates = sorted(csx_cluster_candidates.items(), key=lambda x: x[1], reverse=True)
    print(sorted_candidates[:3])


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
            csx_clusterid = match(wos_paperid)
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

    args = parser.parse_args()
    main(args, config)
