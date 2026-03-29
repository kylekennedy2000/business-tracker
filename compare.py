import json
import os
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

if not os.path.exists("businesses.json"):
    print("No new data found. Skipping comparison.")
    exit()

# Load new data
with open("businesses.json") as f:
    new_data = json.load(f)

# Load old data
if os.path.exists("old_businesses.json"):
    with open("old_businesses.json") as f:
        old_data = json.load(f)
else:
    print("No old data found. Creating baseline...")
    for b in new_data:
        b["date_added"] = today

    with open("old_businesses.json", "w") as f:
        json.dump(new_data, f)

    exit()

# Create lookup from old data
old_lookup = {b["id"]: b for b in old_data if "id" in b}

new_count = 0

for b in new_data:
    business_id = b.get("id")

    if business_id in old_lookup:
        # Keep original date
        b["date_added"] = old_lookup[business_id].get("date_added", today)
    else:
        # New business
        b["date_added"] = today
        new_count += 1

print(f"New businesses found: {new_count}")

# Save updated data
with open("old_businesses.json", "w") as f:
    json.dump(new_data, f)
