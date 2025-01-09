import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from pyvis.network import Network
import matplotlib.colors
import pickle
from utils import draw_network

"""For our analysis, we will be using the extracted genotype-based disease-disease associations projection (only the 1st layer).

## Loading the disease-disease projection in gene space data (OMIM)
"""

# data_link ="https://raw.githubusercontent.com/Murf-y/Disease-projection-in-gene-space-Data/main/DPG_OMIM.csv" (previously hosted on github)
df = pd.read_csv('data/projection1.csv')
df.head()

"""## Initializing the Network"""

G = nx.from_pandas_edgelist(df, source='disease1', target='disease2', edge_attr='weight')
# save the network for later use
with open("data/network.gpickle", "wb") as f:
    pickle.dump(G, f)

"""## Visualizing the Network

Node size is proportional to its degree
An edge size is proportional to its weight, additionally the edge color gets darker the higher its weight
"""

net = Network(notebook=True,cdn_resources='remote', height="750px", width="100%", bgcolor="#e8f1ff", font_color="#000c1f", select_menu=True, filter_menu=True)
net.toggle_hide_edges_on_drag(False)
net.force_atlas_2based()

sources = df['disease1']
targets = df['disease2']
weights = df['weight']
normalized_weights = (weights - min(weights)) / (max(weights) - min(weights))

edge_data = zip(sources, targets, normalized_weights)

min_edge_color = '#1772ff'
max_edge_color = '#ff2146'

for e in edge_data:
    src = e[0]
    dst = e[1]
    w = e[2]
    edge_color = matplotlib.colors.to_hex(np.array(matplotlib.colors.to_rgb(min_edge_color)) + w * (np.array(matplotlib.colors.to_rgb(max_edge_color)) - np.array(matplotlib.colors.to_rgb(min_edge_color))))
    node_color = '#ff2146'
    edge_size = 1 + 5 * w
    node_size = 5 + 20 * G.degree[src]

    net.add_node(src, src, title=src, color=node_color, size=node_size, value=G.degree[src])
    net.add_node(dst, dst, title=dst, color=node_color, size=node_size, value=G.degree[dst])
    net.add_edge(src, dst, value=w, color=edge_color, title=w, width=edge_size, physics=True)

net.show("networks/initial_network.html")
# display(HTML("network.html"))

draw_network(G)