from bitcoinrpc.authproxy import AuthServiceProxy

# Configure connection to the Bitcoin Core JSON-RPC API
rpc_user = "your_rpc_username"
rpc_password = "your_rpc_password"
rpc_host = "localhost"
rpc_port = 8332  # Default Bitcoin Core JSON-RPC port

# Establish a connection to the Bitcoin Core node
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

# Define the Bitcoin address of interest
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

# Analyze the transactions associated with the Bitcoin address
transactions = address_info["transactions"]

for txid in transactions:
    try:
        transaction_info = rpc_connection.gettransaction(txid)
        inputs = transaction_info["vin"]
        outputs = transaction_info["vout"]

        print(f"Transaction ID: {txid}")
        print("Inputs:")
        for inp in inputs:
            print(inp["address"])

        print("Outputs:")
        for outp in outputs:
            addresses = outp["scriptPubKey"]["addresses"]
            for addr in addresses:
                print(addr)

        print("---")
    except Exception as e:
        print(f"Error occurred while analyzing transaction {txid}: {str(e)}")
