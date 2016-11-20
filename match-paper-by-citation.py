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
cg_cursor = None
solr_url = None


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def match(wos_paperid, n, threshold):
    wos_paper = wos.WosPaper.get_paper_by_id(wos_cursor, wos_paperid)
    wos_citations = wos.WosPaper.get_citations(wos_cursor, wos_paper)
    print("WOS: %s" % wos_paper)
    print("WOS: %d citations" % len(wos_citations))

    candidate_cg_clusters_ids = collections.defaultdict(int)
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
            candidate_cg_clusters_ids[cg_citing_cluster_id] += 1

    print("%d candidate CG clusters" % len(candidate_cg_clusters_ids))
    if not candidate_cg_clusters_ids:
        return
    nth_count = sorted(set(candidate_cg_clusters_ids.values()), reverse=True)[:n][-1]
    print('nth_count', nth_count, 'threshold', threshold)
    nth_count = max(threshold, nth_count)
    candidate_cg_clusters_ids = {cluster_id: count for cluster_id, count in candidate_cg_clusters_ids.items() if count >= nth_count}
    sorted_candidate_clusters_ids = sorted(candidate_cg_clusters_ids.items(), key=lambda x: x[1], reverse=True)
    for cluster_id, count in sorted_candidate_clusters_ids:
        cluster = csx.CgCluster.get_cluster_by_id(cg_cursor, cluster_id)
        print("%s : count=%d" % (cluster, count))


def main(args, config):
    global wos_cursor
    global cg_cursor
    global solr_url

    solr_url = config.get('solr', 'url')

    if args.infile:
        inf = open(args.infile, 'rb')
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
            cg_clusterid = match(wos_paperid, int(args.n), int(args.threshold))
    finally:
        if wosdb:
            wosdb.close()
        if cgdb:
            cgdb.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Match papers of Web of Science and clusters of citegraph of CiteSeerX.')
    parser.add_argument('-i', '--infile', help='Input CSV file of paper IDs of Web of Science')
    parser.add_argument('-n', default=3, help='Top n results')
    parser.add_argument('-t', '--threshold', default=3, help='threshold for number of citing')

    args = parser.parse_args()
    main(args, config)
