#!/bin/bash
# run consensus clustering for different number of iterations

eval "$(conda shell.bash hook)"
conda activate neuprint

# list of expIters
expIters=( 5 10 15 )

# loop over expIters
for i in "${expIters[@]}"
do
    nohup ./scripts/consensusClustering.py --expIters $i > ./logs/consensus/log$i.out &
done