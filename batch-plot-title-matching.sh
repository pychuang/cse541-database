#!/bin/sh

mkdir -p summary_plots/title-matching
./plot-summary-xy-line.py -i summary-title-matching.csv -t "Match-By-Title" -x Threshold -y Precision -o summary_plots/title-matching/title-matching-precision.png --no-show
./plot-summary-xy-line.py -i summary-title-matching.csv -t "Match-By-Title" -x Threshold -y Recall -o summary_plots/title-matching/title-matching-recall.png --no-show
./plot-summary-xy-line.py -i summary-title-matching.csv -t "Match-By-Title" -x Threshold -y F1 -o summary_plots/title-matching/title-matching-f1.png --no-show
#./plot-summary-xy-line.py -i summary-title-matching.csv -t "Match-By-Title" -x Recall -y Precision -o summary_plots/title-matching/title-matching-xy-precision-recall.png --no-show
./plot-summary-xy.py -i summary-title-matching.csv -t "Match-By-Title" -x Recall -y Precision -c F1 -o summary_plots/title-matching/title-matching-xy-precision-recall.png --no-show
