import sys
import traceback

from pipeline.extract import run_extraction
from pipeline.transform import run_transformation
from pipeline.load import run_loading

def run_pipeline():
    print("=== STARTING THE ETL AUTOMATION PIPELINE ===", flush=True)
    
    try:
        # 1. EXTRACT
        raw_file = run_extraction()
        
        # 2. TRANSFORM
        cleaned_data = run_transformation(raw_file)
        
        # 3. LOAD
        run_loading(cleaned_data)
        
        print("=== ETL PIPELINE EXECUTION SUCCESSFUL ===", flush=True)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {type(e).__name__}", flush=True)
        print(f"Message: {str(e)}", flush=True)
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
