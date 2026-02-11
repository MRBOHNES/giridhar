import os
import json
import numpy as np
import rasterio
from rasterio.transform import from_origin
from datetime import datetime

# CONFIGURATION
LAT_CENTER = 22.5726
LON_CENTER = 88.3639
RUN_ID = f"run_{datetime.now().strftime('%Y_%m_%d_%H%M')}_MANUAL"

# --- THE MANUAL FIX ---
# We are forcing the path to: D:\yoyoyoyo\river\Flowz\data_store\runs\...
OUTPUT_DIR = fr"D:\yoyoyoyo\river\Flowz\data_store\runs\{RUN_ID}\04_predictions"

def generate_synthetic_flood():
    print(f"🧠 AI Model Starting for: {RUN_ID}")
    print(f"📂 Saving to: {OUTPUT_DIR}") 
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # 1. Generate Flood Map
    data = np.zeros((100, 100), dtype=rasterio.float32)
    for i in range(100):
        for j in range(100):
            dist = np.sqrt((i-50)**2 + (j-50)**2)
            if dist < 30:
                data[i, j] = (30 - dist) / 10.0
    
    transform = from_origin(LON_CENTER - 0.5, LAT_CENTER + 0.5, 0.01, 0.01)
    with rasterio.open(os.path.join(OUTPUT_DIR, "final_map.tif"), 'w', driver='GTiff', 
                       height=100, width=100, count=1, dtype=data.dtype,
                       crs='+proj=latlong', transform=transform) as dst:
        dst.write(data, 1)

    # 2. Generate Summary
    summary = [{
        "id": RUN_ID,
        "location": "Kolkata Region",
        "latitude": LAT_CENTER,
        "longitude": LON_CENTER,
        "riskScore": 0.95,
        "severityLevel": "CRITICAL",
        "waterLevel": 3.2,
        "status": "ACTIVE",
        "timestamp": datetime.now().isoformat()
    }]
    
    with open(os.path.join(OUTPUT_DIR, "risk_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"✅ FIXED! Data saved to correct folder.")

if __name__ == "__main__":
    generate_synthetic_flood()