from bitcoinrpc.authproxy import AuthServiceProxy

# Configure connection to the Bitcoin Core JSON-RPC API
rpc_user = "your_rpc_username"
rpc_password = "your_rpc_password"
rpc_host = "localhost"
rpc_port = 8332  # Default Bitcoin Core JSON-RPC port

# Establish a connection to the Bitcoin Core node
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

# Define the Bitcoin address
bitcoin_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"  # Replace with the desired Bitcoin address

# Get the list of transactions associated with the Bitcoin address
try:
    address_info = rpc_connection.getaddressinfo(bitcoin_address)
except Exception as e:
    print(f"Error occurred while retrieving address info: {str(e)}")
    exit()

if "address" not in address_info:
    print("Address not found.")
    exit()

# Get the IP address associated with the Bitcoin address
try:
    ip_address = address_info["address"]["address"]
except KeyError:
    print("IP address not found for the given Bitcoin address.")
    exit()

# Print the IP address associated with the Bitcoin address
print(f"The IP address associated with Bitcoin address {bitcoin_address} is: {ip_address}")
