#!/usr/bin/env python3

import argparse
import configparser
import csv
import MySQLdb
import sys


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
    query = args.query[0]
    try:
        db = connect_db(config, 'wos')
        cursor = db.cursor()

        print("Query: %s" % query, file=sys.stderr)
        cursor.execute(query)

        print("Writing into %s" % args.output, file=sys.stderr)
        with open(args.output, 'w') as f:
            csvwriter = csv.writer(f)

            count = 0
            for result in ResultIter(cursor, 1000):
                count += 1
                csvwriter.writerow(result)
                if count % 100 == 0:
                    print(count, file=sys.stderr, end='\r')
                    sys.stderr.flush()
            print("Totally %d rows written" % count, file=sys.stderr)
    finally:
        if db:
            db.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Save SQL query to CSV file.')
    parser.add_argument('-o', '--output', required=True, help='Output CSV file')
    parser.add_argument('query', metavar='QUERY', nargs=1, help='SQL query statement')

    args = parser.parse_args()
    main(args, config)
