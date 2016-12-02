#!/usr/bin/env python3

import argparse
import collections
import configparser
import csv
import MySQLdb
import os
import random
import sys

import dataclean.wos as wos
import dataclean.citeseerx as csx

from dataclean import utils


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def high_jaccard(wos_paper, cg_cluster):
    normalized_wos_title = utils.normalize_query_string(wos_paper.title)
    normalized_cluster_title = utils.normalize_query_string(cg_cluster.title)
    return utils.jaccard(normalized_wos_title, normalized_cluster_title) >= 0.7


def cornelia_match(wos_paper, cg_clusters):
    if not cg_clusters:
        return set()

    selected_clusters = set()
    for cg_cluster in cg_clusters:
        # ignore clusters with low Jaccard
        dois = cg_cluster.get_dois(cg_cursor)
        if high_jaccard(wos_paper, cg_cluster):
            print("\t-> CG: %s, DOIs: %s" % (cg_cluster, ', '.join(dois)))
            selected_clusters.add(cg_cluster)
        else:
            print("\t   CG: %s, DOIs: %s" % (cg_cluster, ', '.join(dois)))
    return selected_clusters


def my_match(wos_paper, threshold):
    wos_citations = wos.WosPaper.get_citations(wos_cursor, wos_paper)
    print("\tWOS: %d citations" % len(wos_citations))
    # too few citations to get reasonable results
    if len(wos_citations) <= 3:
        return set()

    candidate_cg_cluster_id_counter = collections.defaultdict(int)
    for wos_citation in wos_citations:
        #print("\t\tWOS citation: %s" % wos_citation)
        cg_citations = csx.CgCluster.find_clusters_by_title_on_solr_imprecise(solr_url, wos_citation.title)
        if not cg_citations:
            continue

        count = 0
        print("\t\tCG: %d citations" % len(cg_citations))
        cg_citing_clusters_ids_set = set()
        for cg_citation in cg_citations:
            if not high_jaccard(wos_citation, cg_citation):
                continue
            count+=1
            cg_citing_clusters_ids = cg_citation.find_citing_clusters_ids(cg_cursor)
            cg_citing_clusters_ids_set.update(cg_citing_clusters_ids)
        print("\t\tCG: %d citations being considered" % count)

        for cg_citing_cluster_id in cg_citing_clusters_ids_set:
            candidate_cg_cluster_id_counter[cg_citing_cluster_id] += 1

    print("\t%d candidate CG clusters" % len(candidate_cg_cluster_id_counter))
    if not candidate_cg_cluster_id_counter:
        return set()

    candidate_cg_cluster_id_counter = {cid: count for cid, count in candidate_cg_cluster_id_counter.items() if count >= len(wos_citations) * threshold}

    selected_clusters = set()
    for cg_cluster_id, count in candidate_cg_cluster_id_counter.items():
        cg_cluster = csx.CgCluster.get_cluster_by_id(cg_cursor, cg_cluster_id)
        cg_cluster.get_authors(cg_cursor)
        dois = cg_cluster.get_dois(cg_cursor)
        cg_citations = csx.CgCluster.get_citations(cg_cursor, cg_cluster)
        selected_clusters.add(cg_cluster)
        print("\t-> CG: %s : #citations=%d, count=%d, DOIs: %s" % (cg_cluster, len(cg_citations), count, ', '.join(dois)))
    return selected_clusters


def match(csvwriter, wos_paperid, threshold):
    wos_paper = wos.WosPaper.get_paper_by_id(wos_cursor, wos_paperid)

    # ignore papers without title
    if not wos_paper.title:
        return False

    authors = wos_paper.get_authors(wos_cursor)
    print("WOS: %s" % wos_paper)
    csvwriter.writerow(['#####', None, None, wos_paper.paper_id, wos_paper.title, wos_paper.year] + authors)

    # match title
    cg_clusters = csx.CgCluster.find_clusters_by_title_on_solr_imprecise(solr_url, wos_paper.title)
    candidate_clusters = []
    for cg_cluster in cg_clusters:
        # ignore clusters without corresponding DOIs
        dois = cg_cluster.get_dois(cg_cursor)
        if not dois:
            continue
        candidate_clusters.append(cg_cluster)

    print("\tCG: %d candidate clusters" % len(candidate_clusters))

    cornelia_selected_clusters = cornelia_match(wos_paper, candidate_clusters)
    print('\t-----')
    my_selected_clusters = my_match(wos_paper, threshold)

    all_candidate_clusters = set(candidate_clusters) | my_selected_clusters
    for cg_cluster in all_candidate_clusters:
        authors = cg_cluster.get_authors(cg_cursor)
        dois = cg_cluster.get_dois(cg_cursor)

        if cg_cluster in cornelia_selected_clusters:
            cornelia_selected = 1
        else:
            cornelia_selected = None

        if cg_cluster in my_selected_clusters:
            we_selected = 1
        else:
            we_selected = None

        csvwriter.writerow([None, cornelia_selected, we_selected, cg_cluster.paper_id, cg_cluster.title, cg_cluster.year] + authors + dois)

    print('#####')
    return True


def sampling(csvwriter, wos_paperids, nsamples, threshold):
    csvwriter.writerow(['Truth', 'Cornelia', 'Ours', 'ID', 'Title', 'Year'])
    random.shuffle(wos_paperids)
    count = 0
    for wos_paperid in wos_paperids:
        if match(csvwriter, wos_paperid, threshold):
            count += 1

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
        sampling(csvwriter, wos_paperids, args.nsamples, args.threshold)

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
    parser.add_argument('-t', '--threshold', type=float, default=0.8, help='threshold for percentage of matched/WoS')

    args = parser.parse_args()
    main(args, config)
