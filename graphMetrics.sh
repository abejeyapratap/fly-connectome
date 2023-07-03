#!/bin/bash
# run graph metrics (degree, betweenness) in the background

eval "$(conda shell.bash hook)"
conda activate neuprint

nohup ./scripts/betweenCent.py > ./logs/log1.out &
nohup ./scripts/smallWorldSigma.py > ./logs/log2.out &