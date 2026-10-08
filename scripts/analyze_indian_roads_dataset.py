import urllib.request
import pandas as pd
import io

url = 'https://raw.githubusercontent.com/Prashantsundar/Indian-Road-Accident-Dataset-Analysis-2022-2025-Python---Jupyternotebook/main/indian_roads_dataset.csv'
print("Downloading and analyzing indian_roads_dataset.csv...")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = resp.read()

df = pd.read_csv(io.BytesIO(data))
print(f"Total rows: {len(df)}")
print(f"Unique states: {df['state'].unique()}")
print(f"Unique cities: {df['city'].unique()}")
print(f"Severity counts:\n{df['accident_severity'].value_counts()}")
print(f"Latitude range: {df['latitude'].min()} to {df['latitude'].max()}")
print(f"Longitude range: {df['longitude'].min()} to {df['longitude'].max()}")
