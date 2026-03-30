import requests
import time
import json

urls = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter"
]

query = """
[out:json][timeout:60];
area[name="Edmonton"]->.searchArea;

(
  node["shop"](area.searchArea);
  node["amenity"](area.searchArea);
  node["office"](area.searchArea);
  node["craft"](area.searchArea);
  node["leisure"](area.searchArea);

  way["shop"](area.searchArea);
  way["amenity"](area.searchArea);
  way["office"](area.searchArea);
  way["craft"](area.searchArea);
  way["leisure"](area.searchArea);
);

out center;
"""

print("Requesting data...")

data = None

for attempt in range(5):
    url = urls[attempt % len(urls)]

    try:
        response = requests.post(
            url,
            data=query,
            timeout=120,
            headers={"User-Agent": "business-tracker"}
        )

        print("Using:", url)
        print("Status code:", response.status_code)

        if response.status_code == 200:
            try:
                data = response.json()
                break
            except Exception as e:
                print("JSON error:", e)

    except Exception as e:
        print("Request error:", e)

    print("Retrying in 10 seconds...")
    time.sleep(10)

if not data:
    print("Failed after retries.")
    exit(1)

# ✅ Process data safely
businesses = []

for element in data.get("elements", []):
    tags = element.get("tags", {})
    name = tags.get("name", "Unknown")

    # Handle nodes vs ways
    lat = element.get("lat")
    lon = element.get("lon")

    if not lat or not lon:
        center = element.get("center")
        if center:
            lat = center.get("lat")
            lon = center.get("lon")

    if not lat or not lon:
        continue

    businesses.append({
        "id": element.get("id"),
        "name": name,
        "lat": lat,
        "lon": lon
    })

# ✅ SAVE FILE
with open("businesses.json", "w") as f:
    json.dump(businesses, f)

print(f"Saved {len(businesses)} businesses.")

