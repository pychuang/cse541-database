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
        SELECT title FROM papers
        WHERE uid = %s;""", (paperid,))

    result = cursor.fetchone()
    return result[0]


def get_wos_paper_titles(paperids):
    print "get titles from wos database"
    titles = []
    try:
        db = connect_db(config, 'wos')
        cursor = db.cursor()
        for paperid in paperids:
            title = get_wos_paper_title(cursor, paperid)
            titles.append(title)
    finally:
        if db:
            db.close()

    return titles


def title_exists_in_citegraph(cursor, title):
    cursor.execute("""
        SELECT * FROM clusters
        WHERE ctitle = %s;""", (title,))

    result = cursor.fetchone()
    return result is not None


def get_ratio_of_titles_in_citegraph(titles):
    print "check whether titles appear in citegraph"
    count = 0
    try:
        db = connect_db(config, 'citegraph')
        cursor = db.cursor()
        for title in titles:
            if title_exists_in_citegraph(cursor, title):
                count += 1
    finally:
        if db:
            db.close()

    ratio = float(count) / len(titles)
    print "%d out of %d sampled WoS papers match titles of clusters in citegraph database in CiteSeerX (%f)" % (count, len(titles), ratio)
    return ratio


def sampling(paperids, nsamples):
    print "randomly select %d from %d papers" % (nsamples, len(paperids))
    paperids_sample = random.sample(paperids, nsamples)
    titles = get_wos_paper_titles(paperids_sample)
    return get_ratio_of_titles_in_citegraph(titles)


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
