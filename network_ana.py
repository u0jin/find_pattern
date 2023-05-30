import networkx as nx
import matplotlib.pyplot as plt

# Create an empty graph
G = nx.Graph()

# Read transaction details from the file
transaction_file = "other.Transaction_bc1q5tvvnwzhd96ep299vfcarq0vrkuudqu8wtpyny.csv"  # Replace with the actual file name/path
transactions = []  # List to store the transactions

# Read the transaction file and extract the relevant information
with open(transaction_file, "r") as file:
    next(file)  # Skip the header line
    for line in file:
        values = line.strip().split(",")
        if len(values) >= 2:
            sending_wallet = values[1]
            receiving_wallet = values[2]
            transactions.append((sending_wallet, receiving_wallet))

# Add nodes (Bitcoin addresses) to the graph
addresses = set()
for sending_wallet, receiving_wallet in transactions:
    addresses.add(sending_wallet)
    addresses.add(receiving_wallet)

G.add_nodes_from(addresses)

# Add edges (transactions) between the nodes
G.add_edges_from(transactions)

# Visualize the graph
pos = nx.spring_layout(G)  # Choose a layout algorithm

# Identify influential nodes based on eigenvector centrality
eigenvector_centrality = nx.eigenvector_centrality(G)
influential_nodes = [address for address, centrality in eigenvector_centrality.items() if centrality >= 0.2]

# Customize node labels to display truncated addresses
node_labels = {address: address[:8] + "..." + address[-6:] if address in influential_nodes else "" for address in G.nodes}

# Draw the network graph
nx.draw_networkx(G, pos=pos, with_labels=False, node_size=100)

# Draw the influential nodes with the wallet address as labels
for address in influential_nodes:
    x, y = pos[address]
    plt.text(x, y + 0.1, address, ha="center", color="red")

plt.title("Bitcoin Address Network")
plt.axis("off")
# Save the graph as an image
plt.savefig("network_graph.png", dpi=300)
plt.show()

# Calculate centrality measures
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)
eigenvector_centrality = nx.eigenvector_centrality(G)

print("Degree Centrality:")
for address, centrality in degree_centrality.items():
    print(f"{address}: {centrality}")
    
print("\nDegree centrality measures the number of connections (edges) that a node (address) has in the network. "
      "Addresses with higher degree centrality are more connected or involved in more transactions.")

print("\nBetweenness Centrality:")
for address, centrality in betweenness_centrality.items():
    print(f"{address}: {centrality}")
    
print("\nBetweenness centrality quantifies the importance of a node (address) by measuring how often it appears "
      "on the shortest paths between all pairs of nodes. Addresses with higher betweenness centrality act as "
      "key intermediaries or bridges in the network.")

print("\nEigenvector Centrality:")
for address, centrality in eigenvector_centrality.items():
    print(f"{address}: {centrality}")

print("\nEigenvector centrality measures the influence of a node (address) in the network, taking into account "
      "the centrality of its neighbors. Addresses with higher eigenvector centrality are connected to other "
      "highly influential addresses.")
