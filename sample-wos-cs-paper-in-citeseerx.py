#!/usr/bin/env python

import argparse
import ConfigParser
import MySQLdb
import pickle
import random


def get_wos_paper_title(cursor, paperid):
    cursor.execute("""
        SELECT title FROM papers
        WHERE uid = %s;""", (paperid,))

    result = cursor.fetchone()
    return result[0]


def title_exists_in_citegraph(cursor, title):
    cursor.execute("""
        SELECT * FROM clusters
        WHERE ctitle = %s;""", (title,))

    result = cursor.fetchone()
    return result is not None


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def main(args, config):
    print "loading %s ..." % args.input
    with open(args.input, 'rb') as f:
        cs_papers = pickle.load(f)

    nsamples = int(args.nsamples)
    print "randomly select %d from %d papers" % (nsamples, len(cs_papers))
    cs_papers_sample = random.sample(cs_papers, nsamples)

    print "get titles from wos database"
    titles = []
    try:
        db = connect_db(config, 'wos')
        cursor = db.cursor()
        for paperid in cs_papers_sample:
            title = get_wos_paper_title(cursor, paperid)
            titles.append(title)
    finally:
        if db:
            db.close()

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

    print "%d out of %d WoS papers exist in CiteSeerX (%f)" % (count, len(titles), float(count) / len(titles))

if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Calculate the percentage of CS papers in Web of Science being in CiteSeerX.')
    parser.add_argument('-i', '--input', required=True, help='input pickle file of CS papers')
    parser.add_argument('-n', '--nsamples', default=1000, help='number of samples')

    args = parser.parse_args()
    main(args, config)
