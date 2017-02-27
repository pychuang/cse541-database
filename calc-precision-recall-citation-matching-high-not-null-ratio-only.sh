#!/bin/sh

./calc-precision-recall-citation-matching-high-not-null-ratio-only.py -n 0.5 -o summary-citation-matching-not-null-ratio-0.5.csv exp4/results-*
./calc-precision-recall-citation-matching-high-not-null-ratio-only.py -n 0.6 -o summary-citation-matching-not-null-ratio-0.6.csv exp4/results-*
./calc-precision-recall-citation-matching-high-not-null-ratio-only.py -n 0.7 -o summary-citation-matching-not-null-ratio-0.7.csv exp4/results-*
./calc-precision-recall-citation-matching-high-not-null-ratio-only.py -n 0.8 -o summary-citation-matching-not-null-ratio-0.8.csv exp4/results-*
./calc-precision-recall-citation-matching-high-not-null-ratio-only.py -n 0.9 -o summary-citation-matching-not-null-ratio-0.9.csv exp4/results-*
./calc-precision-recall-citation-matching-high-not-null-ratio-only.py -n 1.0 -o summary-citation-matching-not-null-ratio-1.0.csv exp4/results-*
