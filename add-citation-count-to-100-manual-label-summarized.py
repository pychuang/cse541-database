#!/usr/bin/env python3

import argparse
import collections
import configparser
import csv
import MySQLdb
import os
import random
import sys

import dataclean.wos as wos
import dataclean.citeseerx as csx

from dataclean import utils


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def get_wos_citation_count(cursor, wos_paperid):
    cursor.execute("""
        SELECT COUNT(*)
        FROM citations
        WHERE paperid = %s;""", (wos_paperid, ))
    result = cursor.fetchone()
    return result[0]


def get_wos_not_null_citation_count(cursor, wos_paperid):
    cursor.execute("""
        SELECT COUNT(*)
        FROM citations
        WHERE paperid = %s AND citedTitle IS NOT NULL;""", (wos_paperid, ))
    result = cursor.fetchone()
    return result[0]


def main(args, config):
    global wos_cursor

    if args.infile:
        inf = open(args.infile)
    else:
        inf = sys.stdin

    if args.outfile:
        outf = open(args.outfile, 'w')
    else:
        outf = sys.stdout

    try:
        wosdb = None
        wosdb = connect_db(config, 'wos')
        wos_cursor = wosdb.cursor()

        csvreader = csv.reader(inf)
        csvwriter = csv.writer(outf)

        wos_count = 0

        fieldnames = next(csvreader)
        fnmap = {}
        for i, fn in enumerate(fieldnames):
            fnmap[fn] = i

        i_wos_citations = 1
        i_wos_not_null_citations = 2

        fieldnames.insert(i_wos_citations, '#Citation')
        fieldnames.insert(i_wos_not_null_citations, '#NotNull')

        csvwriter.writerow(fieldnames)

        for row in csvreader:
            if not row[0]:
                break

            wos_paperid = row[0]
            count = get_wos_citation_count(wos_cursor, wos_paperid)
            row.insert(i_wos_citations, count)

            count = get_wos_not_null_citation_count(wos_cursor, wos_paperid)
            row.insert(i_wos_not_null_citations, count)

            csvwriter.writerow(row)

            wos_count += 1
            print(wos_count, file=sys.stderr, end='\r')
            sys.stderr.flush()
        print(file=sys.stderr)

    finally:
        if wosdb:
            wosdb.close()


if __name__ == '__main__':
    wos_cursor = None

    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Sample matched papers in Web of Science and papers in CiteSeerX that have DOIs.')
    parser.add_argument('-i', '--infile', help='input CSV file of CS papers')
    parser.add_argument('-o', '--outfile', help='output CSV file of sample results')

    args = parser.parse_args()
    main(args, config)
