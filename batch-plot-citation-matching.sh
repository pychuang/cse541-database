#!/bin/sh

./batch-plot.py -s summary-citation-matching.csv -m jaccard -t "Citation Matching (Jaccard of citations)" -b summary_plots -p citation-matching-jaccard
./batch-plot.py -s summary-citation-matching.csv -m nnmr -t "Citation Matching (non-NULL citation matched ratio)" -b summary_plots -p citation-matching-nnmr
./batch-plot.py -s summary-citation-matching.csv -m mr -t "Citation Matching (citation matched ratio)" -b summary_plots -p citation-matching-mr
