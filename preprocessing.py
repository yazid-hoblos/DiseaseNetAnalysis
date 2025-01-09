## Data preparation

import sys
import pandas as pd
import matplotlib.pyplot as plt
import prettytable
import networkx as nx
import numpy as np
from pyvis.network import Network
import matplotlib.colors
from IPython.core.display import display, HTML
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
    associations[row[1]].append(row[0])

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
