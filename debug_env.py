import os
from pathlib import Path
from dotenv import load_dotenv

# Try loading from CWD
print(f"CWD: {os.getcwd()}")
load_dotenv()

keys = ['CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET']
print("--- Checking Environment Variables ---")
for k in keys:
    val = os.environ.get(k)
    status = "SET" if val else "MISSING"
    # detailed check for empty string
    if val == "": status = "EMPTY STRING"
    print(f"{k}: {status}")

# Try loading explicitly from BASE_DIR logic
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'
print(f"--- Checking Explicit Path: {env_path} ---")
print(f"Exists: {env_path.exists()}")
