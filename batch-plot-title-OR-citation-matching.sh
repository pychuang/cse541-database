#!/bin/sh

./batch-plot.py -s summary-title-OR-citation-matching.csv -m jaccard -t "Title OR Citation Matching (Jaccard of citations)" -b summary_plots -p title-OR-citation-matching-jaccard
./plot-summary-xy.py -i summary-title-OR-citation-matching.csv -m jaccard -t "Precision v.s. Recall for Title OR Citation Matching (Jaccard of citations)" -x Recall -y Precision -c F1 -o summary_plots/title-OR-citation-matching-jaccard/title-OR-citation-matching-jaccard-xy-precision-recall.png --no-show

./batch-plot.py -s summary-title-OR-citation-matching.csv -m nnmr -t "Title OR Citation Matching (non-NULL citation matched ratio)" -b summary_plots -p title-OR-citation-matching-nnmr
./plot-summary-xy.py -i summary-title-OR-citation-matching.csv -m nnmr -t "Precision v.s. Recall for Title OR Citation Matching (Jaccard of citations)" -x Recall -y Precision -c F1 -o summary_plots/title-OR-citation-matching-nnmr/title-OR-citation-matching-nnmr-xy-precision-recall.png --no-show

./batch-plot.py -s summary-title-OR-citation-matching.csv -m mr -t "Title OR Citation Matching (citation matched ratio)" -b summary_plots -p title-OR-citation-matching-mr
./plot-summary-xy.py -i summary-title-OR-citation-matching.csv -m mr -t "Precision v.s. Recall for Title OR Citation Matching (Jaccard of citations)" -x Recall -y Precision -c F1 -o summary_plots/title-OR-citation-matching-mr/title-OR-citation-matching-mr-xy-precision-recall.png --no-show
