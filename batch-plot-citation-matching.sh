#!/bin/sh

./batch-plot.py -s summary-citation-matching.csv -m jaccard -t "Citation Matching (Jaccard of citations)" -b summary_plots -p citation-matching-jaccard
./plot-summary-xy.py -i summary-citation-matching.csv -m jaccard -t "Precision v.s. Recall for Citation Matching (Jaccard of citations)" -x Recall -y Precision -c F1 -o summary_plots/citation-matching-jaccard/citation-matching-jaccard-xy-precision-recall.png --no-show

./batch-plot.py -s summary-citation-matching.csv -m nnmr -t "Citation Matching (non-NULL citation matched ratio)" -b summary_plots -p citation-matching-nnmr
./plot-summary-xy.py -i summary-citation-matching.csv -m "non-NULL matched ratio"  -t "Precision v.s. Recall for Citation Matching (non-NULL citation matched ratio)" -x Recall -y Precision -c F1 -o summary_plots/citation-matching-nnmr/citation-matching-nnmr-xy-precision-recall.png --no-show

./batch-plot.py -s summary-citation-matching.csv -m mr -t "Citation Matching (citation matched ratio)" -b summary_plots -p citation-matching-mr
./plot-summary-xy.py -i summary-citation-matching.csv -m "matched ratio"  -t "Precision v.s. Recall for Citation Matching (citation matched ratio)" -x Recall -y Precision -c F1 -o summary_plots/citation-matching-mr/citation-matching-mr-xy-precision-recall.png --no-show