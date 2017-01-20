#!/usr/bin/env python3

import argparse
import collections
import configparser
import csv
import MySQLdb
import os
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


def get_wos_citation_count(cursor, wos_paperid):
    cursor.execute("""
        SELECT COUNT(*)
        FROM citations
        WHERE paperid = %s;""", (wos_paperid, ))
    result = cursor.fetchone()
    return result[0]


def get_wos_not_null_citation_count(cursor, wos_paperid):
    cursor.execute("""
        SELECT COUNT(*)
        FROM citations
        WHERE paperid = %s AND citedTitle IS NOT NULL;""", (wos_paperid, ))
    result = cursor.fetchone()
    return result[0]


def get_cg_citation_count(cursor, cg_clusterid):
    cursor.execute("""
        SELECT COUNT(*)
        FROM citegraph
        WHERE citing = %s;""", (cg_clusterid, ))
    result = cursor.fetchone()
    return result[0]


def jaccard(wos_paper, cg_cluster):
    normalized_wos_title = utils.normalize_query_string(wos_paper.title)
    normalized_cluster_title = utils.normalize_query_string(cg_cluster.title)
    return utils.jaccard(normalized_wos_title, normalized_cluster_title)


def title_match(wos_paper):
    cg_clusters = csx.CgCluster.find_clusters_by_title_on_solr_imprecise(solr_url, wos_paper.title)
    candidate_clusters = set()
    for cg_cluster in cg_clusters:
        # ignore clusters without corresponding DOIs
        dois = cg_cluster.get_dois(cg_cursor)
        if not dois:
            continue
        candidate_clusters.add(cg_cluster)
    return candidate_clusters


def citation_match(wos_paper):
    wos_citations = wos.WosPaper.get_citations(wos_cursor, wos_paper)
    print("\tWOS: %d citations" % len(wos_citations))

    citeinfo = {}
    for wos_citation in wos_citations:
        cg_citations = csx.CgCluster.find_clusters_by_title_on_solr_imprecise(solr_url, wos_citation.title)
        if not cg_citations:
            continue

        candidates = []
        for cg_citation in cg_citations:
            jc = jaccard(wos_citation, cg_citation)
            if jc < 0.6:
                continue

            candidate = {}
            candidate['jaccard'] = jc
            candidate['cg_cluster'] = cg_citation
            candidate['citing_clusters_ids'] = cg_citation.find_citing_clusters_ids(cg_cursor)
            candidates.append(candidate)

        citeinfo[wos_citation] = candidates
    return citeinfo


def infer_clusters_by_cgcount(wos_paperid, citeinfo, jaccard_threshold):
    # too few citations to get reasonable results
    if len(citeinfo) <= 3:
        return {}

    candidate_cg_cluster_id_counter = collections.defaultdict(int)
    for wos_citation, candidates in citeinfo.items():
        cg_citing_clusters_ids_set = set()
        for candidate in candidates:
            if candidate['jaccard'] < jaccard_threshold:
                continue
            cg_citing_clusters_ids = candidate['citing_clusters_ids']
            cg_citing_clusters_ids_set.update(cg_citing_clusters_ids)

        for cg_citing_cluster_id in cg_citing_clusters_ids_set:
            candidate_cg_cluster_id_counter[cg_citing_cluster_id] += 1

    print("\t%d candidate CG clusters" % len(candidate_cg_cluster_id_counter))
    wos_citation_count = get_wos_citation_count(wos_cursor, wos_paperid)
    wos_notnull_citation_count = len(citeinfo)
    cg_clusters_and_ratio = {}
    for cg_cluster_id, count in candidate_cg_cluster_id_counter.items():
        if count < wos_notnull_citation_count * 0.5:
            continue
        cg_cluster = csx.CgCluster.get_cluster_by_id(cg_cursor, cg_cluster_id)
        cg_clusters_and_ratio[cg_cluster] = (count, count / wos_citation_count, count / wos_notnull_citation_count)
        dois = cg_cluster.get_dois(cg_cursor)
        print("\t-> CG: %s : DOIs: %s" % (cg_cluster, ', '.join(dois)))

    return cg_clusters_and_ratio


