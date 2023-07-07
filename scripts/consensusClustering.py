# Run from ./scripts directory: python3 consensusClustering.py --expIters 100
### Consensus Clusters on Louvain Algorithm
import numpy as np
import pandas as pd

from neuprint import  fetch_adjacencies, fetch_neurons
from neuprint.utils import connection_table_to_matrix, merge_neuron_properties

from netneurotools import cluster
from netneurotools import modularity

from sknetwork.clustering import Louvain, get_modularity

from sknetwork.data import from_edge_list

import argparse

# take in expIters as a required argument
argparser = argparse.ArgumentParser(description='Consensus Clustering on Louvain Algorithm')
argparser.add_argument('--expIters', type=int, default=250, help='Number of iterations for consensus clustering', required=True)

args = argparser.parse_args()


# DNp01 (giant fiber) to DNp11
body_ids = ["2307027729","5813024015", "1565846637", "1405231475", "1466998977", "5813023322", "1100404581", "1226887763", "1228264951", "512851433", "5813026936", "1281324958"]
DNp_ids = [int(i) for i in body_ids]


# read all_connection_df.csv file
all_connection_df = pd.read_csv("../data/all_connection_df.csv")


def make_matrix(conn_df, group_cols='bodyId', weight_col='weight', sort_by=None, make_square=False):
    if isinstance(group_cols, str):
        group_cols = (f"{group_cols}_pre", f"{group_cols}_post")

    assert len(group_cols) == 2, \
        "Please provide two group_cols (e.g. 'bodyId_pre', 'bodyId_post')"

    assert group_cols[0] in conn_df, \
        f"Column missing: {group_cols[0]}"

    assert group_cols[1] in conn_df, \
        f"Column missing: {group_cols[1]}"

    assert weight_col in conn_df, \
        f"Column missing: {weight_col}"

    col_pre, col_post = group_cols
    dtype = conn_df[weight_col].dtype

    agg_weights_df = conn_df.groupby([col_pre, col_post], sort=False)[weight_col].sum().reset_index()
    matrix = agg_weights_df.pivot(col_pre, col_post, weight_col)
    matrix = matrix.fillna(0).astype(dtype)

    if sort_by:
        if isinstance(sort_by, str):
            sort_by = (f"{sort_by}_pre", f"{sort_by}_post")

        assert len(sort_by) == 2, \
            "Please provide two sort_by column names (e.g. 'type_pre', 'type_post')"

        pre_order = conn_df.sort_values(sort_by[0])[col_pre].unique()
        post_order = conn_df.sort_values(sort_by[1])[col_post].unique()
        matrix = matrix.reindex(index=pre_order, columns=post_order)
    else:
        # No sort: Keep the order as close to the input order as possible.
        pre_order = conn_df[col_pre].unique()
        post_order = conn_df[col_post].unique()
        matrix = matrix.reindex(index=pre_order, columns=post_order)

    if make_square:    
        matrix ,_ = matrix.align(matrix.T)
        matrix = matrix.fillna(0.0).astype(matrix.dtypes) # not sure abt dtypes

        # matrix, _ = matrix.align(matrix.T).fillna(0.0).astype(matrix.dtype)
        matrix = matrix.rename_axis('bodyId_pre', axis=0).rename_axis('bodyId_post', axis=1)
        matrix = matrix.loc[sorted(matrix.index), sorted(matrix.columns)]

    return matrix


# convert to NxN adjacency matrix
adj_mat_df = make_matrix(all_connection_df, 'bodyId', make_square=True)
adj_mat = adj_mat_df.to_numpy()


dfFilt = all_connection_df[['bodyId_pre', 'bodyId_post', 'weight']] # sknetwork uses 3rd col as weight
graph = from_edge_list(list(dfFilt.itertuples(index=False)), weighted=True, directed=True) # without directed=True, wrong # of elements


consensusResults = [] # this list stores a tuple for each iteration: (numIter, consensusClusterAssn)
clusterAssignments = []

for _ in range(args.expIters):
    louvain = Louvain(shuffle_nodes=True)
    labels = louvain.fit_predict(graph.adjacency) # each node (neuron) is assigned a label
    clusterAssignments.append(labels)

    labels_unique, counts = np.unique(labels, return_counts=True)
    if args.expIters > 10 and args.expIters % 10 == 0:
        continue
    print(labels_unique, counts)

clusterAssignments = np.array(clusterAssignments)


# Run Consensus algorithm
# consensus = cluster.find_consensus(np.column_stack(clusterAssignments), seed=1234)
consensus = cluster.find_consensus(np.column_stack(clusterAssignments))

# find unique labels and their counts
labels_unique, counts = np.unique(consensus, return_counts=True)
print(labels_unique, counts)

consensusResults.append((args.expIters, consensus))

### save results of consensus clustering over all iterations
outPath = f'../data/consensusResults/{args.expIters}.npy'
np.save(outPath, np.array(consensusResults, dtype=object), allow_pickle=True)