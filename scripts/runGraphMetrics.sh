#!/bin/bash
### run graph metrics (degree, betweenness) in the background

eval "$(conda shell.bash hook)"
conda activate neuprint

nohup ./consensusMetrics.py -m "betweenCentrality" > ./logs/metrics/1.out &
nohup ./consensusMetrics.py -m "eigenCentrality" > ./logs/metrics/2.out &
# nohup ./consensusMetrics.py -m "smallWorldSigma" > ./logs/metrics/3.out &
nohup ./consensusMetrics.py -m "degreeCentrality" > ./logs/metrics/4.out &
