# cse541-database

## Get CS-related papers in WoS dataset

```sh
$ ./get-wos-cs-papers.py -o wos-cs-papers.pickle
```

## Check the ratio of WoS papers match titles in citegraph of CiteSeerX

```sh
$ ./sample-wos-cs-paper-in-citeseerx.py -i wos-cs-papers.pickle -r 30
```

## Check the ratio of citations of WoS papers match titles in citegraph of CiteSeerX

```sh
$ ./sample-wos-cs-paper-citation-in-citeseerx.py -i wos-cs-papers.pickle -r 30
```
