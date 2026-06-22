import requests
import pandas as pd

url = "https://api.mfapi.in/mf/125497"

response = requests.get(url)

data = response.json()

# Get scheme name
scheme_name = data["meta"]["scheme_name"]

# Get latest NAV record
latest_nav = data["data"][0]

# Create dataframe
nav_df = pd.DataFrame([{
    "scheme_name": scheme_name,
    "date": latest_nav["date"],
    "nav": latest_nav["nav"]
}])

print(nav_df)

# Save CSV
nav_df.to_csv("data/raw/live_nav_snapshot.csv", index=False)

print("\nCSV saved successfully!")