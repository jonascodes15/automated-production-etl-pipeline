import json
import requests
from pathlib import Path

def run_extraction() -> Path:
    print(" Starting Extraction Phase...")
    url = "https://randomuser.me/api/?results=10"
    
    response = requests.get(url)
    response.raise_for_status()  # Throws an error if the website is down
    data = response.json()["results"]
    
    # Save the raw data to our data folder
    output_path = Path("data/raw_users.json")
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        
    print(f" Extracted 10 raw profiles to {output_path}")
    return output_path

