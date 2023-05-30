import requests

# Define the Bitcoin address
bitcoin_address = "bc1qekmw2l8fw5c4q5sf5lqenc9g0sfgk6dcz078dt"  # Replace with the desired Bitcoin address

# Define the Esplora API endpoint
api_url = f"https://blockstream.info/api/address/{bitcoin_address}"

try:
    # Send a GET request to the Esplora API
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        ip_address = data["address"]
        print(f"The IP address associated with Bitcoin address {bitcoin_address} is: {ip_address}")
    else:
        print(f"Error occurred while retrieving address info. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Error occurred while retrieving address info: {str(e)}")
