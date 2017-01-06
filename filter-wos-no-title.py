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

        for row in csvreader:
            wos_paperid = row[0]
            wos_paper = wos.WosPaper.get_paper_by_id(wos_cursor, wos_paperid)

            # ignore papers without title
            if not wos_paper.title:
                print()
                print(wos_paper)
                continue

            wos_count += 1
            print(wos_count, file=sys.stderr, end='\r')
            sys.stderr.flush()
            csvwriter.writerow(row)
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
