#!/bin/sh

./batch-plot.py -s summary-title-OR-citation-matching.csv -m jaccard -t "Title OR Citation Matching (Jaccard of citations)" -b summary_plots -p title-OR-citation-matching-jaccard
./batch-plot.py -s summary-title-OR-citation-matching.csv -m nnmr -t "Title OR Citation Matching (non-NULL citation matched ratio)" -b summary_plots -p title-OR-citation-matching-nnmr
./batch-plot.py -s summary-title-OR-citation-matching.csv -m mr -t "Title OR Citation Matching (citation matched ratio)" -b summary_plots -p title-OR-citation-matching-mr
