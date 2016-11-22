#!/usr/bin/env python3

import argparse
import configparser
import csv
import MySQLdb
import os
import random
import sys

import dataclean.wos as wos
import dataclean.citeseerx as csx


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def match(wos_paperid):
    wos_paper = wos.WosPaper.get_paper_by_id(wos_cursor, wos_paperid)

    # ignore papers without title
    if not wos_paper.title:
        return None

    # match title
    cg_clusters = csx.CgCluster.find_clusters_by_title(cg_cursor, wos_paper.title)
    if not cg_clusters:
        return None

    # ignore clusters without corresponding DOIs
    cg_clusters_with_dois = []
    for cg_cluster in cg_clusters:
        if not cg_cluster.get_dois(cg_cursor):
            continue
        cg_clusters_with_dois.append(cg_cluster)

    if not cg_clusters_with_dois:
        return None

    print(wos_paper.paper_id)
    return (wos_paper, cg_clusters_with_dois)


def sampling(wos_paperids, nsamples):
    random.shuffle(wos_paperids)
    sample_pairs = []
    for wos_paperid in wos_paperids:
        pair = match(wos_paperid)
        if not pair:
            continue
        sample_pairs.append(pair)
        if len(sample_pairs) >= nsamples:
            break
    return sample_pairs


def output(csvwriter, wos_paper, cg_clusters):
    # WoS papers
    print(wos_paper.paper_id)
    csvwriter.writerow(['WoS uid', wos_paper.paper_id])
    csvwriter.writerow(['Title', wos_paper.title])

    wos_citations = wos.WosPaper.get_citations(wos_cursor, wos_paper)
    csvwriter.writerow(["%d citations" % len(wos_citations)])
    for citation in wos_citations:
        csvwriter.writerow([citation.paper_id, citation.title])

    # CiteSeerX papers
    for cg_cluster in cg_clusters:
        csvwriter.writerow(['Cluster ID', cg_cluster.paper_id])
        csvwriter.writerow(['Title', cg_cluster.title])

        dois = cg_cluster.get_dois(cg_cursor)
        csvwriter.writerow(['DOIs'] + dois)

        cg_citations = csx.CgCluster.get_citations(cg_cursor, cg_cluster)
        csvwriter.writerow(["%d citations" % len(cg_citations)])
        for citation in cg_citations:       
            csvwriter.writerow([citation.paper_id, citation.title])
    csvwriter.writerow(['#####'])


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
        samples = sampling(wos_paperids, args.nsamples)

        print('output...')
        for wos_paper, cg_clusters in samples:
            output(csvwriter, wos_paper, cg_clusters)
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
