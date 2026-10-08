import os
import urllib.request
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATASETS = {
    "indian_roads_dataset.csv": "https://raw.githubusercontent.com/Prashantsundar/Indian-Road-Accident-Dataset-Analysis-2022-2025-Python---Jupyternotebook/main/indian_roads_dataset.csv",
    "accident_prediction_india.csv": "https://raw.githubusercontent.com/rahul-saha18/India-Road-Accident-Exploratory-Data-Analysis./main/accident_prediction_india.csv",
    "ndap_accident_dataset.csv": "https://raw.githubusercontent.com/Saurabh-Vidyarthi/Classification_of_Indian_cities_based_on_road_accident_using_NDAP_Dataset/main/Road_Accident_Classificaion/Dataset/accident_dataset.csv"
}

def download_datasets():
    for filename, url in DATASETS.items():
        filepath = os.path.join(DATA_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Downloading {filename} from {url}...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp, open(filepath, 'wb') as out_f:
                out_f.write(resp.read())
            print(f"Saved {filename} ({os.path.getsize(filepath):,} bytes)")
        else:
            print(f"Already exists: {filename} ({os.path.getsize(filepath):,} bytes)")

def inspect_downloaded():
    print("\n--- Summary of Downloaded Datasets ---")
    for filename in DATASETS.keys():
        filepath = os.path.join(DATA_DIR, filename)
        try:
            df = pd.read_csv(filepath)
            print(f"\nFile: {filename}")
            print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
            print(f"Columns: {list(df.columns)}")
        except Exception as e:
            print(f"Error reading {filename}: {e}")

if __name__ == "__main__":
    download_datasets()
    inspect_downloaded()
