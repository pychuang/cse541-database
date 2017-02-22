#!/usr/bin/env python3

import argparse
import configparser
import csv
import MySQLdb
import os
import pickle
import random
import sys

from lxml import etree

def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database, charset='utf8')


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


def get_ratios_of_matches_in_citegraph(cursor, dblp_titles):
    print("check whether papers match in citegraph")
    num_matched_clusters = 0
    for dblp_title in dblp_titles:
        print("DBLP:", dblp_title)
        csx_clusterid, csx_title = match_title_with_dois_in_citegraph(cursor, dblp_title)
        if csx_clusterid is None:
            continue
        num_matched_clusters += 1

    ratio = num_matched_clusters / len(dblp_titles)
    print("%d out of %d sampled DBLP papers match titles of clusters in citegraph database in CiteSeerX (%f)" % (num_matched_clusters, len(dblp_titles), ratio))
    return ratio

def sampling(cursor, dblp_titles, nsamples):
    print("randomly select %d from %d papers" % (nsamples, len(dblp_titles)))
    sampled_dblp_titles = random.sample(dblp_titles, nsamples)
    return get_ratios_of_matches_in_citegraph(cursor, sampled_dblp_titles)


def load_dblp_titles(fname):
    with open(fname) as f:
        print("loading %s ..." % args.infile)
        parser = etree.XMLParser(load_dtd=True)
        tree = etree.parse(f, parser)

    root = tree.getroot()

    titles = []
    for child in root:
        title = child.findtext('title')
        titles.append(title)

    return titles


def main(args, config):
    try:
        db = connect_db(config, 'citegraph')
        cursor = db.cursor()

        dblp_titles = load_dblp_titles(args.infile)

        runs = args.runs
        nsamples = args.nsamples
        ratio = 0
        for i in range(runs):
            ratio += sampling(cursor, dblp_titles, nsamples)
        ratio /= runs
        print("in average, %f of sampled DBLP papers match titles of clusters in citegraph database in CiteSeerX" % ratio)

    finally:
        if db:
            db.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Estimate the percentage of papers in DBLP being in CiteSeerX by sampling.')
    parser.add_argument('-i', '--infile', help='DBLP XML file')
    parser.add_argument('-n', '--nsamples', type=int, default=1000, help='number of samples')
    parser.add_argument('-r', '--runs', type=int, default=1, help='number of sampling iterations')

    args = parser.parse_args()
    main(args, config)