def match(csvwriter, wos_paperid):
    wos_paper = wos.WosPaper.get_paper_by_id(wos_cursor, wos_paperid)

    # ignore papers without title
    if not wos_paper.title:
        return

    authors = wos_paper.get_authors(wos_cursor)
    print("WOS: %s" % wos_paper)
    wos_citation_count = get_wos_citation_count(wos_cursor, wos_paperid)
    not_null_citation_count = get_wos_not_null_citation_count(wos_cursor, wos_paperid)
    csvwriter.writerow(['#####'] + [None] * 13 + [wos_paper.paper_id, wos_citation_count, not_null_citation_count, wos_paper.title, wos_paper.year] + authors)

    # match title
    t_candidate_clusters = title_match(wos_paper)

    # match citation
    citeinfo = citation_match(wos_paper)
    cjc6_candidate_clusters_and_ratio = infer_clusters_by_cgcount(wos_paperid, citeinfo, 0.6)
    cjc6_candidate_clusters = cjc6_candidate_clusters_and_ratio.keys()
    cjc7_candidate_clusters_and_ratio = infer_clusters_by_cgcount(wos_paperid, citeinfo, 0.7)
    cjc7_candidate_clusters = cjc7_candidate_clusters_and_ratio.keys()
    cjc8_candidate_clusters_and_ratio = infer_clusters_by_cgcount(wos_paperid, citeinfo, 0.8)
    cjc8_candidate_clusters = cjc8_candidate_clusters_and_ratio.keys()
    cjc9_candidate_clusters_and_ratio = infer_clusters_by_cgcount(wos_paperid, citeinfo, 0.9)
    cjc9_candidate_clusters = cjc9_candidate_clusters_and_ratio.keys()

    all_candidate_clusters = t_candidate_clusters | set(cjc6_candidate_clusters) | set(cjc7_candidate_clusters) | set(cjc8_candidate_clusters) | set(cjc9_candidate_clusters)

    for cg_cluster in all_candidate_clusters:
        authors = cg_cluster.get_authors(cg_cursor)
        dois = cg_cluster.get_dois(cg_cursor)
        citation_count = get_cg_citation_count(cg_cursor, cg_cluster.paper_id)

        tjaccard = jaccard(wos_paper, cg_cluster)

        if cg_cluster in cjc6_candidate_clusters_and_ratio:
            matched, cjc6r, cjc6nnr = cjc6_candidate_clusters_and_ratio[cg_cluster]
            cjc6jc = matched / (wos_citation_count + citation_count - matched)
        else:
            cjc6r = None
            cjc6nnr = None
            cjc6jc = None

        if cg_cluster in cjc7_candidate_clusters_and_ratio:
            matched, cjc7r, cjc7nnr = cjc7_candidate_clusters_and_ratio[cg_cluster]
            cjc7jc = matched / (wos_citation_count + citation_count - matched)
        else:
            cjc7r = None
            cjc7nnr = None
            cjc7jc = None

        if cg_cluster in cjc8_candidate_clusters_and_ratio:
            matched, cjc8r, cjc8nnr = cjc8_candidate_clusters_and_ratio[cg_cluster]
            cjc8jc = matched / (wos_citation_count + citation_count - matched)
        else:
            cjc8r = None
            cjc8nnr = None
            cjc8jc = None

        if cg_cluster in cjc9_candidate_clusters_and_ratio:
            matched, cjc9r, cjc9nnr = cjc9_candidate_clusters_and_ratio[cg_cluster]
            cjc9jc = matched / (wos_citation_count + citation_count - matched)
        else:
            cjc9r = None
            cjc9nnr = None
            cjc9jc = None

        csvwriter.writerow([None, tjaccard, cjc6nnr, cjc7nnr, cjc8nnr, cjc9nnr, cjc6r, cjc7r, cjc8r, cjc9r, cjc6jc, cjc7jc, cjc8jc, cjc9jc, cg_cluster.paper_id, citation_count, None, cg_cluster.title, cg_cluster.year] + authors + dois)

    print('#####')


def process(csvwriter, wos_paperids):
    csvwriter.writerow(['Truth', 'tjc', 'cjc0.6nnr', 'cjc0.7nnr', 'cjc0.8nnr', 'cjc0.9nnr', 'cjc0.6r', 'cjc0.7r', 'cjc0.8r', 'cjc0.9r', 'cjc0.6jc', 'cjc0.7jc', 'cjc0.8jc', 'cjc0.9jc', 'ID', '#Citation', '#NotNull', 'Title', 'Year'])
    for wos_paperid in wos_paperids:
        match(csvwriter, wos_paperid)


def main(args, config):
    global wos_cursor
    global cg_cursor
    global solr_url

    solr_url = config.get('solr', 'url')

    if args.infile:
        inf = open(args.infile)
    else:
        inf = sys.stdin

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

        process(csvwriter, wos_paperids)

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

    parser = argparse.ArgumentParser(description='Match papers in Web of Science and papers in CiteSeerX that have DOIs.')
    parser.add_argument('-i', '--infile', help='input CSV file of CS papers')
    parser.add_argument('-o', '--outfile', help='output CSV file of sample results')

    args = parser.parse_args()
    main(args, config)
