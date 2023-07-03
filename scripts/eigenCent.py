#!/usr/bin/env python3
import pickle
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from netneurotools import cluster
from netneurotools import modularity

from sknetwork.clustering import Louvain, get_modularity
from sknetwork.data import from_edge_list

import networkx as nx

# DNp01 (giant fiber) to DNp11
body_ids = ["2307027729","5813024015", "1565846637", "1405231475", "1466998977", "5813023322", "1100404581", "1226887763", "1228264951", "512851433", "5813026936", "1281324958"]
DNp_ids = [int(i) for i in body_ids]

consensusResults = np.load("consensusResults.npy", allow_pickle=True)

all_connection_df = pd.read_csv("./data/all_connection_df.csv")
dfFilt = all_connection_df[['bodyId_pre', 'bodyId_post', 'weight']] # sknetwork uses 3rd col as weight

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
metricName = "eigenCentrality"
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

        # calculate graph theory metrics
        cluster_eigenvector = nx.eigenvector_centrality_numpy(cluster_subgraph, weight='weight') # numpy version is faster for larger graphs
        graphMetric[iteration].append(cluster_eigenvector)
    print(f"Iteration {iteration} runtime: {(time.time()-iterStartTime):.2f}s")
print(f"Total runtime: {(time.time()-startTime):.2f}s")

# save graph theory results
with open(f'./data/{metricName}.pkl', 'wb') as handle:
    pickle.dump(graphMetric, handle)