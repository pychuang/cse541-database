#!/usr/bin/env python

import argparse
import ConfigParser
import MySQLdb
import pickle
import random


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def get_wos_paper_title(cursor, paperid):
    cursor.execute("""
        SELECT title
        FROM papers
        WHERE uid = %s;""", (paperid,))

    result = cursor.fetchone()
    return result[0]


def get_wos_paper_citations(cursor, paperid):
    cursor.execute("""
        SELECT citedTitle
        FROM citations
        WHERE paperid = %s;""", (paperid,))

    result = cursor.fetchall()
    return [d[0] for d in result if d[0] is not None]


def get_wos_papers(paperids):
    print "get paper metadata from WoS database"
    papers = []
    try:
        db = connect_db(config, 'wos')
        cursor = db.cursor()
        for paperid in paperids:
            title = get_wos_paper_title(cursor, paperid)
            citations = get_wos_paper_citations(cursor, paperid)

            papers.append((title, citations))
    finally:
        if db:
            db.close()

    return papers


def match_title_in_citegraph(cursor, title):
    cursor.execute("""
        SELECT id, ctitle
        FROM clusters
        WHERE ctitle = %s;""", (title,))

    result = cursor.fetchone()
    if result is None:
        return (None, None)
    else:
        return result


def match_citations_in_citegraph(cursor, clusterid):
    cursor.execute("""
        SELECT clusters.ctitle
        FROM citegraph, clusters
        WHERE citegraph.citing = %s AND clusters.id = citegraph.cited;""", (clusterid,))

    result = cursor.fetchall()
    return [d[0] for d in result]


def normalize_title(title):
    return title.lower()

# return matched titles in titles1
def match_titles(titles1, titles2):
    normalized_titles2 = [normalize_title(t) for t in titles2]
    return [t for t in titles1 if normalize_title(t) in normalized_titles2]


def get_ratios_of_matches_in_citegraph(papers):
    print "check whether papers match in citegraph"
    num_matched_clusters = 0
    matched_citations_ratios = []
    try:
        db = connect_db(config, 'citegraph')
        cursor = db.cursor()
        for title, citations in papers:
            #print "TITLE: %s\t%s" % (title, citations)
            csx_clusterid, csx_title = match_title_in_citegraph(cursor, title)
            if csx_clusterid is None:
                continue
            num_matched_clusters += 1
            #print "CSX CLUSTER %d\tTITLE: %s" % (csx_clusterid, csx_title)

            if not citations:
                continue
            csx_citations = match_citations_in_citegraph(cursor, csx_clusterid)
            if not csx_citations:
                continue
            print "TITLE: %s\n%s" % (title, citations)
            print
            print "CSX CLUSTER %d\nTITLE: %s\nCITATIONS: %s" % (csx_clusterid, csx_title, csx_citations)
            matched_citations = match_titles(csx_citations, citations)
            matched_citations_ratio = float(len(matched_citations)) / len(citations)
            print 'matched_citations_ratio', matched_citations_ratio
            matched_citations_ratios.append(matched_citations_ratio)
            print '---'
    finally:
        if db:
            db.close()

    ratio = float(num_matched_clusters) / len(papers)
    print "%d out of %d sampled WoS papers match titles of clusters in citegraph database in CiteSeerX (%f)" % (num_matched_clusters, len(papers), ratio)

    avg_matched_citations_ratio = sum(matched_citations_ratios) / len(matched_citations_ratios)
    print "average citations matching ratio: %f" % avg_matched_citations_ratio
    return ratio


def sampling(paperids, nsamples):
    print "randomly select %d from %d papers" % (nsamples, len(paperids))
    paperids_sample = random.sample(paperids, nsamples)
    papers = get_wos_papers(paperids_sample)
    return get_ratios_of_matches_in_citegraph(papers)


def main(args, config):
    print "loading %s ..." % args.input
    with open(args.input, 'rb') as f:
        cs_papers = pickle.load(f)

    nsamples = int(args.nsamples)
    runs = int(args.runs)
    ratio = 0
    for i in xrange(runs):
        ratio += sampling(cs_papers, nsamples)
    ratio /= runs
    print "in average, %f of sampled WoS papers match titles of clusters in citegraph database in CiteSeerX" % ratio

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Calculate the percentage of CS papers in Web of Science being in CiteSeerX.')
    parser.add_argument('-i', '--input', required=True, help='input pickle file of CS papers')
    parser.add_argument('-n', '--nsamples', default=1000, help='number of samples')
    parser.add_argument('-r', '--runs', default=1, help='number of sampling iterations')

    args = parser.parse_args()
    main(args, config)
