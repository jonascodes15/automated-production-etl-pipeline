import json
from pathlib import Path
from typing import List, Dict

def run_transformation(file_path: Path) -> List[Dict]:
    print(" Starting Transformation Phase...")
    
    with open(file_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)
        
    cleaned_records = []
    
    for user in raw_data:
        # Flattening nested data structures safely
        cleaned_records.append({
            "id": user["login"]["uuid"],
            "first_name": user["name"]["first"].title(),
            "last_name": user["name"]["last"].title(),
            "email": user["email"].lower(),
            "country": user["location"]["country"],
            "age": int(user["dob"]["age"])
        })
        
    print(f" Transformed {len(cleaned_records)} records cleanly.")
    return cleaned_records
