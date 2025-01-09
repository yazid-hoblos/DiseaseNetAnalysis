import pandas as pd
import matplotlib.pyplot as plt
import prettytable
import networkx as nx
import numpy as np
import itertools
import random as rnd
import collections
from scipy.stats import linregress
import pickle
import os

def load_network(file_path):
    with open(file_path, "rb") as f:
        G = pickle.load(f)
    return G

def draw_network(network):
    pos=nx.spring_layout(network)
    nx.draw(network, pos, with_labels=False, node_size=3, width=0.3, edge_color='grey')
    plt.show()
    plt.clf()

def plot_centrality(network, centrality,name=None):
    cent = centrality(network)
    sorted_cent = sorted(cent.items(), key=lambda x:x[1], reverse=True)
    plt.hist(list(cent.values()), bins=20, edgecolor='black', alpha=0.7)
    plt.grid()
    plt.title(centrality.__name__)
    plt.xlabel(f"{centrality.__name__} Distribution")
    plt.ylabel("Frequency")
    plt.savefig(f"plots/{name}/{name+'_'+centrality.__name__}.png")
    plt.clf()

    return


def print_centralities(network):
    deg_cen = nx.degree_centrality(network)
    bet_cen = nx.betweenness_centrality(network)
    clo_cen = nx.closeness_centrality(network)
    eig_cen = nx.eigenvector_centrality(network)

    # degree centrality
    sorted_deg_cen = sorted(deg_cen.items(), key=lambda x:x[1], reverse=True)
    # betweenness centrality
    sorted_bet_cen = sorted(bet_cen.items(), key=lambda x:x[1], reverse=True)
    # closeness centrality
    sorted_clo_cen = sorted(clo_cen.items(), key=lambda x:x[1], reverse=True)
    # eigenvector centrality
    sorted_eig_cen = sorted(eig_cen.items(), key=lambda x:x[1], reverse=True)

    table = prettytable.PrettyTable(['Degree', 'Betweenness', 'Closeness', 'Eigenvector'])

    for i in range(3):
        table.add_row([ str(sorted_deg_cen[i][0]) + ': ' + str(sorted_deg_cen[i][1]),
                        str(sorted_bet_cen[i][0]) + ': ' + str(sorted_bet_cen[i][1]),
                        str(sorted_clo_cen[i][0]) + ': ' + str(sorted_clo_cen[i][1]),
                        str(sorted_eig_cen[i][0]) + ': ' + str(sorted_eig_cen[i][1])])

    print("Top three nodes for each centrality measure:")
    print(table)

def print_metrics(network, network_name="Disease Network"):
    print("--------------------------")
    print(network_name, "Metrics")
    print("--------------------------")
    print("Number of nodes:", network.number_of_nodes())
    print("Number of edges:", network.number_of_edges())
    print("Average degree:", sum(dict(network.degree()).values()) / network.number_of_nodes())
    print("Graph density:", nx.density(network))
    if nx.is_connected(network):
        print("Average clustering coefficient:", nx.average_clustering(network))
        print("Average shortest path length:", nx.average_shortest_path_length(network))
        print("Diameter:", nx.diameter(network))
    else:
        largest_component = max(nx.connected_components(network), key=len)
        print("Average clustering coefficient:", nx.average_clustering(network.subgraph(largest_component)))
        print("Average shortest path length:", nx.average_shortest_path_length(network.subgraph(largest_component)))
        print("Diameter:", nx.diameter(network.subgraph(largest_component)))
    print("--------------------------")

def plot_centralities(network, title):
    if not os.path.exists(f'plots/{title}'):
        os.makedirs(f'plots/{title}')
    plot_centrality(network, nx.degree_centrality, title)
    plot_centrality(network, nx.betweenness_centrality, title)
    plot_centrality(network, nx.closeness_centrality, title)
    plot_centrality(network, nx.eigenvector_centrality, title)
    plot_centrality(network, nx.clustering, title)
    
def hidden_parameter_network(N, e_k, omega=2.5):
    # e_k is the expected degree of each node, omega is the exponent of the power law

    G = nx.empty_graph(N)

    # According to equation 4.29,  omega = (1 + 1/a)
    alpha = 1 / (omega - 1)

    # @TODO Can also solve the series sum analytically, approximation by definite integrals for example.
    # https://math.stackexchange.com/questions/1576502/calculate-finite-p-series

    # Series = SUM 1/n^(alpha) FOR n FROM 1 to N
    harmonic_series = np.power((1 / (np.arange(N) + 1)), alpha)
    c = (e_k * N) / np.sum(harmonic_series)

    # No need to recalculate the list of n, already have the harmonic series, just multiply by c, Eq. 4.28
    n_list = harmonic_series * c

    # n_expected is calculated to be e_k so it is unnecessary to recalculate it, to a very high precision.
    # unless you want to verify that e_k is correct.
    n_expected = e_k

    # Assign each node a hidden parameter n_i, they are generated above
    edges = itertools.combinations(range(N), 2)
    denominator = (n_expected * N)
    for e in edges:
        # compute probability of connecting two nodes based on equation under
        # Figure 4.18
        p = ((n_list[e[0]] * n_list[e[1]]) / denominator)
        if rnd.random() < p:
            G.add_edge(*e)

    return G

def find_degree_exponent(network):
    degree_sequence = sorted(
                [d for n, d in network.degree()], reverse=True)
    degree_count = collections.Counter(degree_sequence)
    deg, cnt = zip(*degree_count.items())
    return -linregress(np.log(deg), np.log(cnt)).slope + 1
