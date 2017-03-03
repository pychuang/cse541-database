# cse541-database

## Get CS-related papers in WoS dataset

```sh
$ ./get-wos-cs-papers.py -o wos-cs-papers.csv
```

## Check the ratio of WoS papers match titles in citegraph of CiteSeerX

```sh
$ ./sample-wos-cs-paper-in-citeseerx.py -i wos-cs-papers.csv -r 30
```

## Check the ratio of citations of WoS papers match titles in citegraph of CiteSeerX

```sh
$ ./sample-wos-cs-paper-citation-in-citeseerx.py -i wos-cs-papers.csv -r 30
```

## Get citations of CS papers in WoS

```sh
$ ./get-wos-cs-papers-citations.py -o wos-cs-papers-citations.csv
```

## Check empty fields in citations of CS papers in WoS

```sh
$ ./check-wos-citations-csv.py -i wos-cs-papers-citations.csv
```

## Match WoS and CiteSeerX papers directly

```sh
$ ./match-paper-directly.py -i test.csv
```

Randomly choose 1000 lines of the CSV file as input

```sh
$ shuf -n 1000 wos-cs-papers.csv | ./match-paper-directly.py
```

## Match WoS and CiteSeerX papers using citations information

```sh
$ ./match-paper-by-citation.py -i test.csv
```

Randomly choose 1000 lines of the CSV file as input

```sh
$ shuf -n 1000 wos-cs-papers.csv | ./match-paper-by-citation.py
```

## Sample papers which are in both WoS and CiteSeerX and which titles matched

```sh
$ ./sample-matched-cs-paper-for-manual-check.py -i wos-cs-papers.csv -o result.csv
```

## Match WoS and CiteSeerX papers using imprecise citations information

```sh
$ echo WOS:000253032400003 | ./match-paper-by-citation-imprecise.py
```

## Sample papers using Cornelia's method

```sh
$ ./sample-with-cornelia-method.py -i wos-cs-papers.csv -o result.csv
```

## Extract WoS uids from result CSV file

```sh
$ grep WoS result.csv |cut -d , -f 2 > wosids.csv
```

## Filter out WoS papers without titles

```sh
$ ./filter-wos-no-title.py -i wos-cs-papers.csv -o wos-cs-papers-title-not-null.csv
```

## Sample papers using both Cornelia's method and our method

```sh
$ ./sample-and-match.py -i wos-cs-papers.csv -o result.csv
```

## Save labeled truth in simpler format

```sh
$ ./save-labeled-truth.py --posfile positive.csv --negfile negative.csv *.csv
```

## Apply truth labels to result CSV

```sh
$ ./apply-truth-labels.py -i 1000result.csv -o result.csv --posfile positive.csv --negfile negative.csv
```

## Extract WoS uids from result CSV file

```sh
$ grep "#####" 1000result-citecount.csv | cut -d , -f 4 > 1000-samples.csv
```

## Sample more

```sh
$ ./sample-more.py -i wos-cs-papers.csv -I 1000-samples.csv -o 3000-samples.csv -n 3000
```

## Calculate overlap ratio of WoS

```sh
$ ./calc-overlap.py *.csv
```

## Calculate the precision, recall and F1 for title matching

```sh
$ ./calc-precision-recall-title-matching.py exp4/results-* -o summary-title-matching.csv
```

## Calculate the precision, recall and F1 for title matching (high not NULL ratio only)

```sh
$ ./calc-precision-recall-title-matching-high-not-null-ratio-only.py exp4/results-*
```

## Calculate the precision, recall and F1 for citation matching

```sh
$ ./calc-precision-recall-citation-matching.py exp4/results-* -o summary-citation-matching.csv
```

## Calculate the precision, recall and F1 for title matching OR citation matching

```sh
$ ./calc-precision-recall-title-OR-citation-matching.py exp4/results-* -o summary-title-OR-citation-matching.csv
```

## Calculate the precision, recall and F1 for title matching OR (citation matching AND is JOURNAL)

```sh
$ ./calc-precision-recall-ORed-tjc-ANDed-journal.py exp4/results-*
```

## Calculate the distribution of venue types of matched clusters

```sh
$ ./calc-vtype.py exp4/results-*
```

## Plot plots about citations

```sh
$ ./plot-citation-stats.py exp4/results-*
```

## Save SQL query to CSV file

```sh
$ ./save-query.py -o test.csv "select * from papers limit 10;"
```

## Plot 100 manually labeled results

```sh
$ ./plot-100-manual-label-results.py -i expresults/100-title-matched-papers-summarize-results.csv
```

## Calculate statistics of DBLP

```sh
$ ./calc-dblp-stats.py -i dblp/dblp.xml
```

## Estimate the percentage of papers in DBLP being in CiteSeerX by sampling

```sh
$ ./sample-dblp-paper-in-citeseerx.py -i dblp/dblp.xml
```

## Estimate the percentage of papers in DBLP being in WoS by sampling

```sh
$ ./sample-dblp-paper-in-wos.py -i dblp/dblp.xml
```

## Plot summary

```sh
$ ./plot-summary.py -i summary-citation-matching.csv -m jaccard -t "Precision of Citation Matching" -o test.png -x Threshold -c "Citation Title Jaccard" -y Precision
```

## Output rows with best scores in summary CSV

```sh
$ ./show-best-in-summary.py -i summary-citation-matching.csv -m jaccard -t F1 -n 10 -o test.csv
```

## Summarize best recall

```sh
./summarize-best-recall.py -m jaccard -i summary-citation-matching.csv -o best-recall-citation-matching.cs
```

# DBLP dataset

```sh
$ wget http://dblp.uni-trier.de/xml/dblp.xml.gz
$ wget http://dblp.uni-trier.de/xml/dblp.dtd
```
