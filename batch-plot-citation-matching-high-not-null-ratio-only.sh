#!/bin/sh

./batch-plot.py -s summary-citation-matching-not-null-ratio-0.5.csv -m jaccard -t "Match-By-References (Jaccard of citations), NNR >= 0.5" -b summary_plots -p citation-matching-nnr-0.5-jaccard
./plot-summary-xy.py -i summary-citation-matching-not-null-ratio-0.5.csv -m jaccard -t "Match-By-References (M: Jaccard of citations), NNR >= 0.5" -x Recall -y Precision -c F1 -o summary_plots/citation-matching-nnr-0.5-jaccard/citation-matching-nnr-0.5-jaccard-xy-precision-recall.png --no-show
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.6.csv -m jaccard -t "Match-By-References (Jaccard of citations), NNR >= 0.6" -b summary_plots -p citation-matching-nnr-0.6-jaccard
./plot-summary-xy.py -i summary-citation-matching-not-null-ratio-0.6.csv -m jaccard -t "Match-By-References (M: Jaccard of citations), NNR >= 0.6" -x Recall -y Precision -c F1 -o summary_plots/citation-matching-nnr-0.6-jaccard/citation-matching-nnr-0.6-jaccard-xy-precision-recall.png --no-show
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.7.csv -m jaccard -t "Match-By-References (Jaccard of citations), NNR >= 0.7" -b summary_plots -p citation-matching-nnr-0.7-jaccard
./plot-summary-xy.py -i summary-citation-matching-not-null-ratio-0.7.csv -m jaccard -t "Match-By-References (M: Jaccard of citations), NNR >= 0.7" -x Recall -y Precision -c F1 -o summary_plots/citation-matching-nnr-0.7-jaccard/citation-matching-nnr-0.7-jaccard-xy-precision-recall.png --no-show
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.8.csv -m jaccard -t "Match-By-References (Jaccard of citations), NNR >= 0.8" -b summary_plots -p citation-matching-nnr-0.8-jaccard
./plot-summary-xy.py -i summary-citation-matching-not-null-ratio-0.8.csv -m jaccard -t "Match-By-References (M: Jaccard of citations), NNR >= 0.8" -x Recall -y Precision -c F1 -o summary_plots/citation-matching-nnr-0.8-jaccard/citation-matching-nnr-0.8-jaccard-xy-precision-recall.png --no-show
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.9.csv -m jaccard -t "Match-By-References (Jaccard of citations), NNR >= 0.9" -b summary_plots -p citation-matching-nnr-0.9-jaccard
./plot-summary-xy.py -i summary-citation-matching-not-null-ratio-0.9.csv -m jaccard -t "Match-By-References (M: Jaccard of citations), NNR >= 0.9" -x Recall -y Precision -c F1 -o summary_plots/citation-matching-nnr-0.9-jaccard/citation-matching-nnr-0.9-jaccard-xy-precision-recall.png --no-show
./batch-plot.py -s summary-citation-matching-not-null-ratio-1.0.csv -m jaccard -t "Match-By-References (Jaccard of citations), NNR = 1.0" -b summary_plots -p citation-matching-nnr-1.0-jaccard
./plot-summary-xy.py -i summary-citation-matching-not-null-ratio-1.0.csv -m jaccard -t "Match-By-References (M: Jaccard of citations), NNR >= 1.0" -x Recall -y Precision -c F1 -o summary_plots/citation-matching-nnr-1.0-jaccard/citation-matching-nnr-1.0-jaccard-xy-precision-recall.png --no-show

./batch-plot.py -s summary-citation-matching-not-null-ratio-0.5.csv -m nnmr -t "Match-By-References (non-NULL citation matched ratio), NNR >= 0.5" -b summary_plots -p citation-matching-nnr-0.5-nnmr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.6.csv -m nnmr -t "Match-By-References (non-NULL citation matched ratio), NNR >= 0.6" -b summary_plots -p citation-matching-nnr-0.6-nnmr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.7.csv -m nnmr -t "Match-By-References (non-NULL citation matched ratio), NNR >= 0.7" -b summary_plots -p citation-matching-nnr-0.7-nnmr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.8.csv -m nnmr -t "Match-By-References (non-NULL citation matched ratio), NNR >= 0.8" -b summary_plots -p citation-matching-nnr-0.8-nnmr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.9.csv -m nnmr -t "Match-By-References (non-NULL citation matched ratio), NNR >= 0.9" -b summary_plots -p citation-matching-nnr-0.9-nnmr
./batch-plot.py -s summary-citation-matching-not-null-ratio-1.0.csv -m nnmr -t "Match-By-References (non-NULL citation matched ratio), NNR = 1.0" -b summary_plots -p citation-matching-nnr-1.0-nnmr

./batch-plot.py -s summary-citation-matching-not-null-ratio-0.5.csv -m mr -t "Match-By-References (citation matched ratio), NNR >= 0.5" -b summary_plots -p citation-matching-nnr-0.5-mr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.6.csv -m mr -t "Match-By-References (citation matched ratio), NNR >= 0.6" -b summary_plots -p citation-matching-nnr-0.6-mr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.7.csv -m mr -t "Match-By-References (citation matched ratio), NNR >= 0.7" -b summary_plots -p citation-matching-nnr-0.7-mr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.8.csv -m mr -t "Match-By-References (citation matched ratio), NNR >= 0.8" -b summary_plots -p citation-matching-nnr-0.8-mr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.9.csv -m mr -t "Match-By-References (citation matched ratio), NNR >= 0.9" -b summary_plots -p citation-matching-nnr-0.9-mr
./batch-plot.py -s summary-citation-matching-not-null-ratio-1.0.csv -m mr -t "Match-By-References (citation matched ratio), NNR = 1.0" -b summary_plots -p citation-matching-nnr-1.0-mr
