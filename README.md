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

## Sample papers using both Cornelia's method and our method

```sh
$ ./sample-and-match.py -i wos-cs-papers.csv -o result.csv
```


## Save labeled truth in simpler format

```sh
$ ./save-labeled-truth.py -i result.csv --posfile positive.csv --negfile negative.csv
```
