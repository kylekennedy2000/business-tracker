import json
import os
from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")

# Make sure new data exists
if not os.path.exists("businesses.json"):
    print("No new data found. Skipping comparison.")
    exit()

# Load new data
with open("businesses.json") as f:
    new_data = json.load(f)

# Load old data if it exists
if os.path.exists("old_businesses.json"):
    with open("old_businesses.json") as f:
        old_data = json.load(f)
else:
   from datetime import timedelta

print("No old data found. Creating baseline...")

# Set baseline to 60 days ago so everything starts as "old"
past_date = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")

for b in new_data:
    b["date_added"] = past_date


    # Save baseline
    with open("old_businesses.json", "w") as f:
        json.dump(new_data, f)

    # Save metadata (for frontend display)
    with open("metadata.json", "w") as f:
        json.dump({"last_updated": today}, f)

    exit()

# Create lookup from old data using ID
old_lookup = {}
for b in old_data:
    if "id" in b:
        old_lookup[b["id"]] = b

new_count = 0

# Compare new vs old
for b in new_data:
    business_id = b.get("id")

    if not business_id:
        continue

    if business_id in old_lookup:
        # Keep original date_added
        b["date_added"] = old_lookup[business_id].get("date_added", today)
    else:
        # Brand new business
        b["date_added"] = today
        new_count += 1

print(f"New businesses found: {new_count}")

# Save updated dataset
with open("old_businesses.json", "w") as f:
    json.dump(new_data, f)

# Save metadata (used by your website)
with open("metadata.json", "w") as f:
    json.dump({"last_updated": today}, f)
