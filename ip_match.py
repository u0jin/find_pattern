from bitcoinrpc.authproxy import AuthServiceProxy
import csv

# Configure connection to the Bitcoin Core JSON-RPC API
rpc_user = "your_rpc_username"
rpc_password = "your_rpc_password"
rpc_host = "localhost"
rpc_port = 8332  # Default Bitcoin Core JSON-RPC port

# Establish a connection to the Bitcoin Core node
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@{rpc_host}:{rpc_port}")

# Read IP addresses from kp_ip_address.txt file
ip_addresses = []
with open('kp_ip_address.txt', 'r') as ip_file:
    for line in ip_file:
        ip_addresses.append(line.strip())

# Read hacker's wallet addresses from hacker_data.csv file
hacker_wallet_addresses = []
with open('hacker_data.csv', 'r') as hacker_file:
    csv_reader = csv.reader(hacker_file)
    for row in csv_reader:
        hacker_wallet_addresses.append(row[0])

# Find matching IP addresses and hacker's wallet addresses
matched_addresses = []
for ip_address in ip_addresses:
    for wallet_address in hacker_wallet_addresses:
        try:
            address_info = rpc_connection.getaddressinfo(wallet_address)
        except Exception as e:
            print(f"Error occurred while retrieving address info for {wallet_address}: {str(e)}")
            continue
        
        if "address" not in address_info:
            print(f"Address not found for {wallet_address}.")
            continue
        
        try:
            address_ip = address_info["address"]["address"]
        except KeyError:
            print(f"IP address not found for {wallet_address}.")
            continue
        
        if ip_address == address_ip:
            matched_addresses.append((ip_address, wallet_address))

# Save matched hacker's wallet addresses in matched_hacker_addresses.csv file
with open('matched_hacker_addresses.csv', 'w', newline='') as matched_file:
    csv_writer = csv.writer(matched_file)
    csv_writer.writerow(['IP Address', 'Hacker Wallet Address'])
    csv_writer.writerows(matched_addresses)

print("Matched hacker's wallet addresses saved successfully.")
