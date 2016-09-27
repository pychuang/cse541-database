# cse541-database

## Get CS-related papers in WoS dataset

```sh
$ ./get-wos-cs-papers.py -o wos-cs-papers.csv
```

## Check the ratio of WoS papers match titles in citegraph of CiteSeerX

```sh
$ ./sample-wos-cs-paper-in-citeseerx.py -i wos-cs-papers.pickle -r 30
```

## Check the ratio of citations of WoS papers match titles in citegraph of CiteSeerX

```sh
$ ./sample-wos-cs-paper-citation-in-citeseerx.py -i wos-cs-papers.pickle -r 30
```

## Get citations of CS papers in WoS
```sh
$ ./get-wos-cs-papers-citations.py -o wos-cs-papers-citations.csv
```
