#!/usr/bin/env python3
"""Analyze flight routes from dataset to get realistic duration/stops data"""

import pandas as pd
import json
from pathlib import Path

# Load original dataset (has readable format)
data_path = Path(__file__).parent.parent / "data" / "airlines_flights_data.csv"
print(f"Loading data from: {data_path}")

df = pd.read_csv(data_path)
print(f"\n📊 Dataset shape: {df.shape}")
print(f"📋 Columns: {df.columns.tolist()}\n")

# Convert duration from hours to minutes
df['duration_minutes'] = (df['duration'] * 60).round().astype(int)

# Map stops text to numbers
stops_map = {
    'zero': 0,
    'one': 1,
    'two_or_more': 2
}
df['stops_numeric'] = df['stops'].map(stops_map).fillna(0).astype(int)

# Calculate average duration and most common stops per route
route_stats = df.groupby(['source_city', 'destination_city']).agg({
    'duration_minutes': 'mean',
    'stops_numeric': lambda x: x.mode()[0] if len(x) > 0 else 0
}).reset_index()

print("🛫 All routes with average flight times (from real dataset):")
print("=" * 80)

route_defaults = {}
for _, row in route_stats.iterrows():
    source = row['source_city']
    dest = row['destination_city']
    duration = int(round(row['duration_minutes']))
    stops = int(row['stops_numeric'])
    
    route_key = f"{source}->{dest}"
    route_defaults[route_key] = {
        'duration': duration,
        'stops': stops
    }
    
    print(f"  {source:12} → {dest:12} | {duration:3} min | {stops} stops")

# Save to JSON file
output_file = Path(__file__).parent / "route_defaults.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(route_defaults, f, indent=2, ensure_ascii=False)

print(f"\n✅ Saved {len(route_defaults)} routes to: {output_file}")

# Generate JavaScript object for frontend
print("\n\n🔧 JavaScript code for frontend (copy to .jsx files):\n")
print("const routeDefaults = {")
for route_key, values in sorted(route_defaults.items()):
    print(f"  '{route_key}': {{ duration: {values['duration']}, stops: {values['stops']} }},")
print("};")

print(f"\n✅ Total routes: {len(route_defaults)}")
