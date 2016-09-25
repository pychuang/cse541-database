#!/usr/bin/env python

import argparse
import ConfigParser
import MySQLdb
import pickle


def wos_cs_papers(cursor):
    cursor.execute("""
        SELECT DISTINCT uid
        FROM papers, subjects
        WHERE papers.uid = subjects.paperid AND subjects.subject LIKE 'computer%';""")

    result = cursor.fetchall()
    return [d[0] for d in result]


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def main(args, config):
    try:
        db = connect_db(config, 'wos')
        cursor = db.cursor()
        cs_papers = wos_cs_papers(cursor)
        print "Retrieved %d CS papers from Web of Science database" % len(cs_papers)

        with open(args.output, 'wb') as f:
            pickle.dump(cs_papers, f)
    finally:
        if db:
            db.close()


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Get CS papers in Web of Science.')
    parser.add_argument('-o', '--output', required=True, help='Output pickle file')

    args = parser.parse_args()
    main(args, config)
