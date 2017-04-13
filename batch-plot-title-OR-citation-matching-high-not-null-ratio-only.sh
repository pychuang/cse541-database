#!/bin/sh

./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.5.csv -m jaccard -t "Joint (Jaccard of citations), NNR >= 0.5" -b summary_plots -p title-OR-citation-matching-nnr-0.5-jaccard
./plot-summary-xy.py -i summary-title-OR-citation-matching-not-null-ratio-0.5.csv -m jaccard -t "Precision v.s. Recall for Joint, NNR >= 0.5" -x Recall -y Precision -c F1 -o summary_plots/title-OR-citation-matching-nnr-0.5-jaccard/title-OR-citation-matching-nnr-0.5-jaccard-xy-precision-recall.png --no-show
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.6.csv -m jaccard -t "Joint (Jaccard of citations), NNR >= 0.6" -b summary_plots -p title-OR-citation-matching-nnr-0.6-jaccard
./plot-summary-xy.py -i summary-title-OR-citation-matching-not-null-ratio-0.6.csv -m jaccard -t "Precision v.s. Recall for Joint, NNR >= 0.6" -x Recall -y Precision -c F1 -o summary_plots/title-OR-citation-matching-nnr-0.6-jaccard/title-OR-citation-matching-nnr-0.6-jaccard-xy-precision-recall.png --no-show
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.7.csv -m jaccard -t "Joint (Jaccard of citations), NNR >= 0.7" -b summary_plots -p title-OR-citation-matching-nnr-0.7-jaccard
./plot-summary-xy.py -i summary-title-OR-citation-matching-not-null-ratio-0.7.csv -m jaccard -t "Precision v.s. Recall for Joint, NNR >= 0.7" -x Recall -y Precision -c F1 -o summary_plots/title-OR-citation-matching-nnr-0.7-jaccard/title-OR-citation-matching-nnr-0.7-jaccard-xy-precision-recall.png --no-show
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.8.csv -m jaccard -t "Joint (Jaccard of citations), NNR >= 0.8" -b summary_plots -p title-OR-citation-matching-nnr-0.8-jaccard
./plot-summary-xy.py -i summary-title-OR-citation-matching-not-null-ratio-0.8.csv -m jaccard -t "Precision v.s. Recall for Joint, NNR >= 0.8" -x Recall -y Precision -c F1 -o summary_plots/title-OR-citation-matching-nnr-0.8-jaccard/title-OR-citation-matching-nnr-0.8-jaccard-xy-precision-recall.png --no-show
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.9.csv -m jaccard -t "Joint (Jaccard of citations), NNR >= 0.9" -b summary_plots -p title-OR-citation-matching-nnr-0.9-jaccard
./plot-summary-xy.py -i summary-title-OR-citation-matching-not-null-ratio-0.9.csv -m jaccard -t "Precision v.s. Recall for Joint, NNR >= 0.9" -x Recall -y Precision -c F1 -o summary_plots/title-OR-citation-matching-nnr-0.9-jaccard/title-OR-citation-matching-nnr-0.9-jaccard-xy-precision-recall.png --no-show
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-1.0.csv -m jaccard -t "Joint (Jaccard of citations), NNR = 1.0" -b summary_plots -p title-OR-citation-matching-nnr-1.0-jaccard
./plot-summary-xy.py -i summary-title-OR-citation-matching-not-null-ratio-1.0.csv -m jaccard -t "Precision v.s. Recall for Joint, NNR >= 1.0" -x Recall -y Precision -c F1 -o summary_plots/title-OR-citation-matching-nnr-1.0-jaccard/title-OR-citation-matching-nnr-1.0-jaccard-xy-precision-recall.png --no-show

./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.5.csv -m nnmr -t "Joint (non-NULL citation matched ratio), NNR >= 0.5" -b summary_plots -p title-OR-citation-matching-nnr-0.5-nnmr
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.6.csv -m nnmr -t "Joint (non-NULL citation matched ratio), NNR >= 0.6" -b summary_plots -p title-OR-citation-matching-nnr-0.6-nnmr
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.7.csv -m nnmr -t "Joint (non-NULL citation matched ratio), NNR >= 0.7" -b summary_plots -p title-OR-citation-matching-nnr-0.7-nnmr
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.8.csv -m nnmr -t "Joint (non-NULL citation matched ratio), NNR >= 0.8" -b summary_plots -p title-OR-citation-matching-nnr-0.8-nnmr
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.9.csv -m nnmr -t "Joint (non-NULL citation matched ratio), NNR >= 0.9" -b summary_plots -p title-OR-citation-matching-nnr-0.9-nnmr
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-1.0.csv -m nnmr -t "Joint (non-NULL citation matched ratio), NNR = 1.0" -b summary_plots -p title-OR-citation-matching-nnr-1.0-nnmr

./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.5.csv -m mr -t "Joint (citation matched ratio), NNR >= 0.5" -b summary_plots -p title-OR-citation-matching-nnr-0.5-mr
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.6.csv -m mr -t "Joint (citation matched ratio), NNR >= 0.6" -b summary_plots -p title-OR-citation-matching-nnr-0.6-mr
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.7.csv -m mr -t "Joint (citation matched ratio), NNR >= 0.7" -b summary_plots -p title-OR-citation-matching-nnr-0.7-mr
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.8.csv -m mr -t "Joint (citation matched ratio), NNR >= 0.8" -b summary_plots -p title-OR-citation-matching-nnr-0.8-mr
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-0.9.csv -m mr -t "Joint (citation matched ratio), NNR >= 0.9" -b summary_plots -p title-OR-citation-matching-nnr-0.9-mr
./batch-plot.py -s summary-title-OR-citation-matching-not-null-ratio-1.0.csv -m mr -t "Joint (citation matched ratio), NNR = 1.0" -b summary_plots -p title-OR-citation-matching-nnr-1.0-mr
