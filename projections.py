## Data preparation

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict
import itertools

"""The tripartite network of 910 diseases used in the paper was provided by the authors on Github."""

# Getting the data from the Github repository provided with the paper (The Multiplex Network of Human Diseases)
data_link = "https://raw.githubusercontent.com/manlius/MultiplexDiseasome/master/Datasets/DSG_network_from_OMIM.csv"
df = pd.read_csv(data_link, delimiter=';')
df.head()

"""We start by extracting the genotype-based disease-disease associations projection (1st layer)."""

# Creating the 1st layer (genotype-based disease-disease network projection)
df_g = df.iloc[:,[0,6]]
associations = defaultdict(list)
for _, row in df_g.iterrows():
	associations[row.iloc[1]].append(row.iloc[0])

projection1 = nx.Graph()

# Add edges between all pairs of associated elements
for associated_elements in associations.values():
    for pair in itertools.combinations(associated_elements, 2):
        if projection1.has_edge(*pair):
            projection1[pair[0]][pair[1]]['weight'] += 1
        else:
            projection1.add_edge(pair[0], pair[1], weight=1)

# G is a graph where an edge exists between two elements from column 1 if they are associated with the same element in column 2
# The weight of each edge is the number of shared associations

# remove the nodes that are only connected to themselves (isolates)
projection1.remove_edges_from(nx.selfloop_edges(projection1))
projection1.remove_nodes_from(list(nx.isolates(projection1)))

print("Number of nodes: {}".format(projection1.number_of_nodes()))

# saving projection1 graph
nx.write_gml(projection1, "data/projection1.gml")

"""Next, We extract the phenotype-based disease-disease associations projection (2nd layer)."""

# Creating the 2nd layer (phenotype-based disease-disease network projection)

df_p = df.iloc[:,[0,3]]
associations = defaultdict(list)
for _, row in df_p.iterrows():
    associations[row.iloc[1]].append(row.iloc[0])

projection2 = nx.Graph()

for associated_elements in associations.values():
    for pair in itertools.combinations(associated_elements, 2):
        if projection2.has_edge(*pair):
            projection2[pair[0]][pair[1]]['weight'] += 1
        else:
            projection2.add_edge(pair[0], pair[1], weight=1)

projection2.remove_edges_from(nx.selfloop_edges(projection2))
projection2.remove_nodes_from(list(nx.isolates(projection2)))

print("Number of nodes: {}".format(projection2.number_of_nodes()))

"""We validate that the number of diseases in the final multiplex (after filtering the isolated nodes in both layers) is 779 as reported in the paper."""

# The final number of diseases in the multiplex of the 2 layers
print(f'Combined: {len(set(projection1.nodes()).union(set(projection2.nodes())))}')

# saving projection2 graph
nx.write_gml(projection2, "data/projection2.gml")