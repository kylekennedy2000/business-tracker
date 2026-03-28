import requests
import json
import time

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

query = """
[out:json];
(
  node["shop"](53.45,-113.65,53.65,-113.35);
  node["amenity"](53.45,-113.65,53.65,-113.35);
);
out;
"""

print("Requesting data...")

try:
    response = requests.get(OVERPASS_URL, params={'data': query}, timeout=60)
except Exception as e:
    print("Request failed:", e)
    exit()

print("Status code:", response.status_code)

if response.status_code != 200:
    print("Non-200 response:")
    print(response.text[:500])
    exit()

# Sometimes API returns non-JSON even with 200
try:
    data = response.json()
except Exception:
    print("Failed to parse JSON. Raw response:")
    print(response.text[:500])
    exit()

businesses = []

for element in data.get('elements', []):
    name = element['tags'].get('name', 'Unknown')
    lat = element.get('lat')
    lon = element.get('lon')

    if lat and lon:
        businesses.append({
            "name": name,
            "lat": lat,
            "lon": lon
        })

with open("businesses.json", "w") as f:
    json.dump(businesses, f, indent=2)

print(f"Saved {len(businesses)} businesses.")
