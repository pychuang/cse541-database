#!/usr/bin/env python

import argparse
import ConfigParser
import csv
import MySQLdb
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


def get_ratios_of_matches_in_citegraph(papers):
    print "check whether citations of papers match in citegraph"
    num_citations = 0
    num_matched_citations = 0
    try:
        db = connect_db(config, 'citegraph')
        cursor = db.cursor()
        for paperid, title, citations in papers:
            if not citations:
                continue

            num_citations += len(citations)
            for t in citations:
                c, _ = match_title_in_citegraph(cursor, t)
                if c is None:
                    continue
                num_matched_citations += 1
    finally:
        if db:
            db.close()

    matched_citations_ratio = 0
    if num_citations:
        matched_citations_ratio = float(num_matched_citations) / num_citations
        print "In those WoS papers, the number of all citations is %d. %d of them are matched in CiteSeerX (%f)" % (num_citations, num_matched_citations, matched_citations_ratio)

    return matched_citations_ratio


def sampling(paperids, nsamples):
    print "randomly select %d from %d papers" % (nsamples, len(paperids))
    paperids_sample = random.sample(paperids, nsamples)
    papers = get_wos_papers(paperids_sample)
    return get_ratios_of_matches_in_citegraph(papers)


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

    nsamples = int(args.nsamples)
    runs = int(args.runs)
    avg_matched_citations_ratio = 0
    for i in xrange(runs):
        matched_citations_ratio = sampling(paperids, nsamples)
        avg_matched_citations_ratio += matched_citations_ratio

    avg_matched_citations_ratio /= runs
    print "In average, %f of citations of sampled WoS papers match titles of clusters in citegraph database in CiteSeerX" % avg_matched_citations_ratio


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Calculate the percentage of citations of CS papers in Web of Science being in CiteSeerX.')
    parser.add_argument('-i', '--infile', help='input CSV file of CS papers')
    parser.add_argument('-n', '--nsamples', default=1000, help='number of samples')
    parser.add_argument('-r', '--runs', default=1, help='number of sampling iterations')

    args = parser.parse_args()
    main(args, config)
