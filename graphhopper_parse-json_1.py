import requests 
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
loc1 = "Rome, Italy"
loc2 = "Baltimore, Maryland"
key = "586e0a7d-bcd7-4a6e-8007-391a0b9630a1" # Replace with your Graphhopper API key

url = geocode_url + urllib.parse.urlencode({"q":loc1, "limit": "1", "key":key})

replydata = requests.get(url)
json_data = replydata.json()
json_status = replydata.status_code

print(json_data)