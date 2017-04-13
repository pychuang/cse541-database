#!/bin/sh

mkdir -p summary_plots/title-matching
./plot-summary-xy-line.py -i summary-title-matching.csv -t "Precision of Match-By-Title" -x Threshold -y Precision -o summary_plots/title-matching/title-matching-precision.png --no-show
./plot-summary-xy-line.py -i summary-title-matching.csv -t "Recall of Match-By-Title" -x Threshold -y Recall -o summary_plots/title-matching/title-matching-recall.png --no-show
./plot-summary-xy-line.py -i summary-title-matching.csv -t "F1 of Match-By-Title" -x Threshold -y F1 -o summary_plots/title-matching/title-matching-f1.png --no-show
./plot-summary-xy-line.py -i summary-title-matching.csv -t "Precision v.s. Recall for Match-By-Title" -x Recall -y Precision -o summary_plots/title-matching/title-matching-xy-precision-recall.png --no-show

