from utils import *

G = load_network("data/disease_network.gpickle")
    
"""## Identify the Disease Network Components

We identified 65 Components in the Disease network, additionally we noticed the existence of only one large component.
"""

components = nx.connected_components(G)
components = sorted(components, key=len, reverse=True)

table = prettytable.PrettyTable(['Component', 'Size', 'Nodes', 'Edges'])
for i, c in enumerate(components[:10]):
    subgraph = G.subgraph(c)
    table.add_row([i+1, len(c), subgraph.number_of_nodes(), subgraph.number_of_edges()])
print(table)

"""## Analyzing the Central Nodes and Edges in the Disease Network"""

print_metrics(G)
print_centralities(G)
plot_centralities(G, "disease_network")
