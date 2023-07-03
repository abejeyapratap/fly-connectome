#!/bin/bash
# run graph metrics (degree, betweenness) in the background

eval "$(conda shell.bash hook)"
conda activate neuprint

nohup ./betweenCent.py > log1.out &
nohup ./smallWorldSigma.py > log2.out &