from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
import json

router = APIRouter()

# 1. DYNAMIC PATH FINDING
# This allows the code to find 'data_store' no matter where you install it
# We go up 4 levels: routers -> app -> backend -> Flowz -> data_store
CURRENT_FILE = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE))))
DATA_STORE = os.path.join(BASE_DIR, "data_store", "runs")

print(f"📂 Predictions Router is looking for data in: {DATA_STORE}")

@router.get("/predictions/current")
async def get_current_predictions():
    """
    Finds the latest simulation folder in 'data_store/runs'
    and returns its summary JSON to the frontend.
    """
    # Check if folder exists
    if not os.path.exists(DATA_STORE):
        print("❌ Data Store folder not found!")
        return {"predictions": []}
        
    # Get all run folders (e.g., "run_2026_02_10...")
    all_runs = sorted(os.listdir(DATA_STORE), reverse=True)
    
    if not all_runs:
        print("⚠️ No simulation runs found yet.")
        return {"predictions": []}
    
    # Pick the newest one
    latest_run_id = all_runs[0]
    run_folder = os.path.join(DATA_STORE, latest_run_id)
    
    # Look for the result file from Step 04 (AI Model)
    # We expect: data_store/runs/{run_id}/04_predictions/risk_summary.json
    result_file = os.path.join(run_folder, "04_predictions", "risk_summary.json")
    
    if os.path.exists(result_file):
        with open(result_file, 'r') as f:
            data = json.load(f)
        return {"predictions": data, "source": "REAL_ENGINE", "run_id": latest_run_id}
    
    # If the folder exists but no result yet, it's still processing
    return {
        "status": "processing", 
        "message": "Simulation is running...", 
        "run_id": latest_run_id
    }

@router.get("/predictions/map/{run_id}")
async def get_flood_map(run_id: str):
    """
    Directly serves the Flood Map TIF or PNG image to the frontend.
    Example: <img src="/api/predictions/map/run_2026_..." />
    """
    # Security check: prevent users from asking for ".." paths
    safe_id = os.path.basename(run_id)
    
    map_path = os.path.join(DATA_STORE, safe_id, "04_predictions", "final_map.tif")
    
    if os.path.exists(map_path):
        return FileResponse(map_path)
    
    raise HTTPException(status_code=404, detail="Flood map not found")