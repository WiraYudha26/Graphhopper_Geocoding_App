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
    
    # Input for destination
    loc2 = input("Destination: ")
    if loc2.lower() in ["quit", "q"]:
        break
    dest = geocoding(loc2, key)
    
    print("=================================================")
    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": "car"}) + op + dp
        
        paths_response = requests.get(paths_url)
        paths_status = paths_response.status_code
        paths_data = paths_response.json() 
        if paths_status == 200:
            distance = paths_data["paths"][0]["distance"]
            duration = paths_data["paths"][0]["time"]

            # Convert distance to km and miles
            km = distance / 1000
            miles = km / 1.61
            
            # Convert duration to hours, minutes, and seconds
            sec = int(duration / 1000 % 60)
            min = int(duration / 1000 / 60 % 60)
            hr = int(duration / 1000 / 60 / 60)
            
            print(f"Routing API Status: {paths_status}\nRouting API URL:\n{paths_url}")
            print(f"Directions from {orig[3]} to {dest[3]}")
            print("=================================================")
            print(f"Distance Traveled: {miles:.1f} miles / {km:.1f} km")
            print(f"Trip Duration: {hr:02d}:{min:02d}:{sec:02d}")            
            
            # Iterate through instructions
            print("Step-by-step directions:")
            for step in paths_data["paths"][0]["instructions"]:
                instruction = step["text"]
                step_distance = step["distance"]
                step_km = step_distance / 1000
                step_miles = step_km / 1.61
                print(f"{instruction} ( {step_km:.2f} km / {step_miles:.2f} miles )")
            
            print("=================================================")
        else:
            print(f"Routing failed. Status: {paths_status}")
            if "message" in paths_data:
                print(f"Error: {paths_data['message']}")
    else:
        print("Failed to geocode one or both locations. Please try again.")
