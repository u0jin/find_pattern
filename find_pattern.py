import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms import community
from networkx.algorithms.community import greedy_modularity_communities

def draw_subgraph(graph, nodes, title, max_edge_amount, max_edge_width=5):
    subgraph = graph.subgraph(nodes)
    pos = nx.spring_layout(subgraph)
    plt.figure(figsize=(10, 10))
    nx.draw(subgraph, pos, node_color='#9538F2', with_labels=True, node_size=1000, font_size=10)
    edge_widths = [d['transaction_amount'] / max_edge_amount * max_edge_width for _, _, d in subgraph.edges(data=True)]
    nx.draw(subgraph, pos, node_color='#9538F2', with_labels=True, node_size=1000, font_size=10, width=edge_widths)
    plt.title(title)
    plt.show()

csv_file = 'other.Transaction_bc1q5tvvnwzhd96ep299vfcarq0vrkuudqu8wtpyny.csv'
transactions = pd.read_csv(csv_file, sep=',', quotechar='"', escapechar='\\', on_bad_lines='skip')

transactions = transactions.dropna()
transactions['transaction_amount'] = pd.to_numeric(transactions['transaction_amount'], errors='coerce')
transactions['log_amount'] = transactions['transaction_amount'].apply(lambda x: np.log(float(x) + 1.0))

# Filter transactions if necessary
# illicit_transactions = transactions[transactions['illicit'] == True]

graph = nx.from_pandas_edgelist(transactions, source='sending_wallet', target='receiving_wallet', edge_attr=['transaction_amount', 'log_amount'])

max_edge_amount = max([d['transaction_amount'] for _, _, d in graph.edges(data=True)])

# Find star networks
star_nodes = [node for node in graph.nodes() if graph.degree(node) > 2]

# Find chain networks
chain_nodes = [edge for edge in graph.edges() if graph.degree(edge[0]) == 1 and graph.degree(edge[1]) == 1]

# Find circular networks
circular_networks = [cycle for cycle in nx.cycle_basis(graph) if len(cycle) > 2]

# Find clique or community structures
communities = list(greedy_modularity_communities(graph))

print("Star Nodes:", star_nodes)
print("Chain Nodes:", chain_nodes)
print("Circular Networks:", circular_networks)
print("Clique or Community Structures:", [list(community) for community in communities])

# Visualize Star Networks
if star_nodes:
    for node in star_nodes:
        neighbors = list(graph.neighbors(node))
        draw_subgraph(graph, [node] + neighbors, f'Star Network Centered at Node {node}', max_edge_amount)

# Visualize Chain Networks
if chain_nodes:
    for chain in chain_nodes:
        draw_subgraph(graph, list(chain), f'Chain Network Between Nodes {chain[0]} and {chain[1]}', max_edge_amount)

# Visualize Circular Networks
if circular_networks:
    for i, cycle in enumerate(circular_networks):
        draw_subgraph(graph, cycle, f'Circular Network {i + 1}', max_edge_amount)

# Visualize Clique or Community Structures
if communities:
    for i, community in enumerate(communities):
        draw_subgraph(graph, community, f'Clique or Community Structure {i + 1}', max_edge_amount)
