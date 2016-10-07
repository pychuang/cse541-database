#!/usr/bin/env python3

import argparse
import collections
import configparser
import csv
import MySQLdb
import sys

import dataclean.wos as wos
import dataclean.citeseerx as csx


wos_cursor = None
csx_cursor = None


def connect_db(config, target):
    host = config.get(target, 'host')
    username = config.get(target, 'username')
    password = config.get(target, 'password')
    database = config.get(target, 'database')

    return MySQLdb.connect(host=host, user=username, passwd=password, db=database)


def match(wos_paperid, n):
    wos_paper = wos.WosPaper.get_paper_by_id(wos_cursor, wos_paperid)
    wos_citations = wos.WosPaper.get_citations(wos_cursor, wos_paper)
    print("WOS: %s" % wos_paper)
    print("WOS: %d citations" % len(wos_citations))

    candidate_csx_papers_ids = collections.defaultdict(int)
    for wos_citation in wos_citations:
        #print("\tWOS citation: %s" % wos_citation)
        csx_papers_ids = csx.CsxPaper.find_papers_ids_with_citations_matched_by_title(csx_cursor, wos_citation.title)
        if not csx_papers_ids:
            continue

        #print("\t%d candidate CSX papers" % len(csx_papers_ids))
        for csx_paper_id in csx_papers_ids:
            candidate_csx_papers_ids[csx_paper_id] += 1

    print("%d candidate CSX papers" % len(candidate_csx_papers_ids))
    if not candidate_csx_papers_ids:
        return
    nth_count = sorted(set(candidate_csx_papers_ids.values()), reverse=True)[:n][-1]
    candidate_csx_papers_ids = {paper_id: count for paper_id, count in candidate_csx_papers_ids.items() if count >= nth_count}
    sorted_candidate_csx_papers_ids = sorted(candidate_csx_papers_ids.items(), key=lambda x: x[1], reverse=True)
    for paper_id, count in sorted_candidate_csx_papers_ids:
        paper = csx.CsxPaper.get_paper_by_id(csx_cursor, paper_id)
        print("%s : count=%d" % (paper, count))


def main(args, config):
    global wos_cursor
    global csx_cursor

    if args.infile:
        inf = open(args.infile, 'rb')
    else:
        inf = sys.stdin

    try:
        wosdb = None
        csxdb = None
        wosdb = connect_db(config, 'wos')
        csxdb = connect_db(config, 'csx')
        wos_cursor = wosdb.cursor()
        csx_cursor = csxdb.cursor()

        csvreader = csv.reader(inf)
        for row in csvreader:
            print()
            wos_paperid = row[0]
            match(wos_paperid, int(args.n))
    finally:
        if wosdb:
            wosdb.close()
        if csxdb:
            csxdb.close()


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')

    parser = argparse.ArgumentParser(description='Match papers of Web of Science and clusters of citegraph of CiteSeerX.')
    parser.add_argument('-i', '--infile', help='Input CSV file of paper IDs of Web of Science')
    parser.add_argument('-n', default=3, help='Top n results')

    args = parser.parse_args()
    main(args, config)
