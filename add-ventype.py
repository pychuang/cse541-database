#!/usr/bin/env python3

import argparse
import configparser
import csv
import MySQLdb
import os

import dataclean.wos as wos
import dataclean.citeseerx as csx

from dataclean import utils


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def process_file(fpath, out_dir):
    print("reading %s" % fpath)
    inf = open(fpath)
    outpath = os.path.join(out_dir, os.path.basename(fpath))
    print("writing %s" % outpath)
    outf = open(outpath, 'w')

    csvreader = csv.reader(inf)
    fieldnames = next(csvreader)
    fnmap = {}
    for i, fn in enumerate(fieldnames):
        fnmap[fn] = i

    ivtype = fnmap['Year'] + 1
    fieldnames.insert(ivtype, 'VType')

    csvwriter = csv.writer(outf)
    csvwriter.writerow(fieldnames)

    for row in csvreader:
        if row[fnmap['Truth']] == '#####':
            row.insert(ivtype, None)
            csvwriter.writerow(row)
            continue

        cg_cluster_id = row[fnmap['ID']]

        row.insert(ivtype, None)
        csvwriter.writerow(row)


def main(args, config):
    global wos_cursor
    global cg_cursor

    try:
        wosdb = None
        cgdb = None
        '''
        wosdb = connect_db(config, 'wos')
        cgdb = connect_db(config, 'citegraph')
        wos_cursor = wosdb.cursor()
        cg_cursor = cgdb.cursor()
        '''

        for infile in args.infiles:
            process_file(infile, args.out_dir)

    finally:
        if wosdb:
            wosdb.close()
        if cgdb:
            cgdb.close()


if __name__ == '__main__':
    wos_cursor = None
    cg_cursor = None

    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Query cventype of Citegraph clusters and add them to the result CSV files.')
    parser.add_argument('-o', '--out-dir', required=True, help='output directory')
    parser.add_argument('infiles', nargs='+', metavar='INFILE', help='input CSV file of result')

    args = parser.parse_args()
    main(args, config)
