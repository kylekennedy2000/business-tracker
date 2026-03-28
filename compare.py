import os

if not os.path.exists("businesses.json"):
    print("No new data found. Skipping comparison.")
    exit()

import json
import os

# First run: create baseline
if not os.path.exists("old_businesses.json"):
    print("No old data found. Creating baseline...")
    os.rename("businesses.json", "old_businesses.json")
    exit()

# Load new data
with open("businesses.json") as f:
    new_data = json.load(f)

# Load old data
with open("old_businesses.json") as f:
    old_data = json.load(f)

# Compare
old_names = set(b["name"] for b in old_data)
new_businesses = []

for b in new_data:
    if b["name"] not in old_names:
        b["new"] = True
        new_businesses.append(b)
    else:
        b["new"] = False

print(f"New businesses found: {len(new_businesses)}")

# Save updated data
with open("businesses.json", "w") as f:
    json.dump(new_data, f, indent=2)

# Replace old snapshot
os.remove("old_businesses.json")
os.rename("businesses.json", "old_businesses.json")
