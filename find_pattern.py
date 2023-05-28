import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from networkx.algorithms import community
from networkx.algorithms.community import greedy_modularity_communities

# Function to draw subgraph with edge widths proportional to the transaction amount
def draw_subgraph(graph, nodes, title, max_edge_amount, max_edge_width=5):
    subgraph = graph.subgraph(nodes)
    pos = nx.spring_layout(subgraph)
    plt.figure(figsize=(10, 10))
    nx.draw(subgraph, pos, node_color='#9538F2', with_labels=True, node_size=1000, font_size=10)
    edge_widths = [d['transaction_amount'] / max_edge_amount * max_edge_width for _, _, d in subgraph.edges(data=True)]
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=nx.get_edge_attributes(subgraph, 'transaction_amount'))
    nx.draw(subgraph, pos, node_color='#9538F2', with_labels=True, node_size=1000, font_size=10, width=edge_widths)
    plt.title(title)
    plt.show()

# Function to preprocess the raw transaction data
def preprocess_transactions(csv_file):
    transactions = pd.read_csv(csv_file, sep=',', quotechar='"', escapechar='\\', on_bad_lines='skip')
    transactions = transactions.dropna()
    transactions['transaction_amount'] = pd.to_numeric(transactions['transaction_amount'], errors='coerce')
    transactions['log_amount'] = transactions['transaction_amount'].apply(lambda x: np.log(float(x) + 1.0))
    return transactions

# Function to build network graph from transactions
def build_graph(transactions):
    return nx.from_pandas_edgelist(transactions, source='sending_wallet', target='receiving_wallet', edge_attr=['transaction_amount', 'log_amount'])

# Function to find star networks
def find_star_nodes(graph):
    return [node for node in graph.nodes() if graph.degree(node) > 2]

# Function to find chain networks
def find_chain_nodes(graph):
    return [edge for edge in graph.edges() if graph.degree(edge[0]) == 1 and graph.degree(edge[1]) == 1]

# Function to find circular networks
def find_circular_networks(graph):
    return [cycle for cycle in nx.cycle_basis(graph) if len(cycle) > 2]

# Function to find community structures
def find_communities(graph):
    return list(greedy_modularity_communities(graph))

# Load and preprocess transaction data
csv_file = 'other.Transaction_bc1q5tvvnwzhd96ep299vfcarq0vrkuudqu8wtpyny.csv'
transactions = preprocess_transactions(csv_file)

# Build the graph
graph = build_graph(transactions)

# Calculate maximum transaction amount for later visualization
max_edge_amount = max([d['transaction_amount'] for _, _, d in graph.edges(data=True)])

# Find and visualize different types of networks
star_nodes = find_star_nodes(graph)
chain_nodes = find_chain_nodes(graph)
circular_networks = find_circular_networks(graph)
communities = find_communities(graph)

for node in star_nodes:
    neighbors = list(graph.neighbors(node))
    draw_subgraph(graph, [node] + neighbors, f'Star Network Centered at Node {node}', max_edge_amount)
    print(f"Star Network: This graph represents a network centered around the node {node}. In the context of Bitcoin transactions, this could imply that one address (the central node) is transacting with many other addresses. The central node in a star network could be a central entity like a Bitcoin exchange or a popular service.")

for chain in chain_nodes:
    draw_subgraph(graph, list(chain), f'Chain Network Between Nodes {chain[0]} and {chain[1]}', max_edge_amount)
    print(f"Chain Network: This graph represents a sequence of nodes where each node only has a connection with its predecessor and successor. This kind of network might suggest a sequence of transactions where each address only transacts with the next one in the chain. This might represent a chain of transactions intended to obscure the source of funds (common in money laundering).")

for i, cycle in enumerate(circular_networks):
    draw_subgraph(graph, cycle, f'Circular Network {i + 1}', max_edge_amount)
    print(f"Circular Network: This graph represents a circular network structure where the nodes form a closed loop. This could represent a circular flow of transactions. It could also indicate a potential attempt to obfuscate transaction flows by circulating funds among a group of addresses.")

for i, community in enumerate(communities):
    draw_subgraph(graph, community, f'Clique or Community Structure {i + 1}', max_edge_amount)
    print(f"Clique or Community Structure: This graph represents a community structure where a group of nodes are densely connected. This could indicate a group of addresses transacting heavily among each other. It might represent a group of addresses controlled by the same entity or a group of users frequently transacting with each other.")
