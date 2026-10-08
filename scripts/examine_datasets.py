import urllib.request
import json
import io
import pandas as pd

def check_ndap():
    url = 'https://api.github.com/repos/Saurabh-Vidyarthi/Classification_of_Indian_cities_based_on_road_accident_using_NDAP_Dataset/contents/Road_Accident_Classificaion'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())
            for item in data:
                print(f"NDAP item: {item['name']} ({item['type']}, size: {item.get('size', 0)}, url: {item.get('download_url')})")
    except Exception as e:
        print("NDAP error:", e)

def preview_csv(url, name):
    print(f"\n================ Previewing {name} ================")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            # Read first 100KB
            chunk = resp.read(150000)
            df = pd.read_csv(io.BytesIO(chunk), nrows=10)
            print(f"Columns ({len(df.columns)}):", list(df.columns))
            print("\nFirst 3 rows:")
            print(df.head(3).to_dict(orient='records'))
    except Exception as e:
        print("Error previewing:", e)

if __name__ == '__main__':
    check_ndap()
    preview_csv('https://raw.githubusercontent.com/Prashantsundar/Indian-Road-Accident-Dataset-Analysis-2022-2025-Python---Jupyternotebook/main/indian_roads_dataset.csv', 'Prashantsundar / indian_roads_dataset.csv')
    preview_csv('https://raw.githubusercontent.com/rahul-saha18/India-Road-Accident-Exploratory-Data-Analysis./main/accident_prediction_india.csv', 'rahul-saha18 / accident_prediction_india.csv')
