from utils import load_network
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

"""
### Identifying Important Bridges
We try to identify the important bridges in the network, by removing an edge and calculating the new shortest path between the nodes on the extreme of the edge, and thus when done, we can sort these new shortest path length to indicate which edge removal will result in the highest new shortest path length (We display the top 10 important edges). It is important to note that for all the edges (except 25 edges), only 3 hops are needed to reach all connected nodes if their direct connection is removed.
"""

G = load_network("data/disease_network.gpickle")

shortest_paths = []
for u, v in G.edges:
    G.remove_edge(u, v)

    try:
        path = nx.shortest_path(G, u, v)
        shortest_paths.append((u,v,len(path)))
    except nx.NetworkXNoPath:
        pass

    G.add_edge(u, v)

shortest_paths.sort(key=lambda x: x[2], reverse=True)

important_edges = shortest_paths[:10]

for u, v, length in important_edges:
    print(f"{u} <----> {v}: {length}")


plt.hist([x[2] for x in shortest_paths], bins=100)
plt.xlabel("Shortest Path Length")
plt.ylabel("Frequency")
plt.title("Distribution of Shortest Paths")
plt.show()

# saving the important edges
important_edges_df = pd.DataFrame(important_edges, columns=["disease1", "disease2", "shortest_path_length"])
important_edges_df.to_csv("data/important_edges.csv", index=False)
