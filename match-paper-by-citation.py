#!/usr/bin/env python3

import argparse
import collections
import configparser
import csv
import MySQLdb
import operator
import sys

import dataclean.wos as wos
import dataclean.citeseerx as csx


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def match(wos_paperid, threshold):
    wos_paper = wos.WosPaper.get_paper_by_id(wos_cursor, wos_paperid)
    wos_citations = wos.WosPaper.get_citations(wos_cursor, wos_paper)
    print("WOS: %s" % wos_paper)
    print("WOS: %d citations" % len(wos_citations))

    candidate_cg_cluster_id_counter = collections.defaultdict(int)
    for wos_citation in wos_citations:
        #print("\tWOS citation: %s" % wos_citation)
        cg_citations = csx.CgCluster.find_clusters_by_title_on_solr(solr_url, wos_citation.title)
        if not cg_citations:
            continue

        #print("\tCG: %d citations" % len(cg_citations))
        cg_citing_clusters_ids_set = set()
        for cg_citation in cg_citations:
            #print("\tCG: %s" % cg_citation)
            cg_citing_clusters_ids = cg_citation.find_citing_clusters_ids(cg_cursor)
            cg_citing_clusters_ids_set.update(cg_citing_clusters_ids)

        for cg_citing_cluster_id in cg_citing_clusters_ids_set:
            candidate_cg_cluster_id_counter[cg_citing_cluster_id] += 1

    print("%d candidate CG clusters" % len(candidate_cg_cluster_id_counter))
    if not candidate_cg_cluster_id_counter:
        return
    # get the item with max value
    cg_cluster_id, count = max(candidate_cg_cluster_id_counter.items(), key=operator.itemgetter(1))

    if count < len(wos_citations) * threshold:
        return

    cg_cluster = csx.CgCluster.get_cluster_by_id(cg_cursor, cg_cluster_id)
    dois = cg_cluster.get_dois(cg_cursor)
    cg_citations = csx.CgCluster.get_citations(cg_cursor, cg_cluster)
    (["%d citations" % len(cg_citations)])
    print("%s : #citations=%d, count=%d, DOIs: %s" % (cg_cluster, len(cg_citations), count, ', '.join(dois)))


def main(args, config):
    global wos_cursor
    global cg_cursor
    global solr_url

    solr_url = config.get('solr', 'url')

    if args.infile:
        inf = open(args.infile)
    else:
        inf = sys.stdin

    try:
        wosdb = None
        cgdb = None
        wosdb = connect_db(config, 'wos')
        cgdb = connect_db(config, 'citegraph')
        wos_cursor = wosdb.cursor()
        cg_cursor = cgdb.cursor()

        csvreader = csv.reader(inf)
        for row in csvreader:
            print()
            wos_paperid = row[0]
            cg_clusterid = match(wos_paperid, args.threshold)
    finally:
        if wosdb:
            wosdb.close()
        if cgdb:
            cgdb.close()


if __name__ == '__main__':
    wos_cursor = None
    cg_cursor = None
    solr_url = None

    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Match papers of Web of Science and clusters of citegraph of CiteSeerX.')
    parser.add_argument('-i', '--infile', help='Input CSV file of paper IDs of Web of Science')
    parser.add_argument('-t', '--threshold', type=float, default=0.8, help='threshold for percentage of matched/WoS')

    args = parser.parse_args()
    main(args, config)
