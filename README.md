# Diseasome Network Analysis

## Context

The work in this repository is based on the article [1]. The diseasome network was constructed based on shared genes between diseases. Several network science approaches were applied to study the general features, topology, and community structure of the diseasome. 

## Preprocessing

Two projections were done to create a two-layer disease-disease network in [projections.py](projections.py). The first layer was based on genotype information and the second on shared phenotypes. Two diseases are linked in the 1st projection if they share at least one gene and in the 2nd if they share at least one symptom. The weight of the connections is defined as the number of common genes or symptoms. 

## Network Analysis

Most analysis steps were adopted from [2]. 

### Visualization 

After the network construction, a dynamic interactive representation was generated in [networks/initial_network.html](networks/initial_network.html).

### Centrality Metrics

The functions in [utils.py](utils.py) were used to study the main metrics of the network and all subsequent simulations, focusing on centrality measures (degree, betweeness, closeness, and eigenvector centralities). 

### Important bridges 

Important bridges in the network were identified by removing each edge and calculating the new shortest path between the nodes on the extreme of the edge. For all edges (except 25), only 3 hops are needed to reach all connected nodes if their direct connection is removed. Some of these bridges will be later found to link two distinct communities in the network. 

## Simulations

Multiple random and non-random approaches were applied to create simulations of our network. Corresponding plots could be found in seperate folders in [plots](plots).

### Randomized

Erdos-Renyi model and degree-preserving randomization were tested for a random simulation. 

### Preferential Attachment (Barabasi-Albert model)

The BA model was used to simulate networks based on preferential attachment, where new nodes are more likely to connect to existing nodes with a higher degree resulting in a scale-free structure. This preferential attachement property is prevalent for many real-world biological networks. 

### Hidden Parameter Model

The hidden parameter model was used to simulate networks where the likelihood of connections depends on intrinsic parameters assigned to each node. These parameters influence edge formation, introducing additional complexity to the network structure. This approach can reflect real-world scenarios with community structures or biased connectivity patterns.

## Community-Detection 

Multiple clustering approaches were tested. Most notably, the communities detected using Infomap are highlighted in [networks/clustered_network.html](networks/clustered_network.html).

![image](https://github.com/user-attachments/assets/a0009c3e-2ba1-49ed-8d6c-c1e1695dafe6)

## References

1. Halu, A., De Domenico, M., Arenas, A. et al. The multiplex network of human diseases. npj Syst Biol Appl 5, 15 (2019). https://doi.org/10.1038/s41540-019-0092-5
2. Barabási, A.-L., Pósfai, M. (2016). Network science. Cambridge: Cambridge University Press. ISBN: 9781107076266 1107076269
