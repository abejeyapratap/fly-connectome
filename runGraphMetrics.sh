#!/bin/bash
# run graph metrics (degree, betweenness) in the background

eval "$(conda shell.bash hook)"
conda activate neuprint

nohup ./scripts/betweenCent.py > ./logs/metrics/1.out &
# nohup ./scripts/smallWorldSigma.py > ./logs/metrics/2.out &
nohup ./scripts/eigenCent.py > ./logs/metrics/3.out &