#!/bin/bash
# run consensus clustering for different number of iterations

eval "$(conda shell.bash hook)"
conda activate neuprint

# list of expIters
expIters=( 10 25 50 75 100 150 200 250 300 350 400 450 500 600 700 800 900 1000 1500 2000 2500 )

# loop over expIters
for i in "${expIters[@]}"
do
    nohup ./consensusClustering.py --expIters $i > ../logs/consensus/$i.out &
done