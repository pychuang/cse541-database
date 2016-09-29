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
    wos_citations = wos.WosPaper.get_citations(wos_cursor, wos_paper)
    print("WOS: %s" % wos_paper)
    print("WOS: %d citations" % len(wos_citations))

    candidate_csx_clusters_ids = collections.defaultdict(int)
    for wos_citation in wos_citations:
        #print("\tWOS citation: %s" % wos_citation)
        csx_citations = csx.CsxCluster.find_clusters_by_title(solr_url, wos_citation.title)
        if not csx_citations:
            continue

        #print("\tCSX: %d citations" % len(csx_citations))
        for csx_citation in csx_citations:
            #print("\tCSX: %s" % csx_citation)
            csx_citing_clusters_ids = csx_citation.find_citing_clusters_ids(csx_cursor)
            for csx_citing_cluster_id in csx_citing_clusters_ids:
                candidate_csx_clusters_ids[csx_citing_cluster_id] += 1
    print("%d candidate CSX clusters" % len(candidate_csx_clusters_ids))
    sorted_candidate_clusters_ids = sorted(candidate_csx_clusters_ids.items(), key=lambda x: x[1], reverse=True)
    for cluster_id, count in sorted_candidate_clusters_ids[:n]:
        cluster = csx.CsxCluster.get_cluster_by_id(csx_cursor, cluster_id)
        print("%s : count=%d" % (cluster, count))


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
