#!/usr/bin/env python3

import argparse
import configparser
import csv
import MySQLdb
import os
import random
import sys

from dataclean import utils

import dataclean.wos as wos
import dataclean.citeseerx as csx


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def match(csvwriter, wos_paperid):
    wos_paper = wos.WosPaper.get_paper_by_id(wos_cursor, wos_paperid)

    # ignore papers without title
    if not wos_paper.title:
        return False

    authors = wos_paper.get_authors(wos_cursor)
    print("WOS: %s" % wos_paper)
    csvwriter.writerow(['WoS uid', wos_paper.paper_id])
    csvwriter.writerow(['Title', wos_paper.title])
    csvwriter.writerow(['Authors'] + authors)

    # match title
    cg_clusters = csx.CgCluster.find_clusters_by_title_on_solr_imprecise(solr_url, wos_paper.title)
    if not cg_clusters:
        return True

    normalized_wos_title = utils.normalize_query_string(wos_paper.title)
    for cg_cluster in cg_clusters:
        # ignore clusters without corresponding DOIs
        dois = cg_cluster.get_dois(cg_cursor)
        if not dois:
            continue

        # ignore clusters with low Jaccard
        normalized_cluster_title = utils.normalize_query_string(cg_cluster.title)
        if utils.jaccard(normalized_wos_title, normalized_cluster_title) < 0.7:
            continue

        authors = cg_cluster.get_authors(cg_cursor)
        print("\tCG: %s" % cg_cluster)
        csvwriter.writerow(['Cluster ID', cg_cluster.paper_id])
        csvwriter.writerow(['Title', cg_cluster.title])
        csvwriter.writerow(['Authors'] + authors)
        csvwriter.writerow(['DOIs'] + dois)
    return True


def sampling(csvwriter, wos_paperids, nsamples):
    random.shuffle(wos_paperids)
    count = 0
    for wos_paperid in wos_paperids:
        if match(csvwriter, wos_paperid):
            count += 1
            csvwriter.writerow(['#####'])

        if count >= nsamples:
            break


def main(args, config):
    global wos_cursor
    global cg_cursor
    global solr_url

    solr_url = config.get('solr', 'url')

    if args.infile:
        inf = open(args.infile)
    else:
        inf = sys.stdin

    print('loading input...')
    wos_paperids = []
    csvreader = csv.reader(inf)
    for row in csvreader:
        wos_paperid = row[0]
        wos_paperids.append(wos_paperid)

    if args.outfile:
        outf = open(args.outfile, 'w')
    else:
        outf = open(os.devnull, 'w')
    csvwriter = csv.writer(outf)

    try:
        wosdb = None
        cgdb = None
        wosdb = connect_db(config, 'wos')
        cgdb = connect_db(config, 'citegraph')
        wos_cursor = wosdb.cursor()
        cg_cursor = cgdb.cursor()

        print('sampling...')
        sampling(csvwriter, wos_paperids, args.nsamples)

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

    parser = argparse.ArgumentParser(description='Sample matched papers in Web of Science and papers in CiteSeerX that have DOIs.')
    parser.add_argument('-i', '--infile', help='input CSV file of CS papers')
    parser.add_argument('-o', '--outfile', help='output CSV file of sample results')
    parser.add_argument('-n', '--nsamples', type=int, default=1000, help='number of samples')

    args = parser.parse_args()
    main(args, config)
