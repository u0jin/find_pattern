import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Load the preprocessed dataset
data = pd.read_csv('preprocessed_data.csv')

# Create a directed graph from the transaction data
G = nx.from_pandas_edgelist(data, source='sending_wallet', target='receiving_wallet', create_using=nx.DiGraph())

# Get weakly connected components
weakly_connected = nx.weakly_connected_components(G)

# Create lists to store the calculated features
address_list = []
degree_centrality_list = []
clustering_coefficient_list = []
node_count_list = []
edge_count_list = []
max_path_length_list = []

# Calculate features for each weakly connected component
for component in weakly_connected:
    component_graph = G.subgraph(component)

    # Calculate degree centrality for each node in the component
    degree_centrality = nx.degree_centrality(component_graph)

    # Calculate clustering coefficient for each node in the component
    clustering_coefficient = nx.clustering(component_graph)

    # Calculate the number of nodes and edges in the component
    node_count = len(component_graph.nodes)
    edge_count = len(component_graph.edges)

    # Calculate the maximum path length in the component
    try:
        max_path_length = nx.diameter(component_graph)
    except nx.NetworkXError:
        max_path_length = float('inf')

    # Append the calculated features to the lists
    address_list.extend(degree_centrality.keys())
    degree_centrality_list.extend(degree_centrality.values())
    clustering_coefficient_list.extend(clustering_coefficient.values())
    node_count_list.extend([node_count] * len(degree_centrality))
    edge_count_list.extend([edge_count] * len(degree_centrality))
    max_path_length_list.extend([max_path_length] * len(degree_centrality))

# Create a DataFrame to store the results
df_results = pd.DataFrame({
    'Address': address_list,
    'Degree Centrality': degree_centrality_list,
    'Clustering Coefficient': clustering_coefficient_list,
    'Node Count': node_count_list,
    'Edge Count': edge_count_list,
    'Maximum Path Length': max_path_length_list
})

# Print the table
print(df_results)

# Visualize the results as a bar plot
plt.bar(df_results['Address'], df_results['Degree Centrality'])
plt.xlabel('Address')
plt.ylabel('Degree Centrality')
plt.title('Degree Centrality of Addresses')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
plt.savefig('degree_centrality_plot.png')
