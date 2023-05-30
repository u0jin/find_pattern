import requests

# Define the API endpoint and parameters
api_endpoint = "https://api.ipgeolocation.io/ipgeo"
api_key = "84a11b0c2bf54368b7a22123634737dd"  # Replace with your actual API key
ip_address = "1.1.1.1"  # Replace with the IP address you want to query

# Construct the API URL with the endpoint, IP address, and API key
api_url = f"{api_endpoint}?apiKey={api_key}&ip={ip_address}"

# Send a GET request to the API
response = requests.get(api_url)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()

    # Extract relevant information from the response
    country = data.get("country_name")
    city = data.get("city")
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    # Print the geolocation information
    print("Geolocation Information:")
    print(f"Country: {country}")
    print(f"City: {city}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
else:
    print("Error occurred while querying the API.")
