#!/usr/bin/env python

import argparse
import ConfigParser
import csv
import MySQLdb


def ResultIter(cursor, size):
    while True:
        results = cursor.fetchmany(size)
        if not results:
            break
        for result in results:
            yield result


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

        cursor.execute("""
            SELECT DISTINCT uid
            FROM papers, subjects
            WHERE papers.uid = subjects.paperid AND subjects.subject LIKE 'computer%';""")

        with open(args.output, 'wb') as f:
            csvwriter = csv.writer(f)

            count = 0
            for result in ResultIter(cursor, 1000):
                count += 1
                csvwriter.writerow(result)
                if count % 100 == 0:
                    print "\r%d rows written" % count,
            print "\r",
            print "totally %d rows written" % count
    finally:
        if db:
            db.close()


if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Get CS papers in Web of Science.')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file')

    args = parser.parse_args()
    main(args, config)
