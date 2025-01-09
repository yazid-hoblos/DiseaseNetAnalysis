from utils import *

G = load_network('data/disease_network.gpickle')

"""## Generating a preferential attachment version of the network
BA with same Density
Calculate an m value, m = density * N/2, such that the density of BA will be the same of the disease network
"""
graph_density = nx.density(G)

# generate a preferential attachment version of G with the same number of nodes and density
pref = nx.barabasi_albert_graph(G.number_of_nodes(), int(graph_density * G.number_of_nodes() / 2))

print_metrics(pref, "Preferential Attachment Graph")
print_centralities(pref)
plot_centralities(pref, "BA_simulation")
draw_network(pref)

## Hidden Parameter Model with same Degree Exponent

hidden_param_net = hidden_parameter_network(G.number_of_nodes(), sum(dict(G.degree()).values()) / G.number_of_nodes(), omega=find_degree_exponent(G))

print_metrics(hidden_param_net, "Hidden Parameter Network")
print_centralities(hidden_param_net)
plot_centralities(hidden_param_net, "Hidden-Parameter_simulation")
draw_network(hidden_param_net)