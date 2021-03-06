#!/usr/bin/env python

import argparse
import ConfigParser
import csv
import MySQLdb
import os
import pickle
import random
import sys


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

            papers.append((paperid, title, citations))
    finally:
        if db:
            db.close()

    return papers


def match_title_with_dois_in_citegraph(cursor, title):
    cursor.execute("""
        SELECT clusters.id, ctitle
        FROM clusters, papers
        WHERE ctitle = %s AND papers.cluster = clusters.id
        LIMIT 1;""", (title,))

    result = cursor.fetchone()
    if result is None:
        return (None, None)
    else:
        return result


def get_paper_dois_in_citegraph(cursor, clusterid):
    cursor.execute("""
        SELECT id
        FROM papers
        WHERE cluster= %s;""", (clusterid,))

    result = cursor.fetchall()
    return [d[0] for d in result]


def get_citations_in_citegraph(cursor, clusterid):
    cursor.execute("""
        SELECT clusters.id, clusters.ctitle
        FROM citegraph, clusters
        WHERE citegraph.citing = %s AND clusters.id = citegraph.cited;""", (clusterid,))

    result = cursor.fetchall()
    return [(clusterid, title) for clusterid, title in result]


def normalize_title(title):
    return title.lower()


# return matched titles in titles1
def match_titles(titles1, titles2):
    normalized_titles2 = [normalize_title(t) for t in titles2]
    return [t for t in titles1 if normalize_title(t) in normalized_titles2]


def get_ratios_of_matches_in_citegraph(csvwriter, papers):
    print "check whether papers match in citegraph"
    num_matched_clusters = 0
    matched_citations_ratios = []
    matched_citations_jaccards = []
    try:
        db = connect_db(config, 'citegraph')
        cursor = db.cursor()
        for paperid, title, citations in papers:
            csvwriter.writerow(['WoS uid', paperid])
            csvwriter.writerow(['Title', title])
            csvwriter.writerow(["%d Citations" % len(citations)])
            for citation in citations:
                csvwriter.writerow([citation])
            csvwriter.writerow([])

            #print "TITLE: %s\t%s" % (title, citations)
            csx_clusterid, csx_title = match_title_with_dois_in_citegraph(cursor, title)
            if csx_clusterid is None:
                continue
            num_matched_clusters += 1
            #print "CSX CLUSTER %d\tTITLE: %s" % (csx_clusterid, csx_title)

            dois = get_paper_dois_in_citegraph(cursor, csx_clusterid)
            csvwriter.writerow(['Cluster ID', csx_clusterid])
            csvwriter.writerow(['DOI'] + dois)
            csvwriter.writerow(['Title', csx_title])

            if not citations:
                csvwriter.writerow([])
                continue
            csx_citations = get_citations_in_citegraph(cursor, csx_clusterid)
            if not csx_citations:
                csvwriter.writerow([])
                continue

            csvwriter.writerow(["%d Citations" % len(csx_citations)])
            for citation in csx_citations:
                csvwriter.writerow(citation)

            print '---'
            print 'WoS uid', paperid
            print 'TITLE:', title
            print 'CITATIONS:', citations
            print
            print 'CSX cluster', csx_clusterid
            print 'DOIs:', dois
            print 'TITLE:', csx_title
            print 'CITATIONS:', csx_citations
            csx_titles_of_citations = [title for clusterid, title in csx_citations]
            matched_citations = match_titles(csx_titles_of_citations, citations)

            matched_citations_ratio = float(len(matched_citations)) / len(citations)
            csvwriter.writerow(['matched_citations_ratio', matched_citations_ratio])
            print 'matched_citations_ratio', matched_citations_ratio
            matched_citations_ratios.append(matched_citations_ratio)

            matched_citations_jaccard = float(len(matched_citations)) / (len(citations) + len(csx_citations) - len(matched_citations))
            csvwriter.writerow(['matched_citations_jaccard', matched_citations_jaccard])
            print 'matched_citations_jaccard', matched_citations_jaccard
            matched_citations_jaccards.append(matched_citations_jaccard)
            csvwriter.writerow([])
    finally:
        if db:
            db.close()

    ratio = float(num_matched_clusters) / len(papers)
    print "%d out of %d sampled WoS papers match titles of clusters in citegraph database in CiteSeerX (%f)" % (num_matched_clusters, len(papers), ratio)

    if matched_citations_ratios:
        avg_matched_citations_ratio = sum(matched_citations_ratios) / len(matched_citations_ratios)
        print "average citations matching ratio: %f" % avg_matched_citations_ratio
    if matched_citations_jaccards:
        avg_matched_citations_jaccard = sum(matched_citations_jaccards) / len(matched_citations_jaccards)
        print 'avg_matched_citations_jaccard', avg_matched_citations_jaccard
    return ratio


def sampling(csvwriter, paperids, nsamples):
    print "randomly select %d from %d papers" % (nsamples, len(paperids))
    paperids_sample = random.sample(paperids, nsamples)
    papers = get_wos_papers(paperids_sample)
    return get_ratios_of_matches_in_citegraph(csvwriter, papers)


def main(args, config):
    if args.infile:
        print "loading %s ..." % args.infile
        inf = open(args.infile, 'rb')
    else:
        inf = sys.stdin

    paperids = []
    csvreader = csv.reader(inf)
    for row in csvreader:
        wos_paperid = row[0]
        paperids.append(wos_paperid)

    if args.outfile:
        outf = open(args.outfile, 'wb')
    else:
        outf = open(os.devnull, 'wb')
    csvwriter = csv.writer(outf)

    nsamples = int(args.nsamples)
    runs = int(args.runs)
    ratio = 0
    for i in xrange(runs):
        ratio += sampling(csvwriter, paperids, nsamples)
    ratio /= runs
    print "in average, %f of sampled WoS papers match titles of clusters in citegraph database in CiteSeerX" % ratio


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Calculate the percentage of CS papers in Web of Science being in CiteSeerX.')
    parser.add_argument('-i', '--infile', help='input CSV file of CS papers')
    parser.add_argument('-o', '--outfile', help='output CSV file of sample results')
    parser.add_argument('-n', '--nsamples', default=1000, help='number of samples')
    parser.add_argument('-r', '--runs', default=1, help='number of sampling iterations')

    args = parser.parse_args()
    main(args, config)
