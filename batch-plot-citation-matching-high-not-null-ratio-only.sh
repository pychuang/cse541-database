#!/bin/sh

./batch-plot.py -s summary-citation-matching-not-null-ratio-0.5.csv -m jaccard -t "Citation Matching (Jaccard of citations), NNR >= 0.5" -b summary_plots -p citation-matching-nnr-0.5-jaccard
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.6.csv -m jaccard -t "Citation Matching (Jaccard of citations), NNR >= 0.6" -b summary_plots -p citation-matching-nnr-0.6-jaccard
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.7.csv -m jaccard -t "Citation Matching (Jaccard of citations), NNR >= 0.7" -b summary_plots -p citation-matching-nnr-0.7-jaccard
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.8.csv -m jaccard -t "Citation Matching (Jaccard of citations), NNR >= 0.8" -b summary_plots -p citation-matching-nnr-0.8-jaccard
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.9.csv -m jaccard -t "Citation Matching (Jaccard of citations), NNR >= 0.9" -b summary_plots -p citation-matching-nnr-0.9-jaccard
./batch-plot.py -s summary-citation-matching-not-null-ratio-1.0.csv -m jaccard -t "Citation Matching (Jaccard of citations), NNR = 1.0" -b summary_plots -p citation-matching-nnr-1.0-jaccard

./batch-plot.py -s summary-citation-matching-not-null-ratio-0.5.csv -m nnmr -t "Citation Matching (non-NULL citation matched ratio), NNR >= 0.5" -b summary_plots -p citation-matching-nnr-0.5-nnmr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.6.csv -m nnmr -t "Citation Matching (non-NULL citation matched ratio), NNR >= 0.6" -b summary_plots -p citation-matching-nnr-0.6-nnmr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.7.csv -m nnmr -t "Citation Matching (non-NULL citation matched ratio), NNR >= 0.7" -b summary_plots -p citation-matching-nnr-0.7-nnmr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.8.csv -m nnmr -t "Citation Matching (non-NULL citation matched ratio), NNR >= 0.8" -b summary_plots -p citation-matching-nnr-0.8-nnmr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.9.csv -m nnmr -t "Citation Matching (non-NULL citation matched ratio), NNR >= 0.9" -b summary_plots -p citation-matching-nnr-0.9-nnmr
./batch-plot.py -s summary-citation-matching-not-null-ratio-1.0.csv -m nnmr -t "Citation Matching (non-NULL citation matched ratio), NNR = 1.0" -b summary_plots -p citation-matching-nnr-1.0-nnmr

./batch-plot.py -s summary-citation-matching-not-null-ratio-0.5.csv -m mr -t "Citation Matching (citation matched ratio), NNR >= 0.5" -b summary_plots -p citation-matching-nnr-0.5-mr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.6.csv -m mr -t "Citation Matching (citation matched ratio), NNR >= 0.6" -b summary_plots -p citation-matching-nnr-0.6-mr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.7.csv -m mr -t "Citation Matching (citation matched ratio), NNR >= 0.7" -b summary_plots -p citation-matching-nnr-0.7-mr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.8.csv -m mr -t "Citation Matching (citation matched ratio), NNR >= 0.8" -b summary_plots -p citation-matching-nnr-0.8-mr
./batch-plot.py -s summary-citation-matching-not-null-ratio-0.9.csv -m mr -t "Citation Matching (citation matched ratio), NNR >= 0.9" -b summary_plots -p citation-matching-nnr-0.9-mr
./batch-plot.py -s summary-citation-matching-not-null-ratio-1.0.csv -m mr -t "Citation Matching (citation matched ratio), NNR = 1.0" -b summary_plots -p citation-matching-nnr-1.0-mr
