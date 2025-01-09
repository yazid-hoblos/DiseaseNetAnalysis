from utils import *
import networkx as nx

G = load_network('data/disease_network.gpickle')

"""## Generating an ER random version of the Network
We tried multiple methods to generate a randomized version of the network so that we can compare the results of the original network with the randomized one. We tried the following methods:

#### 1. Same Density ER Network
We tried generating an ER network with same density as the Disease Network.

We calculate a p value, p = 2m / (n(n-1))^2, such that using this p value would results in a same density ER network
"""

# get p for ER such that the graph has the same density as the original graph
# p = 2m / (n(n-1))^2

p = 2 * G.number_of_edges() / ((G.number_of_nodes() - 1) ** 2)
er = nx.erdos_renyi_graph(G.number_of_nodes(), p)

print_metrics(er, "Erdos-Renyi Graph")
print_centralities(er)
plot_centralities(er, "Erdos-Renyi_simulation")
draw_network(er)

"""#### 2. Degree Preserving Randomization Model
We use a method, mentioned in the book and the paper, to preserve the degree of every node while reshuffling the edges randomly
"""

G_copy = G.copy()
G_randomized = nx.double_edge_swap(G_copy, nswap=2*G.number_of_edges(), max_tries=G.number_of_edges()*100)

print_metrics(G_randomized, "Degree-Preserved Randomized Graph")
print_centralities(G_randomized)
plot_centralities(G_randomized, "Degree-Preserving-Randomized_simulation")
draw_network(G_randomized)
