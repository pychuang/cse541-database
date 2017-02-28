#!/bin/sh

mkdir -p summary_plots/title-matching
./plot-summary-xy-line.py -i summary-title-matching.csv -t "Precision of Title Matching" -x Threshold -y Precision -o summary_plots/title-matching/title-matching-precision.png --no-show
./plot-summary-xy-line.py -i summary-title-matching.csv -t "Recall of Title Matching" -x Threshold -y Recall -o summary_plots/title-matching/title-matching-recall.png --no-show
./plot-summary-xy-line.py -i summary-title-matching.csv -t "F1 of Title Matching" -x Threshold -y F1 -o summary_plots/title-matching/title-matching-f1.png --no-show
./plot-summary-xy-line.py -i summary-title-matching.csv -t "Precision v.s. Recall for Title Matching" -x Recall -y Precision -o summary_plots/title-matching/title-matching-xy-precision-recall.png --no-show

