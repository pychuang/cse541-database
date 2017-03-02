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


def match_title_in_wos(cursor, title):
    cursor.execute("""
        SELECT uid, title
        FROM papers
        WHERE title = %s
        LIMIT 1;""", (title,))

    result = cursor.fetchone()
    if result is None:
        return (None, None)
    else:
        return result


def get_ratios_of_matches_in_wos(cursor, dblp_titles):
    print("check whether papers match in WoS")
    num_matched_papers = 0
    for dblp_title in dblp_titles:
        print("DBLP:", dblp_title)
        wos_paper_id, wos_title = match_title_in_wos(cursor, dblp_title)
        if wos_paper_id is None:
            continue
        num_matched_papers += 1

    ratio = num_matched_papers / len(dblp_titles)
    print("%d out of %d sampled DBLP papers match titles of WoS papers (%f)" % (num_matched_papers, len(dblp_titles), ratio))
    return ratio

def sampling(cursor, dblp_titles, nsamples):
    print("randomly select %d from %d papers" % (nsamples, len(dblp_titles)))
    sampled_dblp_titles = random.sample(dblp_titles, nsamples)
    return get_ratios_of_matches_in_wos(cursor, sampled_dblp_titles)


def load_dblp_titles(fname):
    titles = []
    with open(fname, 'rb') as f:
        print("loading %s ..." % fname, file=sys.stderr)
        xmldoc = etree.iterparse(f, load_dtd=True, events=('start', 'end'))
        _, root = next(xmldoc)

        count = 0
        current_tag = None
        for event, elem in xmldoc:
            if event == 'end' and elem.tag == current_tag:
                #print(elem.findtext('title'))
                titles.append(elem.findtext('title'))
                current_tag = None
                elem.clear()
            if event == 'start' and current_tag is None:
                current_tag = elem.tag
                count += 1

                print(count, file=sys.stderr, end='\r')
                sys.stderr.flush()
        print("Totally %d records" % count)
    return titles


def main(args, config):
    try:
        db = connect_db(config, 'wos')
        cursor = db.cursor()

        dblp_titles = load_dblp_titles(args.infile)

        runs = args.runs
        nsamples = args.nsamples
        ratio = 0
        for i in range(runs):
            ratio += sampling(cursor, dblp_titles, nsamples)
        ratio /= runs
        print("in average, %f of sampled DBLP papers match titles of WoS papers" % ratio)

    finally:
        if db:
            db.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Estimate the percentage of papers in DBLP being in WoS by sampling.')
    parser.add_argument('-i', '--infile', help='DBLP XML file')
    parser.add_argument('-n', '--nsamples', type=int, default=1000, help='number of samples')
    parser.add_argument('-r', '--runs', type=int, default=1, help='number of sampling iterations')

    args = parser.parse_args()
    main(args, config)
