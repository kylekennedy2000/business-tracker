import requests
import time
import json

url = "https://overpass-api.de/api/interpreter"

query = """
[out:json];
area[name="Edmonton"]->.searchArea;
(
  node["shop"](area.searchArea);
  node["amenity"](area.searchArea);
);
out;
"""

print("Requesting data...")

for attempt in range(3):  # retry up to 3 times
    response = requests.post(url, data=query)

    print("Status code:", response.status_code)

    if response.status_code == 200:
        data = response.json()

        businesses = []
        for element in data["elements"]:
            name = element.get("tags", {}).get("name", "Unknown")
            lat = element.get("lat")
            lon = element.get("lon")

           businesses.append({
    "id": element.get("id"),
    "name": name,
    "lat": lat,
    "lon": lon
})


        with open("businesses.json", "w") as f:
            json.dump(businesses, f)

        print(f"Saved {len(businesses)} businesses.")
        break

    else:
        print("Retrying in 5 seconds...")
        time.sleep(5)
else:
    print("Failed after 3 attempts.")
    exit(1)

