import json
import os

if not os.path.exists("businesses.json"):
    print("No new data found. Skipping comparison.")
    exit()

# Load new data
with open("businesses.json") as f:
    new_data = json.load(f)

# Load old data (if exists)
if os.path.exists("old_businesses.json"):
    with open("old_businesses.json") as f:
        old_data = json.load(f)
else:
    print("No old data found. Creating baseline...")
    os.rename("businesses.json", "old_businesses.json")
    exit()

# Create sets of IDs
old_ids = set(b["id"] for b in old_data if "id" in b)

new_businesses = []

for b in new_data:
    if b.get("id") not in old_ids:
        b["new"] = True
        new_businesses.append(b)
    else:
        b["new"] = False

print(f"New businesses found: {len(new_businesses)}")

# Save updated dataset
with open("old_businesses.json", "w") as f:
    json.dump(new_data, f)
