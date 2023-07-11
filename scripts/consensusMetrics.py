#!/usr/bin/env python3
import pickle
import time
from pathlib import Path
import argparse

import numpy as np
import pandas as pd

from sknetwork.data import from_edge_list
import networkx as nx

# DIR = "../data/consensusResults2"
DIR = Path.cwd().parent / "data" / "consensusResults2"

# take metricName as a required argument
argparser = argparse.ArgumentParser(description="Graph Theory Metrics")
argparser.add_argument("--metricName", "-m", type=str, help="Graph theory metric calculated on consensus clustering", required=True, choices=["betweenCentrality", "degreeCentrality", "eigenCentrality", "smallWorldSigma"])

args = argparser.parse_args()

# DNp01 (giant fiber) to DNp11
body_ids = ["2307027729","5813024015", "1565846637", "1405231475", "1466998977", "5813023322", "1100404581", "1226887763", "1228264951", "512851433", "5813026936", "1281324958"]
DNp_ids = [int(i) for i in body_ids]

consensusResults = np.load(DIR / "consensusResults.npy", allow_pickle=True)

all_connection_df = pd.read_csv(Path.cwd().parent / "data" / "all_connection_df.csv")
dfFilt = all_connection_df[["bodyId_pre", "bodyId_post", "weight"]] # sknetwork uses 3rd col as weight

# sknetwork: only needed bc Louvain's clustering assignment output is based on graph.names order
graph = from_edge_list(list(dfFilt.itertuples(index=False)), weighted=True, directed=True) # without directed=True, wrong # of elements

# create directed, weighted networkx graph from dataframe of edges & weights
G = nx.from_pandas_edgelist(all_connection_df, 'bodyId_pre', 'bodyId_post', 'weight', create_using=nx.DiGraph())

""" 
for each consensus result, for each cluster, extract its subgraph
calculate graph theory metrics (degree centrality, betweenness centrality, small worldness) for each subgraph
maybe calculate modularity (reflects degree of community structure) and assortativity (reflects tendency of nodes to connect to similar nodes)

data structure to store results: dictionary of list containing a dictionary of networkx's values
{consensusIterationNum: [{cluster1's metric}, {cluster2's metric}] } 
"""
startTime = time.time()
metricName = args.metricName
graphMetric = {}

print(f"Calculating graph theory metrics: {metricName}\n")
for result in consensusResults:
    iteration, consensus = result
    graphMetric[iteration] = []
    
    iterStartTime = time.time()
    for clusterId in range(1, consensus.max()+1): # cluster indices are beween 1-n (inclusive)
        cluster_indices = np.where(consensus == clusterId)[0]
        cluster_nodes = [graph.names[i] for i in cluster_indices] # bodyIds
        cluster_subgraph = G.subgraph(cluster_nodes)
        # print(cluster_subgraph.number_of_nodes(), cluster_subgraph.number_of_edges())

        ### calculate graph theory metrics ###
        if metricName == "degreeCentrality":
            cluster_degreeCentrality = nx.degree_centrality(cluster_subgraph)
            graphMetric[iteration].append(cluster_degreeCentrality)
        elif metricName == "betweenCentrality":
            cluster_betweenness = nx.betweenness_centrality(cluster_subgraph, weight='weight') # maybe set endpoints=True
            graphMetric[iteration].append(cluster_betweenness)
        elif metricName == "eigenCentrality":
            cluster_eigenvector = nx.eigenvector_centrality_numpy(cluster_subgraph, weight='weight') # numpy version is faster for larger graphs
            graphMetric[iteration].append(cluster_eigenvector)
        # elif metricName == "smallWorldSigma":
        #     smallWorld = nx.algorithms.smallworld.sigma(cluster_subgraph.to_undirected())
        #     graphMetric[iteration].append(smallWorld)

    print(f"Iteration {iteration} runtime: {(time.time()-iterStartTime):.2f}s")
print(f"Total runtime: {(time.time()-startTime):.2f}s")

# save graph theory results
with open(DIR / f"{metricName}.pkl", "wb") as handle:
    pickle.dump(graphMetric, handle)