import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
loc1 = "Washington, D.C."
loc2 = "Baltimore, Maryland"
key = "586e0a7d-bcd7-4a6e-8007-391a0b9630a1" # Replace with your Graphhopper API key

def geocoding (location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q":location, "limit": "1", "key":key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    
    print("Geocoding API URL for " + location + ":\n" + url)

    if json_status == 200:
       json_data = requests.get(url).json()
       lat=(json_data["hits"][0]["point"]["lat"])
       lng=(json_data["hits"][0]["point"]["lng"])
    else:
       lat="null"
       lng="null"
    
    return json_status,lat,lng

while True:
    loc1 = input("Starting Location: ")
    if loc1 == "quit" or loc1 == "q":
        break
    orig = geocoding(loc1, key)
    print(orig)
 
    loc2 = input("Destination: ")
    if loc2 == "quit" or loc2 == "q":
        break
    dest = geocoding(loc2, key)
    print(dest)