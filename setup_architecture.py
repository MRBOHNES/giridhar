import os

# We are currently in D:\yoyoyoyo\river\Flowz
ROOT_DIR = os.getcwd()

print(f"🌊 Injecting Flood Engine into: {ROOT_DIR}")

# 1. Define the NEW folders we need to add to Flowz
new_folders = [
    # The "Brain" (Your Processing Pipeline)
    "pipeline/01_ingestion",    # Step 1: Prep weather data
    "pipeline/02_lisflood_os",  # Step 2: Hydrology (Rain -> Flow)
    "pipeline/03_lisflood_fp",  # Step 3: Hydraulics (Flow -> Flood Map)
    "pipeline/04_ai_model",     # Step 4: AI Prediction
    
    # The "Memory" (Your File Database)
    "data_store/inputs",        # Uploaded files
    "data_store/static_maps",   # Topography/Land use
    "data_store/runs",          # The "Database Rows"
]

# 2. Create them
for folder in new_folders:
    path = os.path.join(ROOT_DIR, folder)
    os.makedirs(path, exist_ok=True)
    
    # Add __init__.py to pipeline folders so Python can see them
    if "pipeline" in folder:
        init_path = os.path.join(path, "__init__.py")
        if not os.path.exists(init_path):
            with open(init_path, 'w') as f:
                pass 
    
    print(f"✅ Injected: {folder}")

# 3. Create the Orchestrator File (The Traffic Cop)
orchestrator_path = os.path.join(ROOT_DIR, "pipeline", "orchestrator.py")
if not os.path.exists(orchestrator_path):
    with open(orchestrator_path, "w") as f:
        f.write("# This script will manage the flow: Ingestion -> OS -> FP -> AI\n")
        f.write("def run_pipeline(run_id):\n")
        f.write("    print(f'Starting pipeline for {run_id}...')\n")
    print("✅ Created: pipeline/orchestrator.py")

print("\n🚀 Integration Complete! Your Flowz app now has a backend engine.")