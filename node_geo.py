import requests

def get_geolocation(ip_address):
    api_key = 'YOUR_API_KEY'  # Replace with your API key from ipapi.com
    url = f'https://ipapi.co/{ip_address}/json/'

    try:
        response = requests.get(url)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while retrieving geolocation data: {str(e)}")
        return None

# Example usage
ip_address = '192.168.0.1'  # Replace with the IP address of the Bitcoin node
geolocation_data = get_geolocation(ip_address)

if geolocation_data is not None:
    country = geolocation_data.get('country_name')
    city = geolocation_data.get('city')
    latitude = geolocation_data.get('latitude')
    longitude = geolocation_data.get('longitude')

    print(f"Geolocation information for IP address {ip_address}:")
    print(f"Country: {country}")
    print(f"City: {city}")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
