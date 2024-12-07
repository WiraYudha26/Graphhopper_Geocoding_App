import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "1cad545c-3f6c-4c83-9d2e-cd23fa99ba24"  # Replace with your Graphhopper API key

def geocoding(location, key):
    while location.strip() == "":
        location = input("Enter the location again: ")
    
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    if json_status == 200 and json_data.get("hits"):
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]

        # Ambil komponen lokasi
        name = json_data["hits"][0].get("name", location)
        state = json_data["hits"][0].get("state", "").strip()
        country = json_data["hits"][0].get("country", "").strip()

        # Format nama lokasi
        if state:
            new_loc = f"{name}, {state}, {country}"
        else:
            new_loc = f"{name}, {country}"

        print(f"Geocoding API URL for {new_loc}:\n{url}")
    else:
        lat, lng = "null", "null"
        new_loc = location
        print(f"Geocoding failed for {location}. Status: {json_status}")
        if json_status != 200 and "message" in json_data:
            print(f"Error: {json_data['message']}")

    return json_status, lat, lng, new_loc

while True:
    # Input for starting location
    loc1 = input("Starting Location: ")
    if loc1.lower() in ["quit", "q"]:
        break
    orig = geocoding(loc1, key)
    print(orig)
    
    # Input for destination
    loc2 = input("Destination: ")
    if loc2.lower() in ["quit", "q"]:
        break
    dest = geocoding(loc2, key)
    print(dest)