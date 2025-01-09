from utils import *
import infomap
from pyvis.network import Network
import matplotlib.colors


G = load_network("data/disease_network.gpickle")

## Community Detection

node_to_int = {node: i for i, node in enumerate(G.nodes)}

im = infomap.Infomap()

# Extract sources, targets, and weights from G
sources = [source for source, _ in G.edges()]
targets = [target for  _, target in G.edges()]
weights = np.array([data.get('weight') for _, _, data in G.edges(data=True)])

for d1, d2, w in zip(sources, targets, weights):
    im.add_link(node_to_int[d1], node_to_int[d2], w)

im.run()

communities = {}

for node in im.tree:
    if node.is_leaf:
        node_name = list(G.nodes)[node.node_id]

        community_id = node.module_id

        if community_id not in communities:
            communities[community_id] = []
        communities[community_id].append(node_name)


largest_communities = sorted(communities.values(), key=len, reverse=True)[:10]

colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'pink', 'gray', 'cyan', 'magenta']
node_colors = {}
for i, nodes in enumerate(largest_communities):
    for node in nodes:
        node_colors[node] = colors[i % len(colors)]

default_color = 'black'
for node in G.nodes:
    if node not in node_colors:
        node_colors[node] = default_color

net = Network(notebook=True,cdn_resources='remote', height="750px", width="100%", bgcolor="#e8f1ff", font_color="#000c1f", select_menu=True, filter_menu=True)
net.toggle_hide_edges_on_drag(False)
net.force_atlas_2based()

normalized_weights = (weights - min(weights)) / (max(weights) - min(weights))

edge_data = zip(sources, targets, normalized_weights)

min_edge_color = '#1772ff'
max_edge_color = '#ff2146'

# load important edges
important_edges = pd.read_csv("data/important_edges.csv",sep=',').values

for e in edge_data:
    src = e[0]
    dst = e[1]
    w = e[2]

    edge_color = matplotlib.colors.to_hex(np.array(matplotlib.colors.to_rgb(min_edge_color)) + w * (np.array(matplotlib.colors.to_rgb(max_edge_color)) - np.array(matplotlib.colors.to_rgb(min_edge_color))))

    for imp_edge in important_edges:
      s, d, we = imp_edge
      if src == s and dst == d:
        edge_color = "black"
        edge_size = 1 + 1000 * w
      else:
        edge_size = 1 + 5 * w


    node_size = 5 + 20 * G.degree[src]

    net.add_node(src, src, title=src, color=node_colors[src], size=node_size, value=G.degree[src])
    net.add_node(dst, dst, title=dst, color=node_colors[dst], size=node_size, value=G.degree[dst])
    net.add_edge(src, dst, value=edge_size, color=edge_color, title=w, width=edge_size, physics=True)

net.show("networks/clustered_network.html")